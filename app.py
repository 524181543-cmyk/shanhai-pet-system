"""
山海经班级宠物积分系统 - Railway启动入口
"""
import os
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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

logger.info("🚀 山海经班级宠物积分系统启动中...")

# 首页
@app.get("/", response_class=HTMLResponse)
async def index():
    """返回前端页面"""
    html_content = """
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
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.9em;
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
            transform: translateY(-5px);
            border-color: #667eea;
            box-shadow: 0 10px 30px rgba(102,126,234,0.3);
        }
        .pet-icon {
            font-size: 2.5em;
            margin-bottom: 8px;
        }
        .pet-name {
            font-weight: bold;
            color: #333;
            font-size: 0.95em;
        }
        .features {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .features h3 {
            color: #667eea;
            margin-bottom: 12px;
            font-size: 1.1em;
        }
        .features p {
            color: #555;
            line-height: 1.8;
            margin: 5px 0;
        }
        .status {
            text-align: center;
            margin-top: 25px;
            padding: 15px;
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-radius: 10px;
            color: #2e7d32;
            font-weight: 500;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 0.85em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐉 山海经班级宠物积分系统</h1>
        <p class="subtitle">领养你的专属神兽，开启奇幻之旅</p>
        
        <div class="pet-grid">
            <div class="pet-card" onclick="alert('麒麟 - 祥瑞之兽，象征着仁慈与和平')">
                <div class="pet-icon">🐉</div>
                <div class="pet-name">麒麟</div>
            </div>
            <div class="pet-card" onclick="alert('凤凰 - 百鸟之王，浴火重生')">
                <div class="pet-icon">🦅</div>
                <div class="pet-name">凤凰</div>
            </div>
            <div class="pet-card" onclick="alert('九尾狐 - 智慧之兽，通灵达意')">
                <div class="pet-icon">🦊</div>
                <div class="pet-name">九尾狐</div>
            </div>
            <div class="pet-card" onclick="alert('玄武 - 北方神兽，守护之灵')">
                <div class="pet-icon">🐢</div>
                <div class="pet-name">玄武</div>
            </div>
            <div class="pet-card" onclick="alert('白虎 - 西方神兽，威武勇猛')">
                <div class="pet-icon">🐯</div>
                <div class="pet-name">白虎</div>
            </div>
            <div class="pet-card" onclick="alert('青龙 - 东方神兽，腾云驾雾')">
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
            ✅ 系统已成功部署并运行！
        </div>
        
        <div class="footer">
            Powered by Railway | 山海经班级宠物积分系统 v1.0
        </div>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# 健康检查
@app.get("/health")
async def health():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": "山海经班级宠物积分系统",
        "version": "1.0.0"
    }

# API接口
@app.get("/api/pets/types")
async def get_pet_types():
    """获取所有宠物类型"""
    return {
        "success": True,
        "data": [
            {"id": 1, "name": "麒麟", "description": "祥瑞之兽，仁慈和平", "icon": "🐉"},
            {"id": 2, "name": "凤凰", "description": "百鸟之王，浴火重生", "icon": "🦅"},
            {"id": 3, "name": "九尾狐", "description": "智慧之兽，通灵达意", "icon": "🦊"},
            {"id": 4, "name": "玄武", "description": "北方神兽，守护之灵", "icon": "🐢"},
            {"id": 5, "name": "白虎", "description": "西方神兽，威武勇猛", "icon": "🐯"},
            {"id": 6, "name": "青龙", "description": "东方神兽，腾云驾雾", "icon": "🐲"},
        ]
    }

@app.get("/api/leaderboard")
async def get_leaderboard():
    """获取排行榜"""
    return {
        "success": True,
        "data": []
    }

# 启动事件
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 50)
    logger.info("🐉 山海经班级宠物积分系统已启动")
    logger.info("🌐 访问地址: http://0.0.0.0:" + os.environ.get("PORT", "8000"))
    logger.info("=" * 50)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
