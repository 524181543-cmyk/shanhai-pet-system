#!/bin/bash
# 打包项目代码供Render上传

echo "📦 打包山海经宠物积分系统..."

# 设置包名
PACKAGE_NAME="shanhai-pet-system-$(date +%Y%m%d-%H%M%S).tar.gz"

# 打包（排除不必要的文件）
tar -czf "$PACKAGE_NAME" \
  --exclude='.git' \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='*.log' \
  --exclude='*.tar.gz' \
  --exclude='.env' \
  --exclude='node_modules' \
  --exclude='.DS_Store' \
  --exclude='tests' \
  --exclude='.pytest_cache' \
  --exclude='htmlcov' \
  --exclude='.coverage' \
  .

echo ""
echo "✅ 打包完成！"
echo ""
echo "📦 文件名: $PACKAGE_NAME"
echo "📊 文件大小: $(du -h "$PACKAGE_NAME" | cut -f1)"
echo ""
echo "下一步："
echo "1. 访问 https://dashboard.render.com/"
echo "2. 创建新的Web Service"
echo "3. 上传此压缩包文件"
echo ""
