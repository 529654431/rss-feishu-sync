# GitHub部署快速指南

## 步骤1：在GitHub上创建仓库（2分钟）

### 操作步骤：
1. **访问GitHub**：https://github.com/new
2. **填写仓库信息**：
   - Repository name: `rss-feishu-sync`
   - Description: `RSS监测与飞书同步工作流`
   - Public/Private: 任选
   - ⚠️ **不要勾选** "Add a README file"
   - ⚠️ **不要勾选** "Add .gitignore"
   - ⚠️ **不要勾选** "Choose a license"
3. 点击 **"Create repository"** 按钮

### 创建成功后，GitHub会显示你的仓库地址：
```
https://github.com/529654431/rss-feishu-sync.git
```

---

## 步骤2：创建Personal Access Token（3分钟）

### 为什么需要Token？
GitHub已不再支持密码认证，必须使用Token。

### 操作步骤：
1. **访问Token创建页面**：
   - https://github.com/settings/tokens/new

2. **配置Token**：
   - Note: `Coze Deploy Token`（或任意名称）
   - Expiration: `90 days` 或 `No expiration`
   - 勾选权限：
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)

3. 点击 **"Generate token"** 按钮

4. **复制Token**（只显示一次！务必保存）：
   ```
   ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   - ⚠️ **立即复制并保存**，刷新页面就看不到了
   - 这个Token相当于你的GitHub密码

---

## 步骤3：推送代码到GitHub（1分钟）

### 方法A：使用命令行推送（推荐）

如果你已经准备好了GitHub Token，执行以下命令：

```bash
# 1. 添加远程仓库（如果还没有）
git remote add origin https://github.com/529654431/rss-feishu-sync.git

# 2. 推送代码（使用Token替代密码）
git push -u origin main
# 提示输入Username时，输入：529654431
# 提示输入Password时，粘贴你的GitHub Token
```

### 方法B：使用Token直接推送

```bash
# 使用Token直接推送（将YOUR_TOKEN替换为你的Token）
git push https://YOUR_TOKEN@github.com/529654431/rss-feishu-sync.git main
```

---

## 步骤4：验证推送成功

推送成功后，访问：
```
https://github.com/529654431/rss-feishu-sync
```

你应该能看到：
- ✅ 所有项目文件
- ✅ 5次提交记录
- ✅ README.md文档

---

## 常见问题

### Q1: 推送失败提示"Authentication failed"
**A**: 检查以下几点：
- Token是否正确（ghp_xxx格式）
- Token是否有`repo`权限
- Username是否正确（529654431）

### Q2: 提示"Repository does not exist"
**A**: 确认你已经按照步骤1在GitHub上创建了仓库

### Q3: Token忘记了怎么办
**A**: Token只显示一次，需要重新创建：
- 访问：https://github.com/settings/tokens
- 删除旧Token，创建新Token

### Q4: 推送时提示"Updates were rejected"
**A**: 使用强制推送（谨慎使用）：
```bash
git push -f origin main
```

---

## 下一步：在Coze平台导入

推送成功后，进入Coze平台导入工作流：

1. 登录 https://www.coze.cn/
2. 进入"工作流" → "新建工作流"
3. 选择"从Git仓库导入"
4. 输入仓库地址：`https://github.com/529654431/rss-feishu-sync.git`
5. 点击"导入"

---

## ⚠️ 安全提示

- 🔒 **不要泄露你的Token**：Token相当于密码
- 💾 **妥善保存Token**：建议使用密码管理器
- 🔄 **定期更新Token**：90天后建议更新

---

**准备好后，告诉我你已完成哪些步骤，我来协助你继续！** 🚀
