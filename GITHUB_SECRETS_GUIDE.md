# 🔐 GitHub Secrets 配置指南

## 需要的Secrets

在GitHub仓库页面，转到：
**Settings** → **Secrets and variables** → **Actions**

添加以下Secrets：

---

### 1. XIAOHONGSHU_COOKIE（最重要！）

**获取方法**：
1. 在本地浏览器登录小红书
2. 按 F12 → Console
3. 输入：`console.log(document.cookie)`
4. 复制所有输出

**添加到GitHub**：
- Name: `XIAOHONGSHU_COOKIE`
- Value: 粘贴刚才复制的cookie字符串

**注意**：
- Cookies有效期约7-30天
- 过期后需要重新获取并更新
- 不要分享给他人

---

### 2. VOLCANO_API_KEY（火山引擎API密钥）

**获取方法**：
1. 访问：https://www.volcengine.com/
2. 登录账号
3. 进入"火山引擎" → "开发者控制台"
4. 创建API Key

**添加到GitHub**：
- Name: `VOLCANO_API_KEY`
- Value: 您的API Key

---

### 3. VOLCANO_API_SECRET（火山引擎API密钥）

**添加到GitHub**：
- Name: `VOLCANO_API_SECRET`
- Value: 您的API Secret

---

## 添加步骤（图文）

1. 打开GitHub仓库：https://github.com/amirbebebebe/pettes

2. 点击 **Settings** 标签

3. 左侧菜单找到 **Secrets and variables** → **Actions**

4. 点击 **New repository secret**

5. 填写：
   - Name: `XIAOHONGSHU_COOKIE`
   - Value: [粘贴cookies]

6. 点击 **Add secret**

7. 重复步骤4-6，添加其他secrets

---

## 验证配置

添加完secrets后，可以手动触发workflow测试：

1. 进入 **Actions** 标签
2. 选择 "小红书宠物内容自动化（直接发布版）"
3. 点击 **Run workflow**
4. 选择 "test_mode: true"（只测试生成，不发布）
5. 点击 **Run workflow**

如果成功，说明配置正确！

---

## ⚠️ 重要提醒

1. **XIAOHONGSHU_COOKIE必须有效**，否则发布会失败
2. 定期检查cookies是否过期
3. 不要泄露secrets给他人
4. 测试模式不会实际发布，适合验证流程

---

## 下一步

配置完成后，告诉我，我帮您：
1. 推送代码到GitHub
2. 手动触发第一次测试
