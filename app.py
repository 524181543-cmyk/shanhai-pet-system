"""
山海经班级宠物积分系统 - Railway启动入口（简化版）
"""
import os
import sys
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(title="山海经班级宠物积分系统")

# 添加健康检查端点
@app.get("/health")
async def health():
    return {"status": "ok", "message": "Service is running"}

# 添加根路径
@app.get("/")
async def root():
    return {"message": "山海经班级宠物积分系统", "status": "running"}

# 尝试导入宠物系统路由
try:
    # 添加src路径
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    from server.pet_app_simple import create_pet_routes
    create_pet_routes(app)
    logger.info("✅ 宠物系统路由已注册")
except Exception as e:
    logger.warning(f"⚠️ 宠物系统路由注册失败: {str(e)}")
    logger.info("使用简化版服务...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"🚀 启动服务，端口: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
