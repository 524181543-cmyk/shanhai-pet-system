"""
山海经班级宠物积分系统 - 完整版 V2
新增：宠物喂养系统、3D动态神兽、山海经原型设计
"""
import os
import sys
import logging
import random
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
import uvicorn

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

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
    version="2.0.0",
    docs_url=None,
    redoc_url=None
)

# ========== 健康检查端点（必须放在最前面）==========

@app.get("/health")
async def health():
    """健康检查 - Railway 使用此端点检查服务状态"""
    return {"status": "ok", "service": "山海经班级宠物积分系统", "version": "2.0.0"}

@app.get("/")
async def root():
    """根路径重定向到主页面"""
    return HTMLResponse(content=INDEX_HTML, status_code=200)

# 数据库连接（延迟初始化）
_db = None

def get_db():
    """获取数据库连接（延迟初始化）"""
    global _db
    if _db is None:
        try:
            from storage.database.supabase_client import get_supabase_client
            _db = get_supabase_client()
            logger.info("✅ 数据库连接成功")
        except Exception as e:
            logger.warning(f"⚠️ 数据库连接失败: {str(e)}")
            logger.info("使用模拟数据模式...")
    return _db

# 模拟数据存储
mock_db = {
    'users': {},
    'user_pets': {},
    'point_records': [],
    'next_user_id': 1,
    'next_pet_id': 1
}

# ========== Pydantic模型 ==========

class UserCreate(BaseModel):
    username: str
    email: str
    display_name: str

class PetAdopt(BaseModel):
    pet_type_id: int
    nickname: Optional[str] = None

class PointAdd(BaseModel):
    points: int
    reason: str
    category: str
    user_pet_id: Optional[int] = None

class FeedPet(BaseModel):
    food_points: int  # 消耗的积分数值
        .user-info {
            background: linear-gradient(135deg, #dfe6e9 0%, #b2bec3 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .user-info h3 {
            color: #2d3436;
            margin-bottom: 12px;
            font-size: 1.5em;
        }
        .user-info p {
            color: #636e72;
            margin: 8px 0;
            font-size: 1em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(102,126,234,0.3);
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 5px;
        }
        .leaderboard-item {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s;
        }
        .leaderboard-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .rank {
            background: #667eea;
            color: white;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        .rank.gold { background: linear-gradient(135deg, #FFD700, #FFA500); }
        .rank.silver { background: linear-gradient(135deg, #C0C0C0, #A0A0A0); }
        .rank.bronze { background: linear-gradient(135deg, #CD7F32, #B8860B); }
        .message {
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
            font-size: 1.1em;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
        }
        .message.info {
            background: #d1ecf1;
            color: #0c5460;
        .user-info {
            background: linear-gradient(135deg, #dfe6e9 0%, #b2bec3 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .user-info h3 {
            color: #2d3436;
            margin-bottom: 12px;
            font-size: 1.5em;
        }
        .user-info p {
            color: #636e72;
            margin: 8px 0;
            font-size: 1em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(102,126,234,0.3);
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 5px;
        }
        .leaderboard-item {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s;
        }
        .leaderboard-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .rank {
            background: #667eea;
            color: white;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        .rank.gold { background: linear-gradient(135deg, #FFD700, #FFA500); }
        .rank.silver { background: linear-gradient(135deg, #C0C0C0, #A0A0A0); }
        .rank.bronze { background: linear-gradient(135deg, #CD7F32, #B8860B); }
        .message {
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
            font-size: 1.1em;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
        }
        .message.info {
            background: #d1ecf1;
            color: #0c5460;
