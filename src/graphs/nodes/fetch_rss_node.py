import feedparser
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
from graphs.state import FetchRssInput, FetchRssOutput

def fetch_rss_node(state: FetchRssInput, config: RunnableConfig, runtime: Runtime[Context]) -> FetchRssOutput:
    """
    title: 读取RSS内容
    desc: 从RSS链接中获取所有新闻条目
    integrations: feedparser
    """
    ctx = runtime.context
    
    try:
        # 使用feedparser读取RSS
        rss_feed = feedparser.parse(state.rss_url)
        
        # 提取所有条目
        all_items = []
        for entry in rss_feed.entries:
            item = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "description": entry.get("description", ""),
                "summary": entry.get("summary", "")
            }
            all_items.append(item)
        
        return FetchRssOutput(all_rss_items=all_items)
    except Exception as e:
        raise Exception(f"读取RSS失败: {e}")
