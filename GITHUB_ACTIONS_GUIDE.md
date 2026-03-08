# GitHub Actions 部署指南

## 🎯 方案优势

GitHub Actions是一个完美的替代方案！

| 特性 | 优势 |
|------|------|
| ✅ **完全免费** | 公开仓库免费使用 |
| ✅ **配置简单** | 只需配置Secrets和推送代码 |
| ✅ **自动执行** | 每小时整点自动运行 |
| ✅ **监控完善** | 查看执行历史和日志 |
| ✅ **无需服务器** | GitHub提供执行环境 |
| ✅ **24/7运行** | GitHub服务器永远在线 |

---

## 📋 部署步骤（10分钟）

### 步骤1：已完成的准备工作 ✅

以下文件已经创建：
- ✅ `.github/workflows/rss-sync.yml` - Actions配置文件
- ✅ `actions_run.py` - 执行脚本
- ✅ 代码已推送到GitHub

### 步骤2：创建飞书应用（5分钟）

1. **访问飞书开放平台**
   - https://open.feishu.cn/app

2. **创建应用**
   - 点击"创建企业自建应用"
   - 应用名称：`RSS同步机器人`
   - 点击"确定"

3. **获取凭证**
   - 进入应用详情页
   - 点击"凭证与基础信息"
   - 复制以下信息：
     - **App ID**：`cli_xxxxxxxxxxxxxx`
     - **App Secret**：点击"查看"，复制这个值

4. **配置权限**
   - 点击"权限管理"
   - 搜索并开通以下权限：
     - `bitable:app` - 获取和更新多维表格
   - 点击"申请权限"

5. **发布应用**
   - 点击右上角"发布"
   - 选择版本（如：1.0.0）
   - 点击"确定"

### 步骤3：配置GitHub Secrets（3分钟）

1. **访问GitHub仓库设置**
   - 访问：https://github.com/529654431/rss-feishu-sync
   - 点击"Settings"标签
   - 左侧菜单点击"Secrets and variables" → "Actions"

2. **添加7个Secrets**

点击"New repository secret"，逐个添加：

#### 3.1 添加 SUPABASE_URL
- Name: `SUPABASE_URL`
- Value: `https://xxx.supabase.co` （你的Supabase项目URL）
- 点击"Add secret"

#### 3.2 添加 SUPABASE_KEY
- Name: `SUPABASE_KEY`
- Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` （你的Supabase anon key）
- 点击"Add secret"

#### 3.3 添加 FEISHU_APP_TOKEN
- Name: `FEISHU_APP_TOKEN`
- Value: `KqLSb9eeqaOYstsryBMcCiJTnkc`
- 点击"Add secret"

#### 3.4 添加 FEISHU_TABLE_ID
- Name: `FEISHU_TABLE_ID`
- Value: `tbl6xkic4IuaOH6u`
- 点击"Add secret"

#### 3.5 添加 FEISHU_APP_ID
- Name: `FEISHU_APP_ID`
- Value: `cli_xxxxxxxxxxxxxx` （从飞书应用获取）
- 点击"Add secret"

#### 3.6 添加 FEISHU_APP_SECRET
- Name: `FEISHU_APP_SECRET`
- Value: `xxxxxxxxxxxxxx` （从飞书应用获取）
- 点击"Add secret"

#### 3.7 添加 RSS_URL（可选）
- Name: `RSS_URL`
- Value: `https://cn.investing.com/rss/news_285.rss`
- 点击"Add secret"

**所有Secrets添加完成后，你会看到7个条目。**

### 步骤4：推送Actions配置到GitHub（1分钟）

配置文件已经创建好了，需要推送到GitHub。

```bash
git add .github/workflows/rss-sync.yml actions_run.py
git commit -m "feat: 添加GitHub Actions自动执行配置"
git push origin main
```

或者直接在GitHub网页端：
- 访问：https://github.com/529654431/rss-feishu-sync
- 点击"Add file" → "Create new file"
- 文件名：`.github/workflows/rss-sync.yml`
- 粘贴yaml配置内容
- 点击"Commit changes"

重复创建 `actions_run.py` 文件。

### 步骤5：验证Actions配置（1分钟）

1. **查看Actions页面**
   - 访问：https://github.com/529654431/rss-feishu-sync/actions
   - 你会看到名为"RSS监测与飞书同步"的工作流

