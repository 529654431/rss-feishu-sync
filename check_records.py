import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from storage.database.supabase_client import get_supabase_client

# 查询rss_tracking表中的记录
def check_records():
    client = get_supabase_client()
    try:
        result = client.table('rss_tracking').select('*').execute()
        records = result.data
        print(f"数据库中共有 {len(records)} 条记录")
        print("\n最近插入的记录：")
        for record in records:
            print(f"- {record.get('title', '')}")
            print(f"  链接: {record.get('link', '')}")
            print(f"  处理时间: {record.get('processed_at', '')}")
            print()
        return records
    except Exception as e:
        print(f"查询失败: {e}")
        return []

if __name__ == "__main__":
    check_records()
