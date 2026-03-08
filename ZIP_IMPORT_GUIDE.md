# 新版Coze - ZIP文件导入指南

## ✅ 部署包已准备完成

**文件信息**：
- 📦 文件名：`rss-feishu-sync.zip`
- 📏 大小：69KB
- 📂 包含：完整的工作流代码、配置、文档

---

## 🚀 导入步骤（5分钟）

### 步骤1：下载ZIP文件

如果你能直接访问工作目录，文件就在项目根目录：
```
rss-feishu-sync.zip
```

或者从GitHub下载：
1. 访问：https://github.com/529654431/rss-feishu-sync
2. 点击"Code" → "Download ZIP"

### 步骤2：登录Coze平台

1. **访问Coze**：https://www.coze.cn/
2. **登录账号**

### 步骤3：创建工作流

1. **进入工作流页面**
   - 点击左侧"工作流"或"Workflow"
   - 或直接访问：https://www.coze.cn/workflow

2. **创建新工作流**
   - 点击"新建工作流"按钮
   - 选择"导入ZIP文件"或"上传文件"

3. **上传ZIP文件**
   - 点击"选择文件"或拖拽上传
   - 选择 `rss-feishu-sync.zip`
   - 点击"导入"

### 步骤4：等待导入完成

- 导入过程约1-2分钟
- 系统会自动：
  - 解压文件
  - 识别工作流结构
  - 安装依赖包
  - 初始化配置

---

## 🔧 步骤5：配置环境变量

导入完成后，需要配置环境变量：

1. **进入工作流设置**
   - 点击刚导入的工作流
   - 找到"设置"或"环境变量"页面

2. **添加环境变量**

在环境变量区域，添加以下变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `SUPABASE_URL` | `https://xxx.supabase.co` | 你的Supabase项目URL |
| `SUPABASE_KEY` | `your_supabase_key` | 你的Supabase API Key |
| `COZE_WORKSPACE_PATH` | `/workspace` | 固定值，保持不变 |

### 如何获取Supabase凭证？

1. **登录Supabase**
   - 访问：https://supabase.com/
   - 进入你的项目

2. **获取URL和Key**
   - 点击左侧"Settings" → "API"
   - 复制：
     - **Project URL**: `https://xxx.supabase.co`
     - **anon/public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

3. **填写到环境变量**

---

## ⚙️ 步骤6：检查工作流配置

1. **查看工作流结构**
   - 确认入口文件：`src/main.py`
   - 确认节点数量：4个
   - 确认循环子图存在

2. **检查定时任务配置**
   - 找到"触发器"或"Triggers"设置
   - 确认配置：
     ```yaml
     类型: Cron
     Cron表达式: 0 * * * *
     时区: Asia/Shanghai
     输入参数:
       rss_url: https://cn.investing.com/rss/news_285.rss
       app_token: KqLSb9eeqaOYstsryBMcCiJTnkc
       table_id: tbl6xkic4IuaOH6u
     ```

---

## 🧪 步骤7：手动测试（重要！）

**在激活定时任务前，必须先手动测试！**

1. **进入测试页面**
   - 在工作流页面，点击"运行"或"测试"

2. **输入测试参数**
   - 可以使用默认参数
   - 或自定义：
     ```json
     {
       "rss_url": "https://cn.investing.com/rss/news_285.rss",
       "app_token": "KqLSb9eeqaOYstsryBMcCiJTnkc",
       "table_id": "tbl6xkic4IuaOH6u"
     }
     ```

3. **点击"运行"**

4. **检查结果**
   - 查看执行日志
   - 确认返回：`{"processed_count": 10, ...}`
   - 打开飞书表格，查看是否有新记录

5. **验证成功标志**
   - ✅ 无错误信息
   - ✅ processed_count > 0
   - ✅ 飞书表格有新记录

---

## ✅ 步骤8：激活定时任务

1. **确保手动测试成功**
   - 只有测试通过了才能激活定时任务

2. **启用触发器**
   - 在触发器设置中
   - 将状态改为"已启用"或点击"启用"按钮

3. **确认配置**
   - Cron: `0 * * * *`（每小时整点）
   - 时区: `Asia/Shanghai`
   - 下次执行时间：显示下一个整点

---

## 📊 步骤9：验证自动运行

1. **等待下一个整点**
   - 例如现在22:40，等到23:00

2. **查看执行历史**
   - 在Coze平台，工作流详情页面
   - 查看"执行历史"或"日志"
   - 确认有自动执行记录

3. **检查飞书表格**
   - 查看是否有新记录自动写入
   - 验证时间戳是否正确

---

## 🎉 完成！

恭喜你！工作流现在会：
- ✅ 每小时整点自动监测RSS
- ✅ 自动过滤新内容
- ✅ 自动写入飞书表格
- ✅ 避免重复写入

---

## 📦 ZIP文件内容清单

```
rss-feishu-sync.zip
├── src/                          # 源代码目录
│   ├── main.py                   # 程序入口
│   ├── graphs/                   # 工作流编排
│   │   ├── graph.py              # 主图
│   │   ├── loop_graph.py         # 循环子图
│   │   ├── state.py              # 状态定义
│   │   └── nodes/                # 节点实现
│   │       ├── fetch_rss_node.py
│   │       ├── filter_new_items_node.py
│   │       ├── process_new_items_node.py
│   │       └── record_processed_node.py
│   ├── storage/                  # 数据存储
│   │   └── database/
│   │       ├── supabase_client.py
│   │       └── shared/model.py
│   └── utils/                    # 工具函数
│       └── file/
├── .coze                         # Coze部署配置
├── requirements.txt              # Python依赖包
├── workflow.yaml                 # 工作流配置
├── AGENTS.md                     # 技术文档
└── README.md                     # 使用说明
```

---

## ❓ 常见问题

### Q1: 导入失败，提示"无效的ZIP文件"
**A**:
- 检查ZIP文件是否完整下载
- 确保文件名是 `rss-feishu-sync.zip`
- 尝试重新下载

### Q2: 导入成功但找不到入口文件
**A**:
- 检查 `.coze` 文件是否包含
- 确认 entrypoint 为 `src/main.py`

### Q3: 运行时提示"找不到模块"
**A**:
- 确认依赖包已自动安装
- 检查环境变量配置是否完整

### Q4: Supabase连接失败
**A**:
- 检查 `SUPABASE_URL` 和 `SUPABASE_KEY` 是否正确
- 确认Supabase项目中的 `rss_tracking` 表已创建

### Q5: 飞书表格写入失败
**A**:
- 检查 `app_token` 和 `table_id` 是否正确
- 确认飞书表格有写入权限
- 查看执行日志获取详细错误

### Q6: 定时任务不执行
**A**:
- 确认触发器状态为"已启用"
- 检查Cron表达式：`0 * * * *`
- 检查时区设置：`Asia/Shanghai`

---

## 📞 技术支持

如遇到问题：
1. 查看Coze平台执行日志
2. 检查环境变量配置
3. 参考本文档的"常见问题"部分

---

**现在可以开始导入ZIP文件了！** 🚀

导入完成后，告诉我结果，我来协助你完成后续配置！
