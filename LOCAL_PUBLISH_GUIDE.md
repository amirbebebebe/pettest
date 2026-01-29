# 🐱 本地发布指南

## 📋 概述

GitHub Actions 每天自动生成内容并保存到仓库，但发布需要在**本地环境**执行，因为：
- 小红书MCP (`xhs-mcp-server`) 需要浏览器环境
- 需要扫码登录确认

---

## 🚀 本地发布步骤

### 步骤1：安装依赖

```bash
cd media-automation
pip install -r requirements.txt
```

### 步骤2：安装ChromeDriver

```bash
npx @puppeteer/browsers install chromedriver@latest
```

### 步骤3：安装xhs-mcp-server

```bash
pip install xhs-mcp-server
```

### 步骤4：登录小红书（一次性）

```bash
env phone=13810119101 python -m xhs_mcp_server.__login__
```

1. 终端会显示二维码
2. 用小红书APP扫描
3. 在APP中确认登录

### 步骤5：执行发布

#### 发布到小红书

```bash
python scripts/publisher.py --platform xiaohongshu --local
```

#### 发布到公众号

```bash
python scripts/publisher.py --platform wechat --auto-publish
```

#### 同时发布到两个平台

```bash
python scripts/publisher.py --platform all --local --auto-publish
```

---

## 📖 发布命令说明

```bash
python scripts/publisher.py [OPTIONS]
```

### 参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--platform` | 发布平台 | `all` |
| | `xiaohongshu` - 仅小红书 | |
| | `wechat` - 仅公众号 | |
| | `all` - 两个平台都发 | |
| `--content` | 指定内容文件路径 | 自动查找今日内容 |
| `--local` | 使用本地MCP发布（小红书） | 模拟模式 |
| `--auto-publish` | 公众号：自动发布草稿 | 仅创建草稿 |

### 示例

```bash
# 使用本地MCP发布到小红书（真实发布）
python scripts/publisher.py --platform xiaohongshu --local

# 发布到公众号并自动发布
python scripts/publisher.py --platform wechat --auto-publish

# 全部发布（小红书真实发布，公众号自动发布）
python scripts/publisher.py --platform all --local --auto-publish

# 模拟发布（测试用，不真正发布）
python scripts/publisher.py --platform all
```

---

## 🔧 公众号配置

需要在 `config.py` 或 GitHub Secrets 中配置：

```python
WECHAT_APPID = "你的AppID"
WECHAT_APPSECRET = "你的AppSecret"
```

获取方式：
1. 登录[微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **设置 → 账号信息** 获取 AppID
3. 进入 **设置 → 开发配置** 获取 AppSecret

---

## ⚠️ 注意事项

### 小红书
- 需要保持登录状态，如果Cookie过期需要重新登录
- 使用 `--local` 参数会真实发布，不使用则模拟测试
- 建议先模拟测试，确认内容正确后再真实发布

### 公众号
- 使用 `--auto-publish` 会直接发布到公众号
- 不使用则只创建草稿，需要手动在公众号后台发布
- 草稿保存在公众号后台的 **草稿箱** 中

---

## 📁 生成的内容文件

每天生成的内容保存在：

```
media-automation/
├── content/
│   └── xiaohongshu/
│       └── YYYY-MM-DD/
│           └── post_morning_2026-01-29.json
│           └── post_evening_2026-01-29.json
├── data/
│   └── records/
│       └── 2026-01-29_morning_post.json
│       └── 2026-01-29_evening_post.json
│       └── 2026-01-29_summary.json
```

---

## 🎯 推荐工作流程

### 日常流程

1. **早上** (6:00) - GitHub Actions 自动生成早间内容
2. **中午** - 你检查生成的内容
3. **晚上** (8:00) - GitHub Actions 自动生成晚间内容
4. **睡前** - 本地执行发布命令

### 每日发布命令

```bash
# 1. 发布今日所有内容
python scripts/publisher.py --platform all --local --auto-publish

# 2. 或者分别发布
python scripts/publisher.py --platform xiaohongshu --local
python scripts/publisher.py --platform wechat --auto-publish
```

---

## 🔄 重新登录小红书

如果Cookie过期或登录失效：

```bash
# 重新登录
env phone=13810119101 python -m xhs_mcp_server.__login__

# 验证登录状态
env phone=13810119101 python -m xhs_mcp_server.__login__
# 应该显示 "使用cookies登录成功"
```

---

## ❓ 常见问题

### Q: 提示 "xhs_mcp_server" 模块不存在
A: 请先安装：`pip install xhs-mcp-server`

### Q: 小红书发布失败
A: 
1. 检查是否登录成功
2. 检查Cookie是否有效
3. 检查图片路径是否正确

### Q: 公众号发布失败
A: 
1. 检查AppID和AppSecret是否正确
2. 检查access_token是否过期
3. 确认有发布权限

### Q: 如何只测试不真正发布？
A: 不使用 `--local` 和 `--auto-publish` 参数即可模拟发布

---

## 📞 获取帮助

如果在发布过程中遇到问题：
1. 查看终端错误信息
2. 检查配置文件是否正确
3. 确认网络连接正常
