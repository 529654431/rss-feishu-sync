# Coze可视化编排指南 - RSS监测与飞书同步

## 🎯 工作流结构总览

我们的工作流包含4个主要节点，逻辑如下：

```
开始
  ↓
【节点1：读取RSS】
  ↓
【节点2：过滤新内容】
  ↓
【节点3：循环写入飞书】→ 调用子图循环处理
  ↓
【节点4：记录已处理】
  ↓
结束
```

---

## 🚀 步骤1：创建空白工作流

1. **登录Coze平台**：https://www.coze.cn/
2. **进入工作流页面**
3. **点击"新建工作流"**
4. **选择"空白工作流"**
5. **填写信息**：
   - 名称：RSS监测与飞书同步
   - 描述：每小时整点监测RSS，自动写入飞书表格
6. **点击"创建"**

---

## 🔧 步骤2：配置输入参数

在工作流设置中，添加输入参数：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `rss_url` | String | RSS链接地址 |
| `app_token` | String | 飞书多维表格app_token |
| `table_id` | String | 飞书多维表格table_id |

---

## 📦 步骤3：创建节点1 - 读取RSS

### 节点信息
- **节点名称**：读取RSS
- **节点类型**：代码节点 或 HTTP请求节点
- **功能**：获取RSS内容并解析

### 节点配置

**如果是代码节点**，添加以下Python代码：

```python
import feedparser
from datetime import datetime

def fetch_rss(rss_url):
    # 读取RSS内容
    feed = feedparser.parse(rss_url)
    
    # 提取所有条目
    items = []
    for entry in feed.entries:
        item = {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "description": entry.get("description", "")
        }
        items.append(item)
    
    return {
        "success": True,
        "items": items,
        "count": len(items)
    }

# 调用函数
result = fetch_rss(inputs.rss_url)
return result
```

**如果是HTTP请求节点**：
- 方法：GET
- URL：`{{inputs.rss_url}}`
- 配置自动解析RSS

### 输入参数
- `rss_url`：来自工作流输入

### 输出参数
- `items`：RSS条目列表
- `count`：条目数量

---

## 🔍 步骤4：创建节点2 - 过滤新内容

### 节点信息
- **节点名称**：过滤新内容
- **节点类型**：代码节点
- **功能**：查询数据库，过滤出未处理的条目

### 节点配置

```python
import requests

def filter_new_items(items, supabase_url, supabase_key):
    # 查询数据库中已处理的链接
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    
    # 获取已处理的链接列表
    response = requests.get(
        f"{supabase_url}/rest/v1/rss_tracking?select=link",
        headers=headers
    )
    
    if response.status_code == 200:
        processed_links = {item["link"] for item in response.json()}
    else:
        processed_links = set()
    
    # 过滤新内容
    new_items = []
    for item in items:
        if item["link"] not in processed_links:
            new_items.append(item)
    
    return {
        "success": True,
        "new_items": new_items,
        "new_count": len(new_items)
    }

# 调用函数
result = filter_new_items(
    节点1.items,
    env.SUPABASE_URL,
    env.SUPABASE_KEY
)
return result
```

### 输入参数
- `items`：来自节点1的输出
- `env.SUPABASE_URL`：环境变量
- `env.SUPABASE_KEY`：环境变量

### 输出参数
- `new_items`：新条目列表
- `new_count`：新条目数量

---

## 🔄 步骤5：创建节点3 - 循环写入飞书

### 节点信息
- **节点名称**：写入飞书
- **节点类型**：循环节点 或 调用子图
- **功能**：循环遍历新条目，逐条写入飞书

### 节点配置

**选项A：使用循环节点**

```python
import requests
from typing import List, Dict

def write_to_feishu(item, app_token, table_id):
    # 飞书API配置
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {
        "Authorization": "Bearer {{飞书访问令牌}}",  # 需要配置
        "Content-Type": "application/json"
    }
    
    # 构建记录
    record = {
        "fields": {
            "聊天记录": item["title"],
            "消息链接": {"link": item["link"]},
            "时间": item["published"],
            "发送日期": item["description"]
        }
    }
    
    # 写入飞书
    response = requests.post(url, headers=headers, json={"records": [record]})
    
    return response.status_code == 200

# 循环处理
success_count = 0
failed_count = 0

for item in 节点2.new_items:
    if write_to_feishu(item, inputs.app_token, inputs.table_id):
        success_count += 1
    else:
        failed_count += 1

return {
    "success": True,
    "success_count": success_count,
    "failed_count": failed_count
}
```

**选项B：调用子图（如果支持）**

1. 创建子图"写入单条记录"
2. 在循环中调用子图
3. 传入单条记录参数

