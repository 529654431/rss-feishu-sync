import os
import json
import re
import time
import datetime
import math
import logging
from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from coze_workload_identity import Client
from cozeloop.decorator import observe
from graphs.state import WriteToFeishuInput, WriteToFeishuOutput

# 子图状态定义
class LoopGlobalState(BaseModel):
    """循环子图的全局状态"""
    items: List[Dict[str, Any]] = Field(default=[], description="待处理的条目列表")
    processed_items: List[Dict[str, Any]] = Field(default=[], description="已处理的条目列表")
    app_token: str = Field(..., description="飞书多维表格app_token")
    table_id: str = Field(..., description="飞书多维表格table_id")
    current_index: int = Field(default=0, description="当前处理的索引")

class LoopGraphInput(BaseModel):
    """循环子图的输入"""
    items: List[Dict[str, Any]] = Field(..., description="待处理的条目列表")
    app_token: str = Field(..., description="飞书多维表格app_token")
    table_id: str = Field(..., description="飞书多维表格table_id")

class LoopGraphOutput(BaseModel):
    """循环子图的输出"""
    processed_items: List[Dict[str, Any]] = Field(..., description="已处理的条目列表")

# 飞书客户端
def get_access_token() -> str:
    """
    获取飞书多维表格的租户访问令牌。
    """
    client = Client()
    access_token = client.get_integration_credential("integration-feishu-base")
    return access_token

@observe
def add_records_to_feishu(
    app_token: str,
    table_id: str,
    records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    向飞书多维表格批量添加记录
    """
    import requests
    
    access_token = get_access_token()
    if not access_token:
        raise ValueError("FEISHU_TENANT_ACCESS_TOKEN is not set")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    
    url = f"https://open.larkoffice.com/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    
    try:
        resp = requests.request(
            "POST",
            url,
            headers=headers,
            json={"records": records},
            timeout=30
        )
        resp_data = resp.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Feishu API request error: {e}")
    
    if resp_data.get("code") != 0:
        raise Exception(f"Feishu API error: {resp_data}")
    
    return resp_data

# 写入飞书节点
def write_to_feishu_node(
    state: LoopGlobalState,
    config: RunnableConfig,
    runtime
) -> LoopGlobalState:
    """
    title: 写入飞书表格
    desc: 将单个RSS条目写入飞书多维表格
    integrations: 飞书多维表格
    """
    if state.current_index >= len(state.items):
        return state
    
    # 获取当前条目
    item = state.items[state.current_index]
    
    try:
        # 构建飞书记录
        record = {
            "fields": {
                "标题": item.get("title", ""),
                "链接": item.get("link", ""),
                "发布时间": item.get("published", ""),
                "描述": item.get("description", "")
            }
        }
        
        # 写入飞书
        add_records_to_feishu(
            app_token=state.app_token,
            table_id=state.table_id,
            records=[record]
        )
        
        # 添加到已处理列表
        processed_items = state.processed_items.copy()
        processed_items.append(item)
        
        # 更新状态
        return state.model_copy(
            update={
                "processed_items": processed_items,
                "current_index": state.current_index + 1
            }
        )
    except Exception as e:
        # 记录错误但继续处理下一条
        print(f"写入飞书失败: {e}")
        return state.model_copy(
            update={
                "current_index": state.current_index + 1
            }
        )

# 循环条件判断
def should_continue_loop(state: LoopGlobalState) -> str:
    """
    title: 是否继续循环
    desc: 判断是否还有待处理的条目
    """
    if state.current_index < len(state.items):
        return "继续"
    else:
        return "结束"

# 构建子图
def build_loop_graph():
    """
    构建循环子图，用于逐条写入飞书表格
    """
    builder = StateGraph(LoopGlobalState, input_schema=LoopGraphInput, output_schema=LoopGraphOutput)
    
    # 添加节点
    builder.add_node("write_to_feishu", write_to_feishu_node)
    
    # 设置入口点
    builder.set_entry_point("write_to_feishu")
    
    # 添加循环条件边
    builder.add_conditional_edges(
        source="write_to_feishu",
        path=should_continue_loop,
        path_map={
            "继续": "write_to_feishu",
            "结束": END
        }
    )
    
    return builder.compile()

# 编译子图
subgraph = build_loop_graph()
