import os
import json
import re
import time
import datetime
import math
import logging
from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field

# Global State
class GlobalState(BaseModel):
    """全局状态定义"""
    rss_url: str = Field(..., description="RSS链接地址")
    app_token: str = Field(..., description="飞书多维表格app_token")
    table_id: str = Field(..., description="飞书多维表格table_id")
    all_rss_items: List[Dict[str, Any]] = Field(default=[], description="RSS所有条目")
    new_items: List[Dict[str, Any]] = Field(default=[], description="新内容条目列表")
    processed_items: List[Dict[str, Any]] = Field(default=[], description="已处理的条目列表")
    processed_count: int = Field(default=0, description="已处理的条目数量")
    result_message: str = Field(default="", description="执行结果消息")

# Graph Input/Output
class GraphInput(BaseModel):
    """工作流的输入"""
    rss_url: str = Field(..., description="RSS链接地址")
    app_token: str = Field(..., description="飞书多维表格app_token")
    table_id: str = Field(..., description="飞书多维表格table_id")

class GraphOutput(BaseModel):
    """工作流的输出"""
    result_message: str = Field(..., description="执行结果消息")
    processed_count: int = Field(..., description="处理的条目数量")

# Fetch RSS Node
class FetchRssInput(BaseModel):
    """读取RSS节点的输入"""
    rss_url: str = Field(..., description="RSS链接地址")

class FetchRssOutput(BaseModel):
    """读取RSS节点的输出"""
    all_rss_items: List[Dict[str, Any]] = Field(..., description="RSS所有条目列表")

# Filter New Items Node
class FilterNewItemsInput(BaseModel):
    """过滤新内容节点的输入"""
    all_rss_items: List[Dict[str, Any]] = Field(..., description="RSS所有条目列表")

class FilterNewItemsOutput(BaseModel):
    """过滤新内容节点的输出"""
    new_items: List[Dict[str, Any]] = Field(..., description="新内容条目列表")

# Record Processed Node
class RecordProcessedInput(BaseModel):
    """记录已处理节点的输入"""
    processed_items: List[Dict[str, Any]] = Field(..., description="已处理的条目列表")

class RecordProcessedOutput(BaseModel):
    """记录已处理节点的输出"""
    processed_count: int = Field(..., description="已处理的条目数量")

# Process New Items Node (调用子图)
class ProcessNewItemsInput(BaseModel):
    """处理新内容节点的输入（调用子图）"""
    new_items: List[Dict[str, Any]] = Field(..., description="新内容条目列表")
    app_token: str = Field(..., description="飞书多维表格app_token")
    table_id: str = Field(..., description="飞书多维表格table_id")

class ProcessNewItemsOutput(BaseModel):
    """处理新内容节点的输出"""
    processed_items: List[Dict[str, Any]] = Field(..., description="已处理的条目列表")

# Prepare Empty List Node
class PrepareEmptyListInput(BaseModel):
    """准备空列表节点的输入"""
    pass

class PrepareEmptyListOutput(BaseModel):
    """准备空列表节点的输出"""
    processed_items: List[Dict[str, Any]] = Field(default=[], description="已处理的条目列表")

# Loop Graph - Write to Feishu Node
class WriteToFeishuInput(BaseModel):
    """写入飞书节点的输入"""
    item: Dict[str, Any] = Field(..., description="单个RSS条目")
    app_token: str = Field(..., description="飞书多维表格app_token")
    table_id: str = Field(..., description="飞书多维表格table_id")

class WriteToFeishuOutput(BaseModel):
    """写入飞书节点的输出"""
    success: bool = Field(..., description="是否写入成功")
