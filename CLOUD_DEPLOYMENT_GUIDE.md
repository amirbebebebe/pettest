# 🚀 云服务器部署指南

## 📋 概述

本项目可以在云服务器上部署，实现完全自动化的内容发布：
- GitHub Actions 自动生成内容
- 自动触发云端发布服务
- 自动发布到小红书和公众号

---

## 🛒 第一步：购买云服务器

### 推荐配置

| 服务商 | 产品 | 价格 | 链接 |
|--------|------|------|------|
| 腾讯云 | 轻量应用服务器 2核2G | 约50-100元/年 | https://cloud.tencent.com/ |
| 阿里云 | 轻量应用服务器 2核2G | 约100-200元/年 | https://www.aliyun.com/ |
| 华为云 | 轻量服务器 2核2G | 约100-200元/年 | https://www.huaweicloud.com/ |

### 推荐选择
- **腾讯云轻量应用服务器**（性价比最高）
- 配置：2核2G，50GB SSD，系统盘
- 操作系统：Ubuntu 22.04 LTS

---

## 🔧 第二步：连接服务器

### 1. 获取服务器信息
购买后，你会获得：
- 公网IP地址
- SSH登录账号（通常是 `root`）
- SSH登录密码（或密钥）

### 2. 连接服务器

**Windows用户**（使用PowerShell）：
```powershell
ssh root@你的公网IP
```

**Mac/Linux用户**：
```bash
ssh root@你的公网IP
```

### 3. 首次登录设置

```bash
# 更新系统
apt update && apt upgrade -y

# 安装必要工具
apt install -y curl wget git python3 python3-pip nginx

# 创建用户（可选）
adduser media
```

---

## 🐳 第三步：安装Docker（推荐）

### 1. 安装Docker

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh

# 启动Docker
systemctl start docker
systemctl enable docker

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 2. 验证安装

```bash
docker --version
docker-compose --version
```

---

## 📦 第四步：部署项目

### 1. 上传项目到服务器

**方式A：使用Git（推荐）**

```bash
# 克隆项目
git clone https://github.com/amirbebebebe/pettest.git
cd pettest
```

**方式B：使用SFTP上传**

使用FileZilla或WinSCP将本地项目上传到服务器。

### 2. 安装依赖

```bash
pip3 install -r requirements.txt
pip3 install flask requests
```

### 3. 配置环境变量

```bash
# 编辑环境变量文件
nano .env
```

添加以下内容：
```bash
VOLCANO_API_KEY=你的火山API_KEY
VOLCANO_API_SECRET=你的火山API_SECRET
WECHAT_APPID=你的公众号APPID
WECHAT_APPSECRET=你的公众号APPSECRET
XIAOHONGSHU_COOKIE=你的小红书COOKIE
```

### 4. 安装ChromeDriver

```bash
# 安装Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f -y

# 安装ChromeDriver
npx @puppeteer/browsers install chromedriver@latest
```

### 5. 安装xhs-mcp-server

```bash
pip3 install xhs-mcp-server
```

---

## 🔐 第五步：配置小红书登录

### 1. 登录小红书

```bash
# 设置手机号环境变量
export PHONE="13810119101"

# 执行登录
python3 -m xhs_mcp_server.__login__
```

终端会显示二维码，用小红书APP扫描并确认登录。

### 2. 验证登录

```bash
python3 -m xhs_mcp_server.__login__
```

应该显示：`使用cookies登录成功`

---

## 🌐 第六步：配置Nginx和域名

### 1. 购买域名（可选）

推荐在阿里云或腾讯云购买域名：
- 年费约50-100元
- 解析到你的服务器IP

### 2. 配置Nginx

```bash
nano /etc/nginx/sites-available/media-automation
```

添加以下配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. 启用配置

```bash
ln -s /etc/nginx/sites-available/media-automation /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 4. 申请SSL证书（推荐）

```bash
# 安装certbot
apt install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com
```

---

## 🔄 第七步：配置开机自启

### 1. 创建systemd服务

```bash
nano /etc/systemd/system/media-publisher.service
```

添加以下内容：
```ini
[Unit]
Description=Media Automation Publisher
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/pettest
ExecStart=/usr/bin/python3 /root/pettest/scripts/cloud_publisher.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/root/pettest

[Install]
WantedBy=multi-user.target
```

### 2. 启用服务

```bash
# 重新加载
systemctl daemon-reload

# 启用开机自启
systemctl enable media-publisher

# 启动服务
systemctl start media-publisher

# 查看状态
systemctl status media-publisher
```

---

## 🔗 第八步：配置GitHub Webhook

### 1. 在GitHub仓库添加Webhook

1. 进入GitHub仓库：`https://github.com/amirbebebebe/pettest`
2. 点击 **Settings → Webhooks → Add webhook**
3. 填写信息：
   - **Payload URL**: `http://你的域名/webhook`
   - **Content type**: `application/json`
   - **Secret**: 设置一个密码（记住它）
4. 点击 **Add webhook**

### 2. 更新GitHub Actions工作流

编辑 `.github/workflows/daily-publish.yml`，在最后添加Webhook触发：

```yaml
      # 9. 触发云端发布
      - name: 触发云端发布
        if: always()
        run: |
          if [ "${{ job.status }}" == "success" ]; then
            echo "🚀 触发云端发布..."
            curl -X POST https://你的域名/webhook \
              -H "Content-Type: application/json" \
              -d '{"event": "content_generated", "status": "success"}'
          fi
```

---

## 🧪 第九步：测试

### 1. 测试本地发布

```bash
# 测试发布服务
python3 scripts/cloud_publisher.py &
```

在浏览器访问：
- `http://你的IP:5000/health` - 应该返回健康检查信息

### 2. 测试Webhook

```bash
curl -X POST http://你的IP:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### 3. 手动触发发布

```bash
curl -X POST http://你的IP:5000/publish \
  -H "Content-Type: application/json" \
  -d '{"content": "测试内容"}'
```

---

## 📊 完整流程

### 日常运行流程

1. **每天6:00/20:00** - GitHub Actions 自动生成内容
2. **内容生成完成** - 自动提交到仓库
3. **触发Webhook** - 调用云端发布服务
4. **云端接收** - Flask服务接收请求
5. **自动发布** - 并行发布到小红书和公众号
6. **返回结果** - 记录发布状态

### 你需要做的

- 购买云服务器（已购买）
- 部署项目（完成）
- 配置Webhook（完成）
- 测试完整流程

---

## 🔧 常用命令

```bash
# 查看服务状态
systemctl status media-publisher

# 重启服务
systemctl restart media-publisher

# 查看日志
journalctl -u media-publisher -f

# 查看端口占用
netstat -tlnp | grep 5000

# 重启Nginx
systemctl restart nginx

# 查看磁盘空间
df -h

# 查看内存使用
free -m
```

---

## ❓ 常见问题

### Q: 服务启动失败
A: 
1. 检查日志：`journalctl -u media-publisher -f`
2. 检查端口是否被占用：`netstat -tlnp | grep 5000`
3. 检查环境变量是否配置正确

### Q: 无法访问服务
A: 
1. 检查防火墙：`ufw status`
2. 开放端口：`ufw allow 5000`
3. 检查云服务器安全组是否开放端口

### Q: 发布失败
A: 
1. 检查小红书Cookie是否有效
2. 检查公众号AppID和AppSecret
3. 查看服务日志

---

## 🎯 下一步

1. 购买云服务器（如果还没购买）
2. 按照本指南部署
3. 测试完整流程
4. 配置域名和SSL证书

**需要我帮你购买或配置云服务器吗？** 
