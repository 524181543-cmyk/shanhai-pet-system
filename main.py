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
from fastapi.responses import HTMLResponse, JSONResponse
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
    version="2.0.0"
)

# 初始化Supabase客户端
try:
    from storage.database.supabase_client import get_supabase_client
    db = get_supabase_client()
    logger.info("✅ 数据库连接成功")
except Exception as e:
    logger.warning(f"⚠️ 数据库连接失败: {str(e)}")
    logger.info("使用模拟数据模式...")
    db = None

# ========== 模拟数据存储 ==========
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

# ========== 前端页面 ==========

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
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
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
        }
        
        /* 神兽描述 */
        .beast-description {
            background: rgba(0,0,0,0.05);
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 0 10px 10px 0;
            font-style: italic;
            color: #636e72;
        }
        
        /* 喂养动画 */
        @keyframes feed-animation {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1); }
        }
        .feeding {
            animation: feed-animation 0.5s ease;
                       if (currentUser.total_points < points) {
                alert('积分不足！当前积分：' + currentUser.total_points);
                return;
            }
            
            try {
                // 扣除积分
                const res = await fetch(API_BASE + `/api/users/${currentUser.id}/points`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        points: -points,
                        reason: '喂养' + currentPet.nickname,
                        category: '喂养',
                        user_pet_id: currentPet.id
                    })
                });
                
                const data = await res.json();
                
                if (data.success) {
                    // 更新饱食度
                    currentPet.hunger = Math.min(100, currentPet.hunger + points);
                    currentUser.total_points -= points;
                    
                    // 更新UI
                    document.getElementById('hunger-value').textContent = currentPet.hunger + '%';
                    document.getElementById('hunger-fill').style.width = currentPet.hunger + '%';
                    
                    // 喂养动画
                    const beast = document.getElementById('pet-beast');
                    beast.classList.add('feeding');
                    setTimeout(() => beast.classList.remove('feeding'), 500);
                    
                    alert('✅ 喂养成功！' + currentPet.nickname + '的饱食度提升了！');
                } else {
                    alert('喂养失败：' + (data.error || '未知错误'));
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            }
        }
        
        // 加载积分信息
        async function loadPointsInfo() {
            const userId = currentUser?.id || localStorage.getItem('userId');
            if (!userId) {
                document.getElementById('points-user-info').innerHTML = `
                    <div class="message info">请先创建账号</div>
                `;
                return;
            }
            
            try {
                const res = await fetch(API_BASE + `/api/users/${userId}`);
                const data = await res.json();
                
                if (data.success) {
                    currentUser = data.data;
                    document.getElementById('points-user-info').innerHTML = `
                        <div class="stats">
                            <div class="stat-card">
                                <div class="stat-value">${currentUser.total_points}</div>
                                <div class="stat-label">总积分</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${currentUser.display_name}</div>
                                <div class="stat-label">用户名</div>
                            </div>
                        </div>
                    `;
                    
                    // 加载积分历史
                    const historyRes = await fetch(API_BASE + `/api/users/${userId}/points/records`);
