#!/bin/bash
# 推送代码到GitHub
# 请在你能访问GitHub的环境中运行此脚本

echo "============================================"
echo "🐉 推送山海经宠物系统到GitHub"
echo "============================================"
echo ""

# 仓库地址
REPO_URL="https://github.com/524181543-cmyk/shanhai-pet-system.git"

echo "目标仓库: $REPO_URL"
echo ""

# 检查是否已有origin
if git remote get-url origin 2>/dev/null; then
    echo "更新远程仓库地址..."
    git remote set-url origin $REPO_URL
else
    echo "添加远程仓库..."
    git remote add origin $REPO_URL
fi

echo ""
echo "推送代码到GitHub..."
echo ""

# 尝试推送
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✅ 推送成功！"
    echo "============================================"
    echo ""
    echo "访问你的仓库: https://github.com/524181543-cmyk/shanhai-pet-system"
    echo ""
    echo "下一步："
    echo "1. 访问 https://railway.app/"
    echo "2. 用GitHub登录"
    echo "3. 点击 'New Project'"
    echo "4. 选择 'Deploy from GitHub repo'"
    echo "5. 选择 shanhai-pet-system 仓库"
    echo "6. 等待部署完成"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因："
    echo "1. 需要GitHub认证"
    echo "2. 仓库不存在"
    echo ""
    echo "解决方案："
    echo "1. 确保仓库已创建: https://github.com/new"
    echo "2. 使用Personal Access Token推送"
    echo "   git push https://YOUR_TOKEN@github.com/524181543-cmyk/shanhai-pet-system.git main"
    echo ""
fi
