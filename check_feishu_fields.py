import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import requests
from coze_workload_identity import Client

def get_feishu_fields():
    """获取飞书表格的字段信息"""
    app_token = "KqLSb9eeqaOYstsryBMcCiJTnkc"
    table_id = "tbl6xkic4IuaOH6u"
    
    client = Client()
    access_token = client.get_integration_credential("integration-feishu-base")
    
    if not access_token:
        print("无法获取飞书访问令牌")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    
    url = f"https://open.larkoffice.com/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        result = resp.json()
        
        if result.get("code") == 0:
            fields = result.get("data", {}).get("items", [])
            print(f"飞书表格字段列表（共{len(fields)}个字段）：\n")
            for field in fields:
                field_id = field.get("field_id")
                field_name = field.get("field_name")
                field_type = field.get("type")
                print(f"字段ID: {field_id}")
                print(f"字段名称: {field_name}")
                print(f"字段类型: {field_type}")
                print("-" * 50)
        else:
            print(f"获取字段失败: {result}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    get_feishu_fields()
