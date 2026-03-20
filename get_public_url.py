#!/usr/bin/env python3
"""
使用ngrok创建公网访问地址
"""
import time
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("=" * 60)
    print("🐉 山海经班级宠物积分系统 - 创建公网访问")
    print("=" * 60)
    print()
    
    try:
        from pyngrok import ngrok
        
        print("🚀 正在启动ngrok隧道...")
        print()
        
        # 创建ngrok隧道
        public_url = ngrok.connect(8000)
        
        print("✅ 公网访问地址创建成功！")
        print()
        print("=" * 60)
        print("🌐 你的公网访问地址：")
        print("=" * 60)
        print()
        print(f"  {public_url}")
        print()
        print("=" * 60)
        print()
        print("📱 使用说明：")
        print("  1. 复制上面的地址")
        print("  2. 分享给学生")
        print("  3. 学生在浏览器中打开即可访问")
        print()
        print("💡 提示：")
        print("  - 地址会一直保持在线，直到你停止程序")
        print("  - 按 Ctrl+C 可停止服务")
        print()
        print("=" * 60)
        print()
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 正在停止服务...")
            ngrok.disconnect(public_url)
            print("✅ 服务已停止")
            
    except ImportError:
        print("❌ pyngrok未安装，正在安装...")
        os.system("pip install pyngrok")
        print("请重新运行此脚本")
    except Exception as e:
        print(f"❌ 错误: {e}")
        print()
        print("请确保应用服务正在运行：")
        print("  bash scripts/http_run.sh")

if __name__ == "__main__":
    main()
