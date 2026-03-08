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
from graphs.state import RecordProcessedInput, RecordProcessedOutput
from storage.database.supabase_client import get_supabase_client

def record_processed_node(state: RecordProcessedInput, config: RunnableConfig, runtime: Runtime[Context]) -> RecordProcessedOutput:
    """
    title: 记录已处理内容
    desc: 将已处理的RSS条目记录到数据库中，避免重复处理
    integrations: Supabase
    """
    ctx = runtime.context
    
    try:
        client = get_supabase_client()
        
        # 批量插入已处理的记录
        records_to_insert = []
        for item in state.processed_items:
            record = {
                "link": item.get("link", ""),
                "title": item.get("title", "")
            }
            records_to_insert.append(record)
        
        if records_to_insert:
            client.table('rss_tracking').insert(records_to_insert).execute()
        
        return RecordProcessedOutput(processed_count=len(state.processed_items))
    except Exception as e:
        raise Exception(f"记录已处理内容失败: {e}")
