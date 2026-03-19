"""
启动脚本
用于初始化数据库并启动Flask服务器
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("山海经班级宠物积分系统启动中...")
    logger.info("=" * 60)
    
    # 初始化数据库
    logger.info("步骤1: 初始化数据库...")
    try:
        from init_db import init_database
        init_database()
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        logger.info("继续启动服务器...")
    
    # 启动Flask服务器
    logger.info("步骤2: 启动Flask服务器...")
    os.chdir(os.path.join(os.path.dirname(__file__), '../..'))
    
    from server.app import app
    
    # 获取端口号
    port = int(os.getenv('PORT', 5001))
    
    logger.info(f"服务器启动成功！访问地址: http://0.0.0.0:{port}")
    logger.info("按 Ctrl+C 停止服务器")
    
    # 启动服务器
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    main()
