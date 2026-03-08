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

# 创建logger
logger = logging.getLogger(__name__)

def process_new_items_node(state: ProcessNewItemsInput, config: RunnableConfig, runtime: Runtime[Context]) -> ProcessNewItemsOutput:
    """
    title: 处理新内容
    desc: 调用子图循环处理新内容并写入飞书表格
    integrations: 飞书多维表格
    """
    ctx = runtime.context
    
    logger.info(f"process_new_items_node被调用，新内容数量: {len(state.new_items)}")
    
    try:
        # 调用子图处理新内容
        result = subgraph.invoke({
            "items": state.new_items,
            "app_token": state.app_token,
            "table_id": state.table_id
        })
        
        # 调试输出
        logger.info(f"子图返回结果类型: {type(result)}")
        logger.info(f"子图返回结果: {result}")
        
        # 返回已处理的条目
        processed_items = result.get("processed_items", []) if isinstance(result, dict) else getattr(result, "processed_items", [])
        
        logger.info(f"提取的processed_items: {processed_items}")
        
        return ProcessNewItemsOutput(processed_items=processed_items)
    except Exception as e:
        logger.error(f"处理新内容异常: {e}")
        raise Exception(f"处理新内容失败: {e}")
