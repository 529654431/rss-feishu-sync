#!/usr/bin/env python3
"""
GitHub Actions专用的RSS同步脚本
每小时整点自动执行，将新内容写入飞书表格
"""

import os
import sys
import requests
import feedparser
from datetime import datetime
from typing import List, Dict, Optional


class RSSSyncer:
    """RSS同步器"""
    
    def __init__(self):
        """初始化配置"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.rss_url = os.getenv("RSS_URL", "https://cn.investing.com/rss/news_285.rss")
        self.feishu_app_token = os.getenv("FEISHU_APP_TOKEN")
        self.feishu_table_id = os.getenv("FEISHU_TABLE_ID")
        self.feishu_app_id = os.getenv("FEISHU_APP_ID")
        self.feishu_app_secret = os.getenv("FEISHU_APP_SECRET")
        
        # 飞书访问令牌（缓存）
        self.feishu_access_token = None
        
    def fetch_rss(self) -> List[Dict]:
        """获取RSS内容"""
        print(f"📡 正在获取RSS: {self.rss_url}")
        
        try:
            feed = feedparser.parse(self.rss_url)
            items = []
            
            for entry in feed.entries:
                item = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "description": entry.get("description", "")
                }
                items.append(item)
            
            print(f"✅ 成功获取 {len(items)} 条RSS记录")
            return items
            
        except Exception as e:
            print(f"❌ 获取RSS失败: {e}")
            return []
    
    def get_processed_links(self) -> set:
        """获取已处理的链接集合"""
        print("🔍 查询已处理的链接...")
        
        try:
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.supabase_url}/rest/v1/rss_tracking?select=link",
                headers=headers
            )
            
            if response.status_code == 200:
                links = {item["link"] for item in response.json()}
                print(f"✅ 已处理 {len(links)} 条记录")
                return links
            else:
                print(f"⚠️  查询失败: {response.status_code}")
                return set()
                
        except Exception as e:
            print(f"❌ 查询已处理链接失败: {e}")
            return set()
    
    def get_feishu_access_token(self) -> Optional[str]:
        """获取飞书访问令牌"""
        if self.feishu_access_token:
            return self.feishu_access_token
        
        print("🔑 获取飞书访问令牌...")
        
        try:
            response = requests.post(
                "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
                json={
                    "app_id": self.feishu_app_id,
                    "app_secret": self.feishu_app_secret
                }
            )
            
            if response.status_code == 200:
                self.feishu_access_token = response.json()["app_access_token"]
                print("✅ 成功获取飞书访问令牌")
                return self.feishu_access_token
            else:
                print(f"❌ 获取飞书令牌失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 获取飞书令牌异常: {e}")
            return None
    
    def write_to_feishu(self, item: Dict) -> bool:
        """写入单条记录到飞书表格"""
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.feishu_app_token}/tables/{self.feishu_table_id}/records"
            
            headers = {
                "Authorization": f"Bearer {self.feishu_access_token}",
                "Content-Type": "application/json"
            }
            
            record = {
                "fields": {
                    "聊天记录": item["title"],
                    "消息链接": {"link": item["link"]},
                    "时间": item["published"],
                    "发送日期": item["description"]
                }
            }
            
            response = requests.post(
                url,
                headers=headers,
                json={"records": [record]}
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"⚠️  写入失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 写入飞书异常: {e}")
            return False
    
    def record_processed(self, item: Dict) -> bool:
        """记录已处理的链接"""
        try:
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "link": item["link"],
                "title": item["title"],
                "processed_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.supabase_url}/rest/v1/rss_tracking",
                headers=headers,
                json=data
            )
            
            return response.status_code == 201
            
        except Exception as e:
            print(f"❌ 记录处理失败: {e}")
            return False
    
    def run(self) -> Dict:
        """执行完整流程"""
        print("=" * 50)
        print("🚀 开始RSS同步任务")
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # 1. 获取RSS内容
        items = self.fetch_rss()
        if not items:
            return {"success": False, "message": "获取RSS内容失败"}
        
        # 2. 获取已处理的链接
        processed_links = self.get_processed_links()
        
        # 3. 过滤新内容
        new_items = [item for item in items if item["link"] not in processed_links]
        print(f"🔍 发现 {len(new_items)} 条新内容")
        
        if not new_items:
            print("✅ 没有新内容需要处理")
            return {"success": True, "processed_count": 0}
        
        # 4. 获取飞书访问令牌
        token = self.get_feishu_access_token()
        if not token:
            return {"success": False, "message": "获取飞书令牌失败"}
        
        # 5. 写入飞书表格
        success_count = 0
        failed_count = 0
        
        print("📝 开始写入飞书表格...")
        for i, item in enumerate(new_items, 1):
            print(f"  [{i}/{len(new_items)}] 处理: {item['title'][:30]}...")
            
            if self.write_to_feishu(item):
                success_count += 1
                print(f"    ✅ 写入成功")
            else:
                failed_count += 1
                print(f"    ❌ 写入失败")
        
        # 6. 记录已处理
        print("💾 记录已处理的链接...")
        recorded_count = 0
        for item in new_items:
            if self.record_processed(item):
                recorded_count += 1
        
        # 输出结果
        print("=" * 50)
        print("📊 执行结果:")
        print(f"  ✅ 成功: {success_count} 条")
        print(f"  ❌ 失败: {failed_count} 条")
        print(f"  💾 记录: {recorded_count} 条")
        print("=" * 50)
        
        return {
            "success": True,
            "processed_count": success_count,
            "failed_count": failed_count,
            "recorded_count": recorded_count
        }


def main():
    """主函数"""
    print("\n")
    print("🎯 RSS监测与飞书同步 - GitHub Actions版")
    print("\n")
    
    # 检查环境变量
    required_vars = [
        "SUPABASE_URL", "SUPABASE_KEY",
        "FEISHU_APP_TOKEN", "FEISHU_TABLE_ID",
        "FEISHU_APP_ID", "FEISHU_APP_SECRET"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n请在GitHub仓库的Settings → Secrets中配置这些变量")
        sys.exit(1)
    
    # 执行同步
    syncer = RSSSyncer()
    result = syncer.run()
    
    # 退出码
    if result["success"]:
        print("\n✅ 任务执行成功！")
        sys.exit(0)
    else:
        print(f"\n❌ 任务执行失败: {result.get('message', '未知错误')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
