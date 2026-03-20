#!/bin/bash
# Render启动脚本

echo "🚀 启动山海经班级宠物积分系统..."

# 使用环境变量PORT（Render会自动设置）
python src/main.py -m http -p ${PORT:-8000}
