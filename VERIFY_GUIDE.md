# 验证工作流是否正常运行

## 📋 快速验证清单

### 方法1：查看GitHub Actions（最简单）

1. **访问Actions页面**
   - https://github.com/529654431/rss-feishu-sync/actions

2. **检查执行历史**
   - ✅ 是否有最近的执行记录（今天/昨天）
   - ✅ 执行状态是否为绿色✅成功
   - ✅ 执行时间是否为整点（如 23:00, 00:00）

3. **查看执行日志**
   - 点击最近的执行记录
   - 滚动到日志底部
   - ✅ 应该看到：`✅ 任务执行成功！`
   - ✅ 显示处理记录数：`processed_count: X`

---

### 方法2：检查Supabase数据库

1. **登录Supabase**
   - https://supabase.com/
   - 进入你的项目

2. **查看数据表**
   - 点击左侧 "Table Editor"
   - 选择 `rss_tracking` 表

3. **检查记录**
   - ✅ 表中有记录
   - ✅ 最近记录的 `processed_at` 时间戳是最近1小时内
   - ✅ 没有 `link` 字段相同的重复记录

4. **查询最近记录**
   在SQL Editor中执行：
   ```sql
   -- 查询最近10条记录
   SELECT * FROM rss_tracking
   ORDER BY processed_at DESC
   LIMIT 10;

   -- 查询最近1小时的记录数
   SELECT COUNT(*) FROM rss_tracking
   WHERE processed_at > NOW() - INTERVAL '1 hour';

   -- 检查是否有重复
   SELECT link, COUNT(*) as count
   FROM rss_tracking
   GROUP BY link
   HAVING COUNT(*) > 1;
   ```

---

### 方法3：检查飞书表格

1. **打开飞书多维表格**
   - App Token: `KqLSb9eeqaOYstsryBMcCiJTnkc`
   - Table ID: `tbl6xkic4IuaOH6u`

2. **检查记录**
   - ✅ "聊天记录"字段有新RSS标题
   - ✅ "消息链接"字段有有效链接
   - ✅ "时间"字段有发布时间
   - ✅ 最近记录的时间戳是最近1小时内

---

### 方法4：使用验证脚本（可选）

如果环境中有SUPABASE_URL和SUPABASE_KEY：

```bash
# 设置环境变量
export SUPABASE_URL="你的Supabase URL"
export SUPABASE_KEY="你的Supabase Key"

# 运行验证脚本
python verify.py
```

脚本会自动检查：
- ✅ 数据库总记录数
- ✅ 最近1小时的记录
- ✅ 重复记录检测

---

## 🎯 验证标准

### ✅ 正常运行的标志：

| 检查项 | 正常标志 |
|--------|---------|
| GitHub Actions | 有最近执行记录，状态为✅成功 |
| 执行时间 | 为整点（如23:00） |
| 执行日志 | 显示"任务执行成功" |
| Supabase | 有新记录，processed_at在1小时内 |
| 飞书表格 | 有新RSS内容 |
| 重复检测 | 无重复记录 |

### ❌ 异常情况：

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 无执行记录 | 定时任务未激活 | 检查cron表达式 |
| 执行失败 | Secrets配置错误 | 检查7个Secrets |
| processed_count=0 | RSS无新内容 | 正常，等待下次 |
| 飞书无记录 | 飞书API权限问题 | 检查飞书应用权限 |
| 有重复记录 | 去重逻辑失效 | 检查数据库查询逻辑 |

---

## 📊 执行时间表

### Cron表达式：`0 * * * *`（UTC时区）

| 北京时间 | UTC时间 | 是否执行 |
|---------|---------|---------|
| 08:00 | 00:00 | ✅ 是 |
| 09:00 | 01:00 | ✅ 是 |
| ... | ... | ... |
| 23:00 | 15:00 | ✅ 是 |
| 00:00 | 16:00 | ✅ 是 |
| ... | ... | ... |
| 07:00 | 23:00 | ✅ 是 |

**注意**：北京时间整点对应UTC的16:00-15:00（跨越两天）

---

## 🔍 如何查看详细日志

1. 访问：https://github.com/529654431/rss-feishu-sync/actions
2. 点击最近的执行记录
3. 展开日志文件
4. 查看完整输出

---

## 💡 常见问题

### Q1: 为什么昨天没有执行？
**A**: 检查：
- Actions页面是否有昨天的执行记录
- cron表达式是否正确
- GitHub仓库是否为公开状态

### Q2: 执行成功但飞书无新记录
**A**:
- 检查processed_count是否>0
- 如果processed_count=0，说明RSS无新内容（正常）
- 如果processed_count>0但飞书无记录，检查飞书API权限

### Q3: 如何修改执行时间？
**A**: 编辑 `.github/workflows/rss-sync.yml`，修改cron表达式。

### Q4: 如何查看执行历史超过90天的记录？
**A**: GitHub Actions默认保留90天日志，如需更久记录，建议：
- 使用Supabase数据库查询
- 导出执行历史

---

## 📞 需要帮助？

如果验证发现问题，提供以下信息：
1. GitHub Actions执行日志
2. Supabase数据库查询结果
3. 飞书表格截图

我会帮你诊断问题！
