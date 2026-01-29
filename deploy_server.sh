#!/bin/bash
# 🚀 媒体自动化系统 - 服务器端一键部署脚本
# 在云服务器上执行此脚本

set -e  # 遇到错误立即退出

echo "================================"
echo "🚀 媒体自动化系统 - 服务器部署"
echo "================================"
echo ""

# 1. 安装系统依赖
echo "📦 安装系统依赖..."
apt update && apt upgrade -y
apt install -y curl wget git python3 python3-pip nginx

# 2. 安装Docker
echo ""
echo "🐳 安装Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl start docker
    systemctl enable docker
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker已安装"
fi

# 3. 克隆项目
echo ""
echo "📥 克隆项目..."
cd /root
if [ -d "pettest" ]; then
    cd pettest
    git pull origin master
else
    git clone https://github.com/amirbebebebe/pettest.git
    cd pettest
fi

# 4. 安装Python依赖
echo ""
echo "🐍 安装Python依赖..."
pip3 install -r requirements.txt
pip3 install --no-cache-dir flask requests

# 5. 安装Chrome和ChromeDriver
echo ""
echo "🌐 安装Chrome和ChromeDriver..."
if ! command -v google-chrome &> /dev/null; then
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable
fi

if ! command -v chromedriver &> /dev/null; then
    npx @puppeteer/browsers install chromedriver@latest
fi

# 6. 安装xhs-mcp-server
echo ""
echo "📱 安装xhs-mcp-server..."
pip3 install --no-cache-dir xhs-mcp-server

# 7. 创建环境变量文件
echo ""
echo "⚙️ 配置环境变量..."
cat > /root/pettest/.env << 'ENVEOF'
VOLCANO_API_KEY=你的火山API_KEY
VOLCANO_API_SECRET=你的火山API_SECRET
WECHAT_APPID=你的公众号APPID
WECHAT_APPSECRET=你的公众号APPSECRET
XIAOHONGSHU_COOKIE=你的小红书COOKIE
ENVEOF

echo "⚠️ 请编辑 /root/pettest/.env 文件，配置你的API密钥"
echo "   命令: nano /root/pettest/.env"

# 8. 创建数据目录
echo ""
echo "📁 创建数据目录..."
mkdir -p /root/pettest/content /root/pettest/data /root/pettest/logs

# 9. 测试启动服务
echo ""
echo "🧪 测试启动服务..."
cd /root/pettest
timeout 10 python3 scripts/cloud_publisher.py || true

# 10. 配置systemd服务
echo ""
echo "⚙️ 配置systemd服务..."
cat > /etc/systemd/system/media-publisher.service << 'SERVICEEOF'
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
SERVICEEOF

systemctl daemon-reload
systemctl enable media-publisher
systemctl start media-publisher

# 11. 配置Nginx（可选）
echo ""
echo "🌐 配置Nginx（可选）..."
cat > /etc/nginx/sites-available/media-automation << 'NGINXEOF'
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF

ln -sf /etc/nginx/sites-available/media-automation /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

echo ""
echo "================================"
echo "✅ 部署完成!"
echo "================================"
echo ""
echo "📝 下一步操作:"
echo ""
echo "1. 🔑 配置环境变量:"
echo "   nano /root/pettest/.env"
echo ""
echo "2. 📱 登录小红书:"
echo "   export PHONE=13810119101"
echo "   python3 -m xhs_mcp_server.__login__"
echo "   # 扫码并在APP中确认登录"
echo ""
echo "3. 🔗 配置GitHub Webhook:"
echo "   - 进入GitHub仓库 → Settings → Webhooks"
echo "   - 添加Webhook:"
echo "     * Payload URL: http://你的IP/webhook"
echo "     * Content type: application/json"
echo ""
echo "4. 🧪 测试服务:"
echo "   curl http://localhost:5000/health"
echo ""
echo "5. 📊 查看日志:"
echo "   journalctl -u media-publisher -f"
echo ""
echo "💡 服务已启动并开机自启"
echo "🌐 访问 http://43.129.244.5000 查看健康状态"
echo ""
