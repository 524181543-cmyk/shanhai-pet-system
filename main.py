"""
山海经班级宠物积分系统 - 完整版
包含：用户注册、宠物领养、积分系统、排行榜
"""
import os
import sys
import logging
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
    version="1.0.0"
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.1em;
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .tab {
            background: white;
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
            flex: 1;
            min-width: 150px;
        }
        .tab:hover, .tab.active {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }
        .panel {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
        }
        .panel.active { display: block; }
        .pet-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .pet-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
            border-radius: 15px;
            padding: 25px 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 3px solid transparent;
        }
        .pet-card:hover {
            transform: translateY(-8px);
            border-color: #667eea;
            box-shadow: 0 15px 40px rgba(102,126,234,0.4);
        }
        .pet-icon { font-size: 4em; margin-bottom: 15px; }
        .pet-name { font-weight: bold; color: #333; font-size: 1.2em; margin-bottom: 5px; }
        .pet-desc { color: #666; font-size: 0.9em; }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .user-info {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .user-info h3 {
            color: #2e7d32;
            margin-bottom: 10px;
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
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .leaderboard-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .rank {
            background: #667eea;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        .rank.gold { background: #FFD700; color: #333; }
        .rank.silver { background: #C0C0C0; color: #333; }
        .rank.bronze { background: #CD7F32; color: white; }
        .message {
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 山海经班级宠物积分系统</h1>
            <p class="subtitle">领养你的专属神兽，开启奇幻之旅</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showPanel('adopt')">🐾 领养宠物</button>
            <button class="tab" onclick="showPanel('my-pet')">🎮 我的宠物</button>
            <button class="tab" onclick="showPanel('points')">⭐ 积分中心</button>
            <button class="tab" onclick="showPanel('leaderboard')">🏆 排行榜</button>
        </div>
        
        <!-- 领养宠物 -->
        <div id="adopt-panel" class="panel active">
            <div id="user-section">
                <h2>第一步：创建你的账号</h2>
                <div class="form-group">
                    <label>用户名</label>
                    <input type="text" id="username" placeholder="请输入用户名">
                </div>
                <div class="form-group">
                    <label>邮箱</label>
                    <input type="email" id="email" placeholder="请输入邮箱">
                </div>
                <div class="form-group">
                    <label>显示名称</label>
                    <input type="text" id="display_name" placeholder="请输入显示名称">
                </div>
                <button class="btn" onclick="createUser()">创建账号</button>
            </div>
            
            <div id="pet-section" style="display:none">
                <h2>第二步：选择你的神兽</h2>
                <div id="pets-list" class="pet-grid">
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>加载宠物中...</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- 我的宠物 -->
        <div id="my-pet-panel" class="panel">
            <div id="my-pet-content">
                <p class="message">请先领养宠物</p>
            </div>
        </div>
        
        <!-- 积分中心 -->
        <div id="points-panel" class="panel">
            <h2>添加积分</h2>
            <div id="points-user-info"></div>
            <div class="form-group">
                <label>积分数值</label>
                <input type="number" id="points-input" placeholder="请输入积分（正数增加，负数减少）">
            </div>
            <div class="form-group">
                <label>积分原因</label>
                <input type="text" id="reason-input" placeholder="例如：完成作业、表现优秀">
            </div>
            <div class="form-group">
                <label>积分类别</label>
                <select id="category-input">
                    <option value="作业">作业</option>
                    <option value="表现">表现</option>
                    <option value="奖励">奖励</option>
                    <option value="其他">其他</option>
                </select>
            </div>
            <button class="btn" onclick="addPoints()">添加积分</button>
            <div id="points-history" style="margin-top: 30px;">
                <h3>积分历史</h3>
                <div id="history-list"></div>
            </div>
        </div>
        
        <!-- 排行榜 -->
        <div id="leaderboard-panel" class="panel">
            <h2>🏆 积分排行榜</h2>
            <div id="leaderboard-list">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>加载排行榜...</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentUser = null;
        let currentPet = null;
        const API_BASE = '';
        
        // 显示面板
        function showPanel(name) {
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById(name + '-panel').classList.add('active');
            event.target.classList.add('active');
            
            if (name === 'leaderboard') loadLeaderboard();
            if (name === 'my-pet') loadMyPet();
            if (name === 'points') loadPointsInfo();
        }
        
        // 创建用户
        async function createUser() {
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const displayName = document.getElementById('display_name').value;
            
            if (!username || !email || !displayName) {
                alert('请填写所有字段');
                return;
            }
            
            try {
                const res = await fetch(API_BASE + '/api/users', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        username,
                        email,
                        display_name: displayName
                    })
                });
                
                const data = await res.json();
                
                if (data.success) {
                    currentUser = data.data;
                    localStorage.setItem('userId', currentUser.id);
                    document.getElementById('user-section').innerHTML = `
                        <div class="user-info">
                            <h3>✅ 欢迎，${currentUser.display_name}！</h3>
                            <p>用户名：${currentUser.username}</p>
                            <p>总积分：${currentUser.total_points}</p>
                        </div>
                    `;
                    document.getElementById('pet-section').style.display = 'block';
                    loadPets();
                } else {
                    alert('创建失败：' + (data.error || '未知错误'));
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            }
        }
        
        // 加载宠物列表
        async function loadPets() {
            try {
                const res = await fetch(API_BASE + '/api/pets/types');
                const data = await res.json();
                
                if (data.success) {
                    const petsHtml = data.data.map(pet => `
                        <div class="pet-card" onclick="adoptPet(${pet.id}, '${pet.name}')">
                            <div class="pet-icon">${pet.icon}</div>
                            <div class="pet-name">${pet.name}</div>
                            <div class="pet-desc">${pet.description}</div>
                        </div>
                    `).join('');
                    document.getElementById('pets-list').innerHTML = petsHtml;
                }
            } catch (e) {
                document.getElementById('pets-list').innerHTML = `
                    <div class="message error">加载失败：${e.message}</div>
                `;
            }
        }
        
        // 领养宠物
        async function adoptPet(petTypeId, petName) {
            if (!currentUser) {
                alert('请先创建账号');
                return;
            }
            
            const nickname = prompt('给你的宠物起个名字吧：', petName);
            
            try {
                const res = await fetch(API_BASE + `/api/users/${currentUser.id}/pets`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        pet_type_id: petTypeId,
                        nickname: nickname || petName
                    })
                });
                
                const data = await res.json();
                
                if (data.success) {
                    currentPet = data.data;
                    alert('🎉 恭喜你成功领养了' + nickname + '！');
                    showPanel('my-pet');
                } else {
                    alert('领养失败：' + (data.error || '未知错误'));
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            }
        }
        
        // 加载我的宠物
        async function loadMyPet() {
            const userId = currentUser?.id || localStorage.getItem('userId');
            if (!userId) {
                document.getElementById('my-pet-content').innerHTML = `
                    <div class="message">请先领养宠物</div>
                `;
                return;
            }
            
            try {
                const res = await fetch(API_BASE + `/api/users/${userId}/pets`);
                const data = await res.json();
                
                if (data.success && data.data.length > 0) {
                    const pet = data.data[0];
                    currentPet = pet;
                    document.getElementById('my-pet-content').innerHTML = `
                        <div class="user-info">
                            <h3>🎮 ${pet.nickname}</h3>
                            <p>类型：${pet.pet_types?.name || '未知'}</p>
                            <p>当前阶段：第${pet.current_stage}阶段</p>
                            <p>累计积分：${pet.total_points}</p>
                        </div>
                    `;
                } else {
                    document.getElementById('my-pet-content').innerHTML = `
                        <div class="message">你还没有领养宠物，快去领养一只吧！</div>
                    `;
                }
            } catch (e) {
                document.getElementById('my-pet-content').innerHTML = `
                    <div class="message error">加载失败：${e.message}</div>
                `;
            }
        }
        
        // 加载积分信息
        async function loadPointsInfo() {
            const userId = currentUser?.id || localStorage.getItem('userId');
            if (!userId) {
                document.getElementById('points-user-info').innerHTML = `
                    <div class="message">请先创建账号</div>
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
                    const historyData = await historyRes.json();
                    
                    if (historyData.success) {
                        const historyHtml = historyData.data.map(record => `
                            <div class="leaderboard-item">
                                <div class="rank" style="background: ${record.points > 0 ? '#4caf50' : '#f44336'}">
                                    ${record.points > 0 ? '+' : ''}${record.points}
                                </div>
                                <div>
                                    <div><strong>${record.reason}</strong></div>
                                    <div style="color: #666; font-size: 0.9em">${record.category} · ${new Date(record.created_at).toLocaleDateString()}</div>
                                </div>
                            </div>
                        `).join('');
                        document.getElementById('history-list').innerHTML = historyHtml || '<p>暂无记录</p>';
                    }
                }
            } catch (e) {
                console.error('加载积分信息失败:', e);
            }
        }
        
        // 添加积分
        async function addPoints() {
            const userId = currentUser?.id || localStorage.getItem('userId');
            if (!userId) {
                alert('请先创建账号');
                return;
            }
            
            const points = parseInt(document.getElementById('points-input').value);
            const reason = document.getElementById('reason-input').value;
            const category = document.getElementById('category-input').value;
            
            if (!points || !reason) {
                alert('请填写完整信息');
                return;
            }
            
            try {
                const res = await fetch(API_BASE + `/api/users/${userId}/points`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        points,
                        reason,
                        category,
                        user_pet_id: currentPet?.id
                    })
                });
                
                const data = await res.json();
                
                if (data.success) {
                    alert('✅ 积分添加成功！');
                    document.getElementById('points-input').value = '';
                    document.getElementById('reason-input').value = '';
                    loadPointsInfo();
                } else {
                    alert('添加失败：' + (data.error || '未知错误'));
                }
            } catch (e) {
                alert('请求失败：' + e.message);
            }
        }
        
        // 加载排行榜
        async function loadLeaderboard() {
            try {
                const res = await fetch(API_BASE + '/api/leaderboard');
                const data = await res.json();
                
                if (data.success) {
                    if (data.data.length === 0) {
                        document.getElementById('leaderboard-list').innerHTML = `
                            <div class="message">暂无排行数据</div>
                        `;
                        return;
                    }
                    
                    const leaderboardHtml = data.data.map((user, index) => {
                        const rankClass = index === 0 ? 'gold' : index === 1 ? 'silver' : index === 2 ? 'bronze' : '';
                        return `
                            <div class="leaderboard-item">
                                <div class="rank ${rankClass}">${index + 1}</div>
                                <div>
                                    <div><strong>${user.display_name}</strong></div>
                                    <div style="color: #666">@${user.username}</div>
                                </div>
                                <div style="margin-left: auto; font-size: 1.5em; font-weight: bold; color: #667eea">
                                    ${user.total_points} ⭐
                                </div>
                            </div>
                        `;
                    }).join('');
                    document.getElementById('leaderboard-list').innerHTML = leaderboardHtml;
                }
            } catch (e) {
                document.getElementById('leaderboard-list').innerHTML = `
                    <div class="message error">加载失败：${e.message}</div>
                `;
            }
        }
        
        // 页面加载时检查是否有用户
        window.onload = function() {
            const savedUserId = localStorage.getItem('userId');
            if (savedUserId) {
                fetch(API_BASE + `/api/users/${savedUserId}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            currentUser = data.data;
                            document.getElementById('user-section').innerHTML = `
                                <div class="user-info">
                                    <h3>✅ 欢迎回来，${currentUser.display_name}！</h3>
                                    <p>用户名：${currentUser.username}</p>
                                    <p>总积分：${currentUser.total_points}</p>
                                </div>
                            `;
                            document.getElementById('pet-section').style.display = 'block';
                            loadPets();
                        }
                    })
                    .catch(e => console.error(e));
            }
            
            loadLeaderboard();
        };
    </script>
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
    return {"status": "ok", "service": "山海经班级宠物积分系统", "version": "1.0.0"}

