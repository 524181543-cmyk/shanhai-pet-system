"""
山海经班级宠物积分系统 - 独立启动文件
不依赖任何其他文件，完全独立运行
"""
import os
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="山海经班级宠物积分系统",
    description="基于山海经主题的班级宠物积分系统",
    version="1.0.0"
)

logger.info("=" * 60)
logger.info("🐉 山海经班级宠物积分系统")
logger.info("=" * 60)

# 首页HTML
INDEX_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>山海经班级宠物积分系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
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
            max-width: 700px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.6s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1em;
        }
        .pet-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 30px 0;
        }
        .pet-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
            border-radius: 15px;
            padding: 20px 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .pet-card:hover {
            transform: translateY(-8px);
            border-color: #667eea;
            box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        }
        .pet-icon {
            font-size: 3em;
            margin-bottom: 10px;
        }
        .pet-name {
            font-weight: bold;
            color: #333;
            font-size: 1em;
        }
        .features {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-top: 25px;
        }
        .features h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .features p {
            color: #555;
            line-height: 2;
            margin: 8px 0;
            font-size: 1em;
        }
        .status {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-radius: 12px;
            color: #2e7d32;
            font-weight: 600;
            font-size: 1.1em;
        }
        .footer {
            text-align: center;
            margin-top: 25px;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐉 山海经班级宠物积分系统</h1>
        <p class="subtitle">领养你的专属神兽，开启奇幻之旅</p>
        
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
        
        <div class="features">
            <h3>🎮 系统功能</h3>
            <p>✨ 领养专属山海经神兽</p>
            <p>⭐ 积分系统解锁宠物进化形态</p>
            <p>🏆 班级积分排行榜竞技</p>
            <p>🎯 解锁宠物特殊技能</p>
        </div>
        
        <div class="status">
            ✅ 系统运行正常！欢迎来到山海经世界
        </div>
        
        <div class="footer">
            Powered by Railway | 山海经班级宠物积分系统 v1.0
        </div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    """首页"""
    return HTMLResponse(content=INDEX_HTML, status_code=200)

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "service": "山海经班级宠物积分系统",
        "version": "1.0.0"
    }

@app.get("/api/pets/types")
async def get_pet_types():
    """获取宠物类型"""
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

@app.on_event("startup")
async def startup():
    port = os.environ.get("PORT", "8000")
    logger.info(f"✅ 应用启动成功！端口: {port}")

# 直接运行
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🚀 启动服务器，端口: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
