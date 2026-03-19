#!/bin/bash
# 自动推送脚本
# 使用方法: ./push_to_github.sh 你的GitHub用户名 你的仓库名

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法: $0 <GitHub用户名> <仓库名>"
    echo "示例: $0 myusername shanhai-pet-system"
    exit 1
fi

USERNAME=$1
REPO=$2

echo "============================================"
echo "🐉 准备推送山海经宠物系统到GitHub"
echo "============================================"
echo ""
echo "GitHub用户名: $USERNAME"
echo "仓库名称: $REPO"
echo "远程地址: https://github.com/$USERNAME/$REPO.git"
echo ""

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo "📦 发现有未提交的更改，正在提交..."
    git add .
    git commit -m "feat: 更新代码"
fi

# 检查是否已有origin
if git remote get-url origin 2>/dev/null; then
    echo "⚠️  检测到已存在origin远程仓库"
    echo "更新远程地址..."
    git remote set-url origin https://github.com/$USERNAME/$REPO.git
else
    echo "➕ 添加远程仓库..."
    git remote add origin https://github.com/$USERNAME/$REPO.git
fi

echo ""
echo "🚀 推送代码到GitHub..."
git push -u origin main

echo ""
echo "============================================"
echo "✅ 推送成功！"
echo "============================================"
echo ""
echo "下一步："
echo "1. 访问 https://railway.app/"
echo "2. 点击 'New Project'"
echo "3. 选择 'Deploy from GitHub repo'"
echo "4. 选择仓库: $REPO"
echo "5. 等待部署完成"
echo ""