### 输入参数
- `new_items`：来自节点2的输出
- `app_token`：来自工作流输入
- `table_id`：来自工作流输入

### 输出参数
- `success_count`：成功写入数量
- `failed_count`：失败数量

---

## 💾 步骤6：创建节点4 - 记录已处理

### 节点信息
- **节点名称**：记录已处理
- **节点类型**：代码节点
- **功能**：将已处理的链接保存到数据库

### 节点配置

```python
import requests
from datetime import datetime

def record_processed(items, supabase_url, supabase_key):
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json"
    }
    
    success_count = 0
    
    for item in items:
        data = {
            "link": item["link"],
            "title": item["title"],
            "processed_at": datetime.now().isoformat()
        }
        
        response = requests.post(
            f"{supabase_url}/rest/v1/rss_tracking",
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            success_count += 1
    
    return {
        "success": True,
        "recorded_count": success_count
    }

# 调用函数
result = record_processed(
    节点2.new_items,
    env.SUPABASE_URL,
    env.SUPABASE_KEY
)
return result
```

### 输入参数
- `new_items`：来自节点2的输出
- `env.SUPABASE_URL`：环境变量
- `env.SUPABASE_KEY`：环境变量

### 输出参数
- `recorded_count`：记录数量

---

## 🔗 步骤7：连接节点

按以下顺序连接节点：

```
开始 → 节点1(读取RSS) → 节点2(过滤新内容) → 节点3(写入飞书) → 节点4(记录已处理) → 结束
```

---

## 🎨 步骤8：配置输出参数

在工作流设置中，配置输出参数：

| 参数名 | 来源 |
|--------|------|
| `result_message` | `"成功处理{{节点3.success_count}}条记录"` |
| `processed_count` | 节点3.success_count |

---

## ⚙️ 步骤9：配置环境变量

在工作流设置中，添加环境变量：

| 变量名 | 值 |
|--------|-----|
| `SUPABASE_URL` | `https://xxx.supabase.co` |
| `SUPABASE_KEY` | `your_supabase_key` |

### 获取Supabase凭证

1. 登录：https://supabase.com/
2. 进入项目 → Settings → API
3. 复制：
   - Project URL
   - anon/public key

---

## 🧪 步骤10：手动测试

1. **点击"测试"或"运行"**
2. **输入测试参数**：
   ```json
   {
     "rss_url": "https://cn.investing.com/rss/news_285.rss",
     "app_token": "KqLSb9eeqaOYstsryBMcCiJTnkc",
     "table_id": "tbl6xkic4IuaOH6u"
   }
   ```
3. **点击"执行"**
4. **检查结果**：
   - processed_count > 0
   - 无错误信息
5. **验证飞书表格**：
   - 查看是否有新记录

---

## ⏰ 步骤11：配置定时任务

1. **找到"触发器"或"Cron"设置**
2. **添加定时触发器**：
   - 类型：Cron
   - 表达式：`0 * * * *`
   - 时区：Asia/Shanghai
   - 输入参数：使用测试参数
3. **点击"启用"**

---

## ✅ 步骤12：完成

工作流已配置完成，将：
- ✅ 每小时整点自动执行
- ✅ 监测RSS内容
- ✅ 写入飞书表格
- ✅ 避免重复

---

## 🔧 需要额外配置

### 飞书访问令牌

节点3中需要飞书访问令牌（Authorization），你需要：

1. **创建飞书应用**：https://open.feishu.cn/app
2. **获取凭证**：
   - App ID
   - App Secret
3. **配置权限**：
   - bitable:app（多维表格权限）
4. **获取访问令牌**：
   ```python
   import requests
   
   response = requests.post(
       "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
       json={
           "app_id": "你的App ID",
           "app_secret": "你的App Secret"
       }
   )
   
   token = response.json()["app_access_token"]
   ```

---

## ❓ 常见问题

### Q1: 找不到代码节点
**A**: 查找类似"代码编辑"、"Python节点"、"函数节点"的选项

### Q2: 节点连接失败
**A**: 确保节点之间的输入输出参数匹配

### Q3: 飞书写入失败
**A**: 
- 检查飞书访问令牌是否有效
- 确认app_token和table_id正确
- 验证飞书表格权限

### Q4: 数据库连接失败
**A**:
- 检查环境变量配置
- 确认Supabase项目中有`rss_tracking`表

---

## 📞 需要帮助？

**如果在可视化编排中遇到问题，告诉我：**
1. 当前进行到哪个步骤
2. 遇到的具体问题或错误
3. 界面上显示的选项

**我会根据你的反馈调整指导！** 🚀
