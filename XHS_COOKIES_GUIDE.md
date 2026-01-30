# 🐱 小红书 Cookies 获取工具

## 问题说明

服务器上的ChromeDriver与浏览器版本不兼容，导致无法自动登录。
本工具提供**手动获取cookies**的替代方案。

---

## 📱 第一步：在本地浏览器登录小红书

### 1. 打开小红书网页版
访问：https://www.xiaohongshu.com/

### 2. 登录账号
使用手机号 **13810119101** 登录

### 3. 打开开发者工具
- **Chrome/Edge**: 按 `F12` 或 `Ctrl+Shift+I`
- **Firefox**: 按 `F12`

### 4. 获取Cookies

#### 方法一：简单复制（推荐）

1. 在开发者工具中，切换到 **Application（应用程序）** 标签
2. 左侧菜单展开 **Cookies** → 点击 **https://www.xiaohongshu.com**
3. 在右侧表格中找到以下关键cookie：
   - `web_session`
   - `a1`
   - `webid`
   - `xhs_tracker_id`
   - `tube_scene`

4. **复制完整cookie字符串**：
   - 点击任意cookie值区域
   - 按 `Ctrl+A` 全选
   - 按 `Ctrl+C` 复制

#### 方法二：控制台命令

1. 在 **Console（控制台）** 标签输入：
```javascript
console.log(document.cookie)
```

2. 复制输出的所有内容

---

## 📤 第二步：保存Cookies

### 方式1：保存为文件

将复制的内容保存到文件：
```
C:\Users\Gigabyte\.minimax-agent-cn\projects\1\media-automation\data\xhs_cookies.txt
```

### 方式2：直接配置到服务器

```bash
# 登录服务器
ssh root@43.129.244.154

# 编辑环境变量文件
vi /opt/xhs-automation/.env

# 将 cookies 添加到 XIAOHONGSHU_COOKIE= 后面
```

---

## 🔧 第三步：上传到服务器

运行以下命令上传cookies：

```bash
# 在本地项目目录执行
cd C:\Users\Gigabyte\.minimax-agent-cn\projects\1\media-automation

# 方式A：使用scp（需要安装OpenSSH）
scp data\xhs_cookies.txt root@43.129.244.154:/opt/xhs-automation/data/

# 方式B：手动复制内容，粘贴到服务器文件
```

---

## ✅ 验证登录状态

登录服务器检查：

```bash
ssh root@43.129.244.154
cd /opt/xhs-automation
python3 -c "from scripts.xhs_cookies import XhsCookies; print(XhsCookies.load())"
```

---

## ⚠️ 注意事项

1. **Cookies有效期**：小红书cookies通常在7-30天后过期，需要重新获取
2. **不要退出登录**：保持登录状态可以延长cookies有效期
3. **多设备登录**：在小红书APP中检查是否允许web端登录
4. **安全提示**：不要分享您的cookies给他人

---

## 🔧 替代方案：使用Playwright（需要时启用）

如果上述方法失败，可以尝试安装Playwright：

```bash
# 在服务器上
pip install playwright
playwright install chromium
```

然后修改 `scripts/xhs_mcp_client.py` 使用Playwright浏览器。
