#!/bin/bash
# ngrok一键安装和启动脚本

echo "============================================"
echo "🐉 山海经宠物系统 - ngrok公网穿透"
echo "============================================"
echo ""

# 检查ngrok是否已安装
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok已安装"
else
    echo "📦 正在安装ngrok..."
    
    # 下载并安装ngrok
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install ngrok
    
    echo "✅ ngrok安装完成"
fi

echo ""
echo "🚀 启动公网穿透..."
echo ""
echo "服务将在以下地址运行："
echo "  本地地址: http://localhost:8000"
echo "  公网地址: 运行后会显示"
echo ""
echo "提示: 按 Ctrl+C 停止服务"
echo ""

# 启动ngrok
ngrok http 8000
