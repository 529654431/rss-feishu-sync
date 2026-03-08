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
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import ProcessNewItemsInput, ProcessNewItemsOutput
from graphs.loop_graph import subgraph

def process_new_items_node(state: ProcessNewItemsInput, config: RunnableConfig, runtime: Runtime[Context]) -> ProcessNewItemsOutput:
    """
    title: 处理新内容
    desc: 调用子图循环处理新内容并写入飞书表格
    integrations: 飞书多维表格
    """
    ctx = runtime.context
    
    try:
        # 调用子图处理新内容
        result = subgraph.invoke({
            "items": state.new_items,
            "app_token": state.app_token,
            "table_id": state.table_id
        })
        
        # 返回已处理的条目
        processed_items = result.get("processed_items", [])
        
        return ProcessNewItemsOutput(processed_items=processed_items)
    except Exception as e:
        raise Exception(f"处理新内容失败: {e}")
