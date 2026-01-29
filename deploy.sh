#!/bin/bash
# 🚀 媒体自动化系统 - 一键部署脚本
# 在本地执行此脚本，将项目部署到云服务器

# 服务器配置
SERVER_IP="43.129.244.154"
SERVER_USER="root"
PROJECT_PATH="/root/pettest"

echo "================================"
echo "🚀 媒体自动化系统 - 部署脚本"
echo "================================"
echo ""
echo "📡 服务器: $SERVER_IP"
echo "📁 项目路径: $PROJECT_PATH"
echo ""

# 检查本地Git状态
echo "📦 检查本地Git状态..."
cd "$(dirname "$0")"
git status

# 提示用户确认
read -p "确认推送到GitHub并部署到服务器? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ 已取消"
    exit 1
fi

# 1. 推送到GitHub
echo ""
echo "📤 推送代码到GitHub..."
git add .
git commit -m "添加云端自动化发布系统"
git push origin master

# 2. 连接服务器并执行部署
echo ""
echo "🔗 连接服务器并部署..."

# 上传部署脚本到服务器
scp deploy_server.sh $SERVER_USER@$SERVER_IP:/tmp/

# 在服务器上执行部署
ssh $SERVER_USER@$SERVER_IP << 'EOF'
chmod +x /tmp/deploy_server.sh
/tmp/deploy_server.sh
EOF

echo ""
echo "================================"
echo "✅ 部署完成!"
echo "================================"
echo ""
echo "💡 下一步:"
echo "1. 登录小红书: env phone=13810119101 python3 -m xhs_mcp_server.__login__"
echo "2. 配置GitHub Webhook"
echo "3. 测试完整流程"
echo ""
