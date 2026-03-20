"""
山海经班级宠物积分系统 - Railway启动入口（简化版）
"""
import os
import sys
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(title="山海经班级宠物积分系统")

# 添加健康检查端点
@app.get("/health")
async def health():
    return {"status": "ok", "message": "Service is running"}

# 添加根路径
@app.get("/", response_class=HTMLResponse)
async def root():
    """返回前端页面"""
    html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>山海经班级宠物积分系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2em;
        }
        .pet-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .pet-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .pet-card:hover {
            transform: translateY(-5px);
        }
        .pet-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
        .pet-name {
            font-weight: bold;
            color: #333;
        }
        .info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .info h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .info p {
            color: #666;
            line-height: 1.6;
        }
        .status {
            text-align: center;
            margin-top: 30px;
            padding: 15px;
            background: #e8f5e9;
            border-radius: 10px;
            color: #2e7d32;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐉 山海经班级宠物积分系统</h1>
        
        <div class="pet-grid">
            <div class="pet-card">
                <div class="pet-icon">🐉</div>
                <div class="pet-name">麒麟</div>
            </div>
            <div class="pet-card">
                <div class="pet-icon">🦅</div>
                <div class="pet-name">凤凰</div>
            </div>
            <div class="pet-card">
                <div class="pet-icon">🦊</div>
                <div class="pet-name">九尾狐</div>
            </div>
            <div class="pet-card">
                <div class="pet-icon">🐢</div>
                <div class="pet-name">玄武</div>
            </div>
            <div class="pet-card">
                <div class="pet-icon">🐯</div>
                <div class="pet-name">白虎</div>
            </div>
            <div class="pet-card">
                <div class="pet-icon">🐲</div>
                <div class="pet-name">青龙</div>
            </div>
        </div>
        
        <div class="info">
            <h3>🎮 系统功能</h3>
            <p>✨ 领养专属山海经神兽</p>
            <p>⭐ 积分系统解锁宠物形态</p>
            <p>🏆 班级积分排行榜</p>
            <p>🎯 多种技能系统</p>
        </div>
        
        <div class="status">
            ✅ 系统运行正常！
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html, status_code=200)

@app.get("/api/pets/types")
async def get_pet_types():
    """获取所有宠物类型"""
    return {
        "success": True,
        "data": [
            {"id": 1, "name": "麒麟", "description": "祥瑞之兽", "icon": "🐉"},
            {"id": 2, "name": "凤凰", "description": "百鸟之王", "icon": "🦅"},
            {"id": 3, "name": "九尾狐", "description": "智慧之兽", "icon": "🦊"},
            {"id": 4, "name": "玄武", "description": "北方神兽", "icon": "🐢"},
            {"id": 5, "name": "白虎", "description": "西方神兽", "icon": "🐯"},
            {"id": 6, "name": "青龙", "description": "东方神兽", "icon": "🐲"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🚀 启动服务，端口: {port}")
    logger.info(f"🌐 访问地址: http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
