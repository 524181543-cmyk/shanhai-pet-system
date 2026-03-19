#!/bin/bash
# Railway部署助手
# 自动化部署到Railway

echo "============================================"
echo "🐉 山海经宠物系统 - Railway部署助手"
echo "============================================"
echo ""

# 检查是否有gh命令
if command -v gh &> /dev/null; then
    echo "✅ 检测到GitHub CLI已安装"
    echo ""
    echo "是否要创建GitHub仓库并推送？(y/n)"
    read -r answer

    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo "请输入仓库名称 (默认: shanhai-pet-system):"
        read -r repo_name
        repo_name=${repo_name:-shanhai-pet-system}

        echo ""
        echo "📦 创建GitHub仓库: $repo_name"
        gh repo create "$repo_name" --public --source=. --remote=origin --push

        echo ""
        echo "✅ 仓库创建并推送成功！"
        echo ""
        echo " Railway部署步骤："
        echo "1. 访问 https://railway.app/"
        echo "2. 点击 'New Project'"
        echo "3. 选择 'Deploy from GitHub repo'"
        echo "4. 选择仓库: $repo_name"
        echo "5. 等待部署完成"
    fi
else
    echo "❌ 未检测到GitHub CLI"
    echo ""
    echo "请按以下步骤操作："
    echo ""
    echo "第一步：在GitHub创建仓库"
    echo "  访问: https://github.com/new"
    echo "  仓库名: shanhai-pet-system"
    echo "  类型: Public"
    echo "  不要勾选初始化选项"
    echo ""
    echo "第二步：推送代码"
    echo "  git remote add origin https://github.com/你的用户名/shanhai-pet-system.git"
    echo "  git push -u origin main"
    echo ""
    echo "第三步：在Railway部署"
    echo "  访问: https://railway.app/"
    echo "  选择你的GitHub仓库"
    echo "  等待部署"
fi
