#!/usr/bin/env python3
"""
部署前检查脚本
用于验证应用是否可以正常启动
"""
import os
import sys
import json

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def check_dependencies():
    """检查依赖是否安装"""
    print("📦 检查依赖...")
    try:
        import flask
        import fastapi
        import uvicorn
        import supabase
        print("✅ 核心依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return False

def check_environment():
    """检查环境变量"""
    print("\n🔧 检查环境变量...")
    required_vars = [
        'COZE_SUPABASE_URL',
        'PGDATABASE_URL'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: 已设置")
        else:
            print(f"⚠️  {var}: 未设置")
            all_set = False
    
    return all_set

def check_database():
    """检查数据库连接"""
    print("\n🗄️  检查数据库连接...")
    try:
        from storage.database.supabase_client import get_supabase_client
        client = get_supabase_client()
        
        # 尝试查询宠物类型
        result = client.table('pet_types').select('count').execute()
        if result.data is not None:
            print("✅ 数据库连接正常")
            print(f"   已有 {len(result.data)} 种宠物类型")
            return True
        else:
            print("❌ 数据库查询失败")
            return False
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def check_port():
    """检查端口配置"""
    print("\n🌐 检查端口配置...")
    port = os.getenv('PORT', '8000')
    print(f"✅ 应用将运行在端口: {port}")
    return True

def main():
    print("=" * 60)
    print("🐉 山海经班级宠物积分系统 - 部署前检查")
    print("=" * 60)
    
    results = []
    
    results.append(("依赖检查", check_dependencies()))
    results.append(("环境变量", check_environment()))
    results.append(("数据库连接", check_database()))
    results.append(("端口配置", check_port()))
    
    print("\n" + "=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 所有检查通过！可以开始部署。")
        print("\n下一步：")
        print("1. 推送代码到GitHub")
        print("2. 在Railway创建项目")
        print("3. 选择GitHub仓库进行部署")
        print("\n详细步骤请查看 DEPLOY.md 文件")
        return 0
    else:
        print("\n⚠️  部分检查未通过，请先解决问题。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
