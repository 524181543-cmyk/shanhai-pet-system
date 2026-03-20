#!/bin/bash
# 一键启动公网访问

echo "============================================"
echo "🐉 山海经宠物系统 - 一键公网部署"
echo "============================================"
echo ""

# 步骤1：安装ngrok
if ! command -v ngrok &> /dev/null; then
    echo "📦 步骤1: 安装ngrok..."
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null 2>&1
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list >/dev/null 2>&1
    sudo apt update -qq && sudo apt install -y ngrok >/dev/null 2>&1
    echo "✅ ngrok安装完成"
else
    echo "✅ 步骤1: ngrok已安装"
fi

echo ""
echo "🚀 步骤2: 启动应用服务..."

# 停止可能运行的旧服务
pkill -f "python src/main.py" 2>/dev/null || true

# 启动应用（后台运行）
nohup python src/main.py -m http -p 8000 > /tmp/pet_app.log 2>&1 &
APP_PID=$!

# 等待服务启动
sleep 3

# 检查服务是否启动成功
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 应用服务已启动 (PID: $APP_PID)"
    echo "   本地地址: http://localhost:8000"
else
    echo "❌ 应用启动失败，请检查日志: /tmp/pet_app.log"
    exit 1
fi

echo ""
echo "🌐 步骤3: 启动公网穿透..."
echo ""
echo "即将获得公网访问地址，请稍候..."
echo ""

# 启动ngrok（前台运行，会显示公网地址）
ngrok http 8000