# ========== 用户API ==========

@app.post("/api/users")
async def create_user(user: UserCreate):
    """创建用户"""
    if not db:
        # 模拟数据模式
        return {
            "success": True,
            "data": {
                "id": 1,
                "username": user.username,
                "email": user.email,
                "display_name": user.display_name,
                "total_points": 0
            }
        }
    
    try:
        # 检查用户名是否存在
        existing = db.table('users').select('*').eq('username', user.username).execute()
        if existing.data:
            return JSONResponse(content={"success": False, "error": "用户名已存在"}, status_code=400)
        
        # 创建用户
        result = db.table('users').insert({
            'username': user.username,
            'email': user.email,
            'display_name': user.display_name,
            'total_points': 0
        }).execute()
        
        logger.info(f"创建用户成功: {user.username}")
        return {"success": True, "data": result.data[0]}
    except Exception as e:
        logger.error(f"创建用户失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """获取用户信息"""
    if not db:
        return {"success": True, "data": {"id": user_id, "username": "test", "display_name": "测试用户", "total_points": 100}}
    
    try:
        result = db.table('users').select('*').eq('id', user_id).execute()
        if not result.data:
            return JSONResponse(content={"success": False, "error": "用户不存在"}, status_code=404)
        return {"success": True, "data": result.data[0]}
    except Exception as e:
        logger.error(f"获取用户失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

# ========== 宠物类型API ==========

@app.get("/api/pets/types")
async def get_pet_types():
    """获取所有宠物类型"""
    if not db:
        # 模拟数据
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
    
    try:
        result = db.table('pet_types').select('*').execute()
        # 添加emoji图标
        icons = {'麒麟': '🐉', '凤凰': '🦅', '九尾狐': '🦊', '玄武': '🐢', '白虎': '🐯', '青龙': '🐲'}
        for pet in result.data:
            pet['icon'] = icons.get(pet['name'], '🐉')
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"获取宠物类型失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

# ========== 用户宠物API ==========

@app.post("/api/users/{user_id}/pets")
async def adopt_pet(user_id: int, pet: PetAdopt):
    """领养宠物"""
    if not db:
        return {
            "success": True,
            "data": {
                "id": 1,
                "user_id": user_id,
                "pet_type_id": pet.pet_type_id,
                "nickname": pet.nickname or "宠物",
                "current_stage": 1,
                "total_points": 0,
                "pet_types": {"name": "麒麟"}
            }
        }
    
    try:
        # 检查是否已有宠物
        existing = db.table('user_pets').select('*').eq('user_id', user_id).execute()
        if existing.data:
            return JSONResponse(content={"success": False, "error": "该用户已有宠物"}, status_code=400)
        
        # 领养宠物
        result = db.table('user_pets').insert({
            'user_id': user_id,
            'pet_type_id': pet.pet_type_id,
            'nickname': pet.nickname or '宠物',
            'current_stage': 1,
            'total_points': 0,
            'unlocked_stages': {'1': True},
            'unlocked_skills': {}
        }).execute()
        
        # 获取宠物类型信息
        pet_type = db.table('pet_types').select('*').eq('id', pet.pet_type_id).execute()
        result.data[0]['pet_types'] = pet_type.data[0] if pet_type.data else {}
        
        logger.info(f"用户 {user_id} 领养宠物成功")
        return {"success": True, "data": result.data[0]}
    except Exception as e:
        logger.error(f"领养宠物失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

@app.get("/api/users/{user_id}/pets")
async def get_user_pets(user_id: int):
    """获取用户的宠物"""
    if not db:
        return {"success": True, "data": []}
    
    try:
        result = db.table('user_pets').select('*, pet_types(*)').eq('user_id', user_id).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"获取用户宠物失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

# ========== 积分API ==========

@app.post("/api/users/{user_id}/points")
async def add_points(user_id: int, point: PointAdd):
    """添加积分"""
    if not db:
        return {"success": True, "data": {"id": 1, "points": point.points}}
    
    try:
        # 创建积分记录
        record = db.table('point_records').insert({
            'user_id': user_id,
            'points': point.points,
            'reason': point.reason,
            'category': point.category,
            'user_pet_id': point.user_pet_id
        }).execute()
        
        # 更新用户总积分
        user = db.table('users').select('total_points').eq('id', user_id).execute()
        if user.data:
            new_total = user.data[0]['total_points'] + point.points
            db.table('users').update({'total_points': new_total}).eq('id', user_id).execute()
        
        # 更新宠物积分
        if point.user_pet_id:
            pet = db.table('user_pets').select('total_points').eq('id', point.user_pet_id).execute()
            if pet.data:
                new_pet_total = pet.data[0]['total_points'] + point.points
                db.table('user_pets').update({'total_points': new_pet_total}).eq('id', point.user_pet_id).execute()
        
        logger.info(f"用户 {user_id} 获得 {point.points} 积分")
        return {"success": True, "data": record.data[0]}
    except Exception as e:
        logger.error(f"添加积分失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

@app.get("/api/users/{user_id}/points/records")
async def get_point_records(user_id: int, limit: int = 20):
    """获取积分记录"""
    if not db:
        return {"success": True, "data": []}
    
    try:
        result = db.table('point_records').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"获取积分记录失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

# ========== 排行榜API ==========

@app.get("/api/leaderboard")
async def get_leaderboard(limit: int = 10):
    """获取排行榜"""
    if not db:
        return {"success": True, "data": []}
    
    try:
        result = db.table('users').select('id, username, display_name, total_points').order('total_points', desc=True).limit(limit).execute()
        return {"success": True, "data": result.data}
    except Exception as e:
        logger.error(f"获取排行榜失败: {str(e)}")
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

# ========== 启动 ==========

@app.on_event("startup")
async def startup():
    port = os.environ.get("PORT", "8000")
    logger.info("=" * 60)
    logger.info("🐉 山海经班级宠物积分系统 v1.0")
    logger.info(f"🌐 端口: {port}")
    logger.info("=" * 60)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
