import os
import json
import re
import time
import datetime
import math
import logging
from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context

from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
    PrepareEmptyListInput,
    PrepareEmptyListOutput
)
from graphs.nodes.fetch_rss_node import fetch_rss_node
from graphs.nodes.filter_new_items_node import filter_new_items_node
from graphs.nodes.process_new_items_node import process_new_items_node
from graphs.nodes.record_processed_node import record_processed_node

# 条件判断函数：是否有新内容需要处理
def should_check_new_items(state: GlobalState) -> str:
    """
    title: 是否有新内容
    desc: 判断是否有新内容需要处理
    """
    if len(state.new_items) > 0:
        return "处理新内容"
    else:
        return "直接结束"

# 辅助节点：在没有新内容时设置空列表
def prepare_processed_items(state: PrepareEmptyListInput, config: RunnableConfig, runtime: Runtime[Context]) -> PrepareEmptyListOutput:
    """
    title: 准备已处理列表
    desc: 在没有新内容时设置空的已处理列表
    """
    return PrepareEmptyListOutput(processed_items=[])

# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("fetch_rss", fetch_rss_node)
builder.add_node("filter_new_items", filter_new_items_node)
builder.add_node("process_new_items", process_new_items_node, metadata={"type": "looparray"})
builder.add_node("prepare_empty_list", prepare_processed_items)
builder.add_node("record_processed", record_processed_node)

# 设置入口点
builder.set_entry_point("fetch_rss")

# 添加边
builder.add_edge("fetch_rss", "filter_new_items")
builder.add_conditional_edges(
    source="filter_new_items",
    path=should_check_new_items,
    path_map={
        "处理新内容": "process_new_items",
        "直接结束": "prepare_empty_list"
    }
)
builder.add_edge("process_new_items", "record_processed")
builder.add_edge("prepare_empty_list", "record_processed")
builder.add_edge("record_processed", END)

# 编译图
main_graph = builder.compile()