2. **手动触发测试**
   - 点击工作流
   - 找到"Run workflow"按钮
   - 选择分支：main
   - 点击"Run workflow"

3. **查看执行日志**
   - 等待1-2分钟
   - 点击执行记录查看详细日志
   - 确认显示：`✅ 任务执行成功！`

### 步骤6：验证飞书表格

1. **打开飞书多维表格**
2. **查看是否有新记录**
3. **验证内容是否正确**

---

## ⏰ 定时执行说明

### Cron表达式：`0 * * * *`
- `0` - 每小时的第0分钟（整点）
- `*` - 每小时
- `*` - 每天
- `*` - 每月
- `*` - 每周

### 执行时间（中国时区）
- 00:00, 01:00, 02:00, ..., 23:00
- 每小时整点自动执行一次

### 查看执行历史
1. 访问：https://github.com/529654431/rss-feishu-sync/actions
2. 查看每次执行的记录
3. 点击记录查看详细日志

---

## 📊 执行结果示例

成功执行的日志输出：

```
🎯 RSS监测与飞书同步 - GitHub Actions版

==================================================
🚀 开始RSS同步任务
⏰ 时间: 2026-03-08 23:00:00
==================================================
📡 正在获取RSS: https://cn.investing.com/rss/news_285.rss
✅ 成功获取 20 条RSS记录
🔍 查询已处理的链接...
✅ 已处理 10 条记录
🔍 发现 10 条新内容
🔑 获取飞书访问令牌...
✅ 成功获取飞书访问令牌
📝 开始写入飞书表格...
  [1/10] 处理: 伊朗战争:可能持续多久?摩根士丹利...
    ✅ 写入成功
  [2/10] 处理: 五大分析师AI观点:逢低买入三星...
    ✅ 写入成功
  ...
💾 记录已处理的链接...
==================================================
📊 执行结果:
  ✅ 成功: 10 条
  ❌ 失败: 0 条
  💾 记录: 10 条
==================================================

✅ 任务执行成功！
```

---

## 🔧 如何修改配置

### 修改RSS源
1. 修改GitHub Secret：`RSS_URL`
2. 或修改 `.github/workflows/rss-sync.yml` 中的 `RSS_URL` 值

### 修改执行时间
编辑 `.github/workflows/rss-sync.yml` 中的cron表达式：
```yaml
schedule:
  - cron: '0 * * * *'  # 每小时
  - cron: '0 */2 * * *'  # 每2小时
  - cron: '0 0 * * *'  # 每天0点
```

### 修改飞书表格
更新GitHub Secrets：
- `FEISHU_APP_TOKEN`
- `FEISHU_TABLE_ID`

---

## ❓ 常见问题

### Q1: Actions执行失败，提示"缺少环境变量"
**A**: 检查GitHub Secrets是否配置了所有7个变量

### Q2: 飞书写入失败
**A**:
- 检查飞书应用的App ID和App Secret是否正确
- 确认飞书应用已开通`bitable:app`权限
- 确认飞书应用已发布

### Q3: Supabase连接失败
**A**:
- 检查SUPABASE_URL和SUPABASE_KEY是否正确
- 确认Supabase项目中有`rss_tracking`表

### Q4: 定时任务不执行
**A**:
- 检查cron表达式是否正确：`0 * * * *`
- Actions默认使用UTC时区，需要调整
- 或手动触发测试

### Q5: 如何查看详细日志？
**A**:
- 访问Actions页面
- 点击执行记录
- 查看完整输出

### Q6: 如何停止自动执行？
**A**:
- 编辑 `.github/workflows/rss-sync.yml`
- 注释掉或删除 `schedule` 部分
- 保留 `workflow_dispatch` 以支持手动触发

---

## 🎉 完成！

恭喜你！现在GitHub Actions会：
- ✅ 每小时整点自动执行
- ✅ 监测RSS内容
- ✅ 过滤新内容
- ✅ 写入飞书表格
- ✅ 避免重复
- ✅ 完全免费
- ✅ 24/7运行

---

## 📞 技术支持

遇到问题？
1. 查看Actions执行日志
2. 检查GitHub Secrets配置
3. 参考本文档的"常见问题"部分

**GitHub Actions部署简单、稳定、免费！** 🚀
