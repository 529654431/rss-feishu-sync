# RSS监测与飞书同步工作流

## 项目简介

每小时整点监测指定RSS链接，自动将新内容写入飞书多维表格，避免重复处理。

## 功能特性

- ✅ RSS内容自动解析
- ✅ 智能过滤新内容（基于数据库去重）
- ✅ 自动同步到飞书多维表格
- ✅ 定时执行（每小时整点）
- ✅ 支持重试机制
- ✅ 完整的错误处理

## 快速开始

### 1. 本地测试

#### 测试完整工作流
```bash
bash scripts/local_run.sh -m flow
```

输入参数示例：
```json
{
  "rss_url": "https://cn.investing.com/rss/news_285.rss",
  "app_token": "KqLSb9eeqaOYstsryBMcCiJTnkc",
  "table_id": "tbl6xkic4IuaOH6u"
}
```

#### 测试单个节点
```bash
bash scripts/local_run.sh -m node -n node_name
```

### 2. 启动HTTP服务

```bash
bash scripts/http_run.sh -m http -p 5000
```

服务将在 http://localhost:5000 启动。

### 3. 定时任务配置

工作流已配置为每小时整点自动执行（Cron表达式：`0 * * * *`）。

**定时配置说明：**
- 执行时间：每小时的第0分钟（整点）
- 时区：Asia/Shanghai（中国时区）
- 重试策略：失败后最多重试3次，每次间隔60秒
- 超时时间：15分钟

如需修改定时配置，请编辑 `workflow.yaml` 文件中的 `triggers` 部分。

## 数据库表结构

### rss_tracking 表
用于跟踪已处理的RSS条目，避免重复处理。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 主键 |
| link | text | RSS条目链接（唯一） |
| title | text | RSS条目标题 |
| processed_at | timestamp | 处理时间 |
| created_at | timestamp | 创建时间 |

## 工作流程

```
读取RSS → 过滤新内容 → 是否有新内容？
                              ↓
                    是 → 循环写入飞书表格
                              ↓
                    否 → 准备空列表
                              ↓
                    记录已处理内容 → 结束
```

## 飞书表格字段

每条RSS条目会写入以下字段：

- **标题** (text): RSS条目标题
- **链接** (text): RSS条目链接
- **发布时间** (text): 发布时间
- **描述** (text): 内容描述

## 环境要求

- Python 3.12
- 依赖包见 `requirements.txt`

## 依赖包

- feedparser: RSS解析
- coze-coding-dev-sdk: 飞书集成
- supabase: 数据库集成
- langgraph: 工作流编排
- pydantic: 数据验证

## 监控与告警

- 执行失败时自动触发告警
- 超时（15分钟）自动触发告警
- 支持查看执行日志

## 故障排查

### 工作流执行失败
1. 检查日志文件：`/app/work/logs/bypass/app.log`
2. 验证RSS链接是否可访问
3. 确认飞书多维表格权限配置正确
4. 检查数据库连接状态

### 新内容未写入飞书
1. 检查 `rss_tracking` 表中是否已存在该链接
2. 验证飞书表格字段名称是否正确
3. 确认飞书API权限

## 技术支持

详细技术文档请查看 `AGENTS.md`

