# Coze平台工作流部署指南

## 前置准备

### 1. 确保你有以下信息
- ✅ Coze平台账号（https://www.coze.cn/）
- ✅ Supabase项目URL和Key
- ✅ 飞书多维表格的app_token和table_id

### 2. 确认项目文件完整
当前项目应包含以下关键文件：
```
✅ src/graphs/graph.py       # 主图
✅ src/graphs/loop_graph.py  # 子图
✅ src/graphs/state.py       # 状态定义
✅ workflow.yaml             # 工作流配置
✅ .coze                     # 部署配置
```

---

## 方法1：通过Git仓库导入（推荐）

### 步骤1：推送到Git仓库
```bash
# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "feat: RSS监测与飞书同步工作流"

# 推送到GitHub/Gitee等平台
git remote add origin https://github.com/your-username/rss-feishu-sync.git
git branch -M main
git push -u origin main
```

### 步骤2：在Coze平台导入
1. **登录Coze平台**
   - 访问：https://www.coze.cn/
   - 使用手机号/邮箱登录

2. **进入工作流管理**
   - 点击左侧菜单的"工作流"或"自动化"
   - 点击"新建工作流"

3. **选择导入方式**
   - 选择"从Git仓库导入"
   - 输入你的Git仓库地址：`https://github.com/your-username/rss-feishu-sync.git`
   - 选择分支：`main`
   - 点击"导入"

4. **确认工作流信息**
   - 工作流名称：RSS监测与飞书同步
   - 描述：每小时整点监测RSS链接，将新内容自动写入飞书多维表格
   - 点击"确认创建"

---

## 方法2：手动上传文件

### 步骤1：打包项目
```bash
# 创建部署包
zip -r rss-feishu-sync.zip . -x "*.pyc" "__pycache__/*" ".git/*"
```

### 步骤2：在Coze平台上传
1. 登录Coze平台
2. 进入"工作流" → "新建工作流"
3. 选择"上传文件"或"创建空白工作流"
4. 如果是空白工作流，手动创建以下文件：
   - `src/graphs/graph.py`
   - `src/graphs/loop_graph.py`
   - `src/graphs/state.py`
   - `workflow.yaml`

---

## 部署后配置

### 1. 配置环境变量

在工作流设置中，添加以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `SUPABASE_URL` | `https://xxx.supabase.co` | Supabase项目URL |
| `SUPABASE_KEY` | `your_supabase_key` | Supabase API Key |
| `COZE_WORKSPACE_PATH` | `/workspace` | 工作目录 |

**获取方式：**
- Supabase：登录 https://supabase.com/ → 进入项目 → Settings → API
- 飞书凭证已在 `workflow.yaml` 中配置，无需额外设置

### 2. 配置定时触发器

1. 进入工作流的"触发器"设置
2. 确认以下配置：
   ```yaml
   类型: Cron
   Cron表达式: 0 * * * *
   时区: Asia/Shanghai
   状态: 已启用
   ```
3. 检查输入参数：
   ```json
   {
     "rss_url": "https://cn.investing.com/rss/news_285.rss",
     "app_token": "KqLSb9eeqaOYstsryBMcCiJTnkc",
     "table_id": "tbl6xkic4IuaOH6u"
   }
   ```
4. 点击"保存"

### 3. 首次测试

**重要：在激活定时任务前，先手动测试一次**

1. 在工作流页面，找到"运行"或"测试"按钮
2. 点击运行，查看执行日志
3. 检查飞书表格，确认是否有新记录写入
4. 如果成功，再激活定时任务

---

## 验证部署

### 1. 检查执行历史
- 在Coze平台查看"执行历史"或"日志"
- 确认工作流是否正常运行

### 2. 检查飞书表格
- 打开飞书多维表格
- 查看是否有新的RSS记录
- 字段应包含：
  - **聊天记录**：标题
  - **消息链接**：链接
  - **时间**：发布时间
  - **发送日期**：描述

### 3. 检查数据库
```sql
-- 查看已处理的记录数
SELECT COUNT(*) FROM rss_tracking;

-- 查看最近10条记录
SELECT * FROM rss_tracking ORDER BY processed_at DESC LIMIT 10;
```

### 4. 验证定时执行
- 等待下一个整点（如23:00）
- 观察工作流是否自动执行
- 检查执行日志和飞书表格更新

---

## 常见问题

### Q1: 导入后显示"找不到入口文件"
**A:** 检查 `.coze` 文件中的 `entrypoint` 是否正确：
```toml
[project]
entrypoint = "src/main.py"
requires = ["python-3.12"]
```

### Q2: 定时任务不执行
**A:** 确认以下事项：
- 触发器状态是否为"已启用"
- Cron表达式是否正确：`0 * * * *`
- 时区是否设置为：`Asia/Shanghai`
- 环境变量是否配置完整

### Q3: 飞书表格写入失败
**A:** 检查：
- `app_token` 和 `table_id` 是否正确
- 飞书多维表格是否有写入权限
- 表格字段名称是否匹配：
  - ✅ 聊天记录（Text）
  - ✅ 消息链接（URL）
  - ✅ 时间（Text）
  - ✅ 发送日期（Text）

### Q4: 数据库连接失败
**A:** 检查环境变量：
- `SUPABASE_URL` 格式是否正确
- `SUPABASE_KEY` 是否有效
- Supabase项目是否创建了 `rss_tracking` 表

---

## 监控与告警

### 查看执行日志
- 进入工作流详情
- 点击"日志"或"执行历史"
- 查看每次执行的详细输出

### 配置告警
根据 `workflow.yaml` 中的配置：
- 执行失败会自动触发告警
- 超时（15分钟）会自动触发告警
- 可以在Coze平台通知设置中接收告警

---

## 后续维护

### 修改定时频率
编辑 `workflow.yaml` 中的 `cron` 表达式：
```yaml
cron: "0 * * * *"  # 每小时
cron: "0 */2 * * *"  # 每2小时
cron: "0 0 * * *"  # 每天0点
```

### 修改RSS源
编辑 `workflow.yaml` 中的 `input` 参数：
```yaml
input:
  rss_url: "https://your-new-rss-url.com/feed"
```

### 修改飞书表格
更新 `workflow.yaml` 中的飞书凭证：
```yaml
input:
  app_token: "your_new_app_token"
  table_id: "your_new_table_id"
```

---

## 联系支持

如遇到问题：
1. 查看 `/app/work/logs/bypass/app.log` 日志文件
2. 检查Coze平台执行日志
3. 参考本文档的"常见问题"部分

---

**部署完成后，你的工作流将在云端24/7运行，每小时自动监测RSS并同步到飞书表格！** 🎉
