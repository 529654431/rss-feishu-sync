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
from graphs.state import FilterNewItemsInput, FilterNewItemsOutput
from storage.database.supabase_client import get_supabase_client

def filter_new_items_node(state: FilterNewItemsInput, config: RunnableConfig, runtime: Runtime[Context]) -> FilterNewItemsOutput:
    """
    title: 过滤新内容
    desc: 从所有RSS条目中过滤出未处理的新内容
    integrations: Supabase
    """
    ctx = runtime.context
    
    try:
        # 获取所有已处理的链接
        client = get_supabase_client()
        response = client.table('rss_tracking').select('link').execute()
        
        # 提取已处理的链接列表
        processed_links = set()
        if response.data:
            if isinstance(response.data, list):
                for record in response.data:
                    if isinstance(record, dict):
                        link = record.get('link')
                        if link:
                            processed_links.add(link)
        
        # 过滤出新内容
        new_items = []
        for item in state.all_rss_items:
            link = item.get('link', '')
            if link and link not in processed_links:
                new_items.append(item)
        
        return FilterNewItemsOutput(new_items=new_items)
    except Exception as e:
        raise Exception(f"过滤新内容失败: {e}")
