import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from storage.database.supabase_client import get_supabase_client

# 清空rss_tracking表，以便测试新内容同步
def clear_tracking_table():
    client = get_supabase_client()
    try:
        # 删除所有记录
        result = client.table('rss_tracking').delete().neq('id', 0).execute()
        print(f"已清空rss_tracking表，删除了记录")
        return True
    except Exception as e:
        print(f"清空表失败: {e}")
        return False

if __name__ == "__main__":
    clear_tracking_table()
