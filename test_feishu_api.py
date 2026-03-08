#!/usr/bin/env python3
"""
飞书API测试脚本
用于诊断飞书表格写入问题
"""

import os
import requests
import json


def test_feishu_api():
    """测试飞书API"""
    print("=" * 60)
    print("🧪 飞书API诊断测试")
    print("=" * 60)
    
    # 获取环境变量
    app_token = os.getenv("FEISHU_APP_TOKEN")
    table_id = os.getenv("FEISHU_TABLE_ID")
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    print("\n📋 配置信息:")
    print(f"  App Token: {app_token}")
    print(f"  Table ID: {table_id}")
    print(f"  App ID: {app_id}")
    print(f"  App Secret: {'*' * len(app_secret) if app_secret else '未设置'}")
    
    # 步骤1: 获取访问令牌
    print("\n" + "=" * 60)
    print("步骤1: 获取飞书访问令牌")
    print("=" * 60)
    
    try:
        response = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
            json={
                "app_id": app_id,
                "app_secret": app_secret
            }
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code != 200:
            print("❌ 获取访问令牌失败")
            return False
        
        access_token = response.json().get("app_access_token")
        print(f"✅ 成功获取访问令牌: {access_token[:20]}...")
        
    except Exception as e:
        print(f"❌ 获取访问令牌异常: {e}")
        return False
    
    # 步骤2: 查看表格字段信息
    print("\n" + "=" * 60)
    print("步骤2: 查看表格字段信息")
    print("=" * 60)
    
    try:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        print(f"URL: {url}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            fields = response.json().get("data", {}).get("items", [])
            print(f"\n✅ 找到 {len(fields)} 个字段:")
            for field in fields:
                field_name = field.get("field_name")
                field_type = field.get("type")
                print(f"  - {field_name} ({field_type})")
        else:
            print(f"❌ 查询字段失败")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 查询字段异常: {e}")
        return False
    
    # 步骤3: 测试写入一条记录
    print("\n" + "=" * 60)
    print("步骤3: 测试写入一条记录")
    print("=" * 60)
    
    try:
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 构建测试记录
        record = {
            "fields": {
                "聊天记录": "🧪 测试标题 - " + __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "消息链接": {
                    "link": "https://example.com/test"
                },
                "时间": __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "发送日期": "这是一个测试描述，用于验证飞书API是否正常工作"
            }
        }
        
        print(f"URL: {url}")
        print(f"测试记录: {json.dumps(record, indent=2, ensure_ascii=False)}")
        
        response = requests.post(
            url,
            headers=headers,
            json={"records": [record]}
        )
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ 写入成功！")
            return True
        else:
            print("❌ 写入失败")
            return False
            
    except Exception as e:
        print(f"❌ 写入异常: {e}")
        return False


def main():
    """主函数"""
    print("\n")
    print("🔍 飞书API诊断工具")
    print("\n")
    
    # 检查环境变量
    required_vars = [
        "FEISHU_APP_TOKEN", "FEISHU_TABLE_ID",
        "FEISHU_APP_ID", "FEISHU_APP_SECRET"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ 缺少必要的环境变量:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n请设置环境变量:")
        print("  export FEISHU_APP_TOKEN=xxx")
        print("  export FEISHU_TABLE_ID=xxx")
        print("  export FEISHU_APP_ID=xxx")
        print("  export FEISHU_APP_SECRET=xxx")
        return
    
    # 执行测试
    success = test_feishu_api()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 飞书API测试通过！")
        print("如果Actions中写入失败，请检查:")
        print("  1. 飞书应用是否已发布")
        print("  2. 飞书应用是否开通bitable:app权限")
        print("  3. 表格字段名是否匹配")
    else:
        print("❌ 飞书API测试失败")
        print("请根据上面的错误信息进行排查")
    print("=" * 60)


if __name__ == "__main__":
    main()
