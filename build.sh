#!/bin/bash
# Render构建脚本

echo "🚀 开始构建应用..."

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 初始化数据库（如果需要）
# python src/scripts/init_db.py

echo "✅ 构建完成！"
