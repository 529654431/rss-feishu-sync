## 项目概述
- **名称**: RSS监测与飞书同步工作流
- **功能**: 每小时监测指定RSS链接，将新内容自动写入飞书多维表格

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| fetch_rss | `nodes/fetch_rss_node.py` | task | 读取RSS内容 | - | - |
| filter_new_items | `nodes/filter_new_items_node.py` | task | 过滤出新内容 | - | - |
| process_new_items | `nodes/process_new_items_node.py` | looparray | 调用子图处理新内容 | - | - |
| prepare_empty_list | `graph.py` | task | 准备空列表（无新内容时） | - | - |
| record_processed | `nodes/record_processed_node.py` | task | 记录已处理内容 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
| 子图名 | 文件位置 | 功能描述 | 被调用节点 |
|-------|---------|------|---------|-----------|
| subgraph | `graphs/loop_graph.py` | 循环写入飞书表格 | process_new_items |

### 子图节点清单
| 节点名 | 类型 | 功能描述 |
|-------|------|---------|
| write_to_feishu | task | 将单个RSS条目写入飞书多维表格 |
| should_continue_loop | condition | 判断是否继续循环 |

## 技能使用
- 节点`filter_new_items`使用Supabase技能（查询已处理记录）
- 节点`record_processed`使用Supabase技能（记录已处理内容）
- 节点`process_new_items`调用飞书多维表格技能（写入飞书表格）
- 子图节点`write_to_feishu`使用飞书多维表格技能

## 飞书表格字段映射
- **聊天记录** (Text): 存储RSS标题
- **消息链接** (URL): 存储RSS链接（对象格式：`{"link": "url"}`）
- **时间** (Text): 存储RSS发布时间
- **发送日期** (Text): 存储RSS描述信息（原计划使用"发送人"字段，因其为Person类型不可直接传字符串，故改用"发送日期"）

## 数据库表结构
- **rss_tracking**: 用于跟踪已处理的RSS条目
  - id: 主键
  - link: RSS条目链接（唯一）
  - title: RSS条目标题
  - processed_at: 处理时间
  - created_at: 创建时间

## 依赖包
- feedparser: RSS解析
- coze-coding-dev-sdk: 飞书集成
- supabase: 数据库集成
