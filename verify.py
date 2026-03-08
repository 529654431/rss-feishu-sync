#!/usr/bin/env python3
"""
验证脚本 - 检查RSS监测工作流是否正常运行
"""

import os
import requests
import json
from datetime import datetime, timedelta


def check_supabase():
    """检查Supabase数据库记录"""
    print("=" * 60)
    print("📊 检查Supabase数据库")
    print("=" * 60)
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ 缺少Supabase环境变量")
        print("请设置 SUPABASE_URL 和 SUPABASE_KEY")
        return False
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # 查询总记录数
        response = requests.get(
            f"{supabase_url}/rest/v1/rss_tracking?select=count",
            headers=headers
        )
        
        if response.status_code == 200:
            count_data = response.json()
            total_count = count_data[0]["count"] if count_data else 0
            print(f"✅ 数据库总记录数: {total_count}")
        else:
            print(f"❌ 查询失败: {response.status_code}")
            return False
        
        # 查询最近1小时的记录
        one_hour_ago = datetime.now() - timedelta(hours=1)
        response = requests.get(
            f"{supabase_url}/rest/v1/rss_tracking?select=*&processed_at=gt.{one_hour_ago.isoformat()}&order=processed_at.desc&limit=5",
            headers=headers
        )
        
        if response.status_code == 200:
            recent_records = response.json()
            print(f"\n📝 最近1小时内的记录: {len(recent_records)} 条")
            
            if recent_records:
                print("\n最近5条记录:")
                for i, record in enumerate(recent_records[:5], 1):
                    print(f"  {i}. {record['title'][:50]}...")
                    print(f"     链接: {record['link'][:60]}...")
                    print(f"     处理时间: {record['processed_at']}")
        else:
            print(f"❌ 查询最近记录失败: {response.status_code}")
        
        # 检查是否有重复
        response = requests.get(
            f"{supabase_url}/rest/v1/rss_tracking?select=link",
            headers=headers
        )
        
        if response.status_code == 200:
            links = [r["link"] for r in response.json()]
            unique_count = len(set(links))
            duplicate_count = len(links) - unique_count
            
            if duplicate_count > 0:
                print(f"\n⚠️  发现 {duplicate_count} 条重复记录")
                print("⚠️  建议清理重复数据")
            else:
                print(f"\n✅ 无重复记录（共 {len(links)} 条唯一链接）")
        
        return True
        
    except Exception as e:
        print(f"❌ 检查数据库时出错: {e}")
        return False


def check_github_actions():
    """检查GitHub Actions执行历史（需要用户提供信息）"""
    print("\n" + "=" * 60)
    print("🔍 检查GitHub Actions执行状态")
    print("=" * 60)
    
    print("\n请访问以下页面查看执行历史:")
    print("📌 https://github.com/529654431/rss-feishu-sync/actions")
    print("\n检查项:")
    print("  ✓ 是否有最近的执行记录")
    print("  ✓ 执行状态是否为✅成功")
    print("  ✓ 执行时间是否为整点（如 23:00, 00:00）")
    print("  ✓ 日志中是否显示'任务执行成功'")
    
    print("\n预期执行时间:")
    print("  每小时整点: 00:00, 01:00, 02:00, ..., 23:00")


def check_feishu():
    """提示检查飞书表格"""
    print("\n" + "=" * 60)
    print("📱 检查飞书多维表格")
    print("=" * 60)
    
    print("\n请打开飞书多维表格:")
    print("📌 App Token: KqLSb9eeqaOYstsryBMcCiJTnkc")
    print("📌 Table ID: tbl6xkic4IuaOH6u")
    
    print("\n检查项:")
    print("  ✓ '聊天记录'字段是否有新RSS标题")
    print("  ✓ '消息链接'字段是否有有效链接")
    print("  ✓ '时间'字段是否有发布时间")
    print("  ✓ 最近记录的时间戳是否正确")


def print_summary():
    """打印验证摘要"""
    print("\n" + "=" * 60)
    print("📋 验证检查清单")
    print("=" * 60)
    
    print("\n请逐项确认:")
    print()
    print("□ GitHub Actions有最近的执行记录")
    print("□ 执行状态为成功（绿色✅）")
    print("□ 执行时间为整点（如23:00）")
    print("□ 日志显示'任务执行成功'")
    print("□ Supabase数据库有新记录")
    print("□ 飞书表格有新RSS内容")
    print("□ 没有重复记录")
    print()
    print("如果以上所有项都✅，说明工作流正常运行！")
    print()
    print("如果发现❌，请查看执行日志诊断问题:")
    print("📌 https://github.com/529654431/rss-feishu-sync/actions")


def main():
    """主函数"""
    print("\n")
    print("🎯 RSS监测工作流 - 验证脚本")
    print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n")
    
    # 检查Supabase
    check_supabase()
    
    # 检查GitHub Actions（提示用户查看）
    check_github_actions()
    
    # 检查飞书（提示用户查看）
    check_feishu()
    
    # 打印摘要
    print_summary()
    
    print("\n" + "=" * 60)
    print("✅ 验证完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
