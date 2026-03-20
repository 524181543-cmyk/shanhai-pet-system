"""
山海经班级宠物积分系统 - 完整版 V3
修复：Railway 健康检查问题
"""
import os
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
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
    version="3.0.0",
    docs_url=None,
    redoc_url=None
)

# ========== 健康检查端点（Railway 使用）==========

@app.get("/health")
async def health():
    """健康检查 - Railway 使用此端点检查服务状态"""
    return {"status": "ok", "service": "山海经班级宠物积分系统"}

@app.get("/")
async def index():
    """首页 - 返回HTML页面"""
    return HTMLResponse(content=INDEX_HTML, status_code=200)

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
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff);
            animation: rainbow 3s linear infinite;
        }
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }
        h1 {
            color: #2d3436;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle { text-align: center; color: #636e72; font-size: 1.1em; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .tab {
            background: rgba(255,255,255,0.9);
            border: none;
            padding: 15px 25px;
            border-radius: 15px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #2d3436;
            transition: all 0.3s;
            flex: 1;
            min-width: 150px;
        }
        .tab:hover, .tab.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            transform: translateY(-3px);
        }
        .panel {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            display: none;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .panel.active { display: block; }
        .pet-3d-container {
            width: 100%;
            height: 400px;
            perspective: 1000px;
            margin: 20px 0;
            position: relative;
            background: radial-gradient(circle, rgba(102,126,234,0.1), transparent);
            border-radius: 20px;
            overflow: hidden;
        }
        .pet-3d-stage {
            width: 100%;
            height: 100%;
            position: relative;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
        .beast {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            font-size: 150px;
            filter: drop-shadow(0 20px 40px rgba(0,0,0,0.3));
            animation: breathe 2s ease-in-out infinite;
        }
        @keyframes breathe { 0%, 100% { transform: translate(-50%, -50%) scale(1); } 50% { transform: translate(-50%, -50%) scale(1.05); } }
        .beast-glow {
            position: absolute;
            left: 50%;
            top: 50%;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            animation: pulse 2s ease-in-out infinite;
            opacity: 0.5;
        }
        @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; } 50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.6; } }
        .qilin { animation: qilin-move 4s ease-in-out infinite; }
        @keyframes qilin-move { 0%, 100% { transform: translate(-50%, -50%) rotate(-5deg); } 50% { transform: translate(-50%, -50%) rotate(5deg); } }
        .qilin-glow { background: radial-gradient(circle, #ffd700, transparent); }
        .fenghuang { animation: fenghuang-fly 3s ease-in-out infinite; }
        @keyframes fenghuang-fly { 0%, 100% { transform: translate(-50%, -50%) translateY(0) rotateY(0deg); } 50% { transform: translate(-50%, -60%) translateY(-20px) rotateY(180deg); } }
        .fenghuang-glow { background: radial-gradient(circle, #ff6b6b, transparent); }
        .jiuweihu { animation: jiuweihu-dance 2.5s ease-in-out infinite; }
        @keyframes jiuweihu-dance { 0%, 100% { transform: translate(-50%, -50%) rotate(-3deg); } 50% { transform: translate(-50%, -50%) rotate(3deg); } }
        .jiuweihu-glow { background: radial-gradient(circle, #ff9ff3, transparent); }
        .xuanwu { animation: xuanwu-swim 5s ease-in-out infinite; }
        @keyframes xuanwu-swim { 0%, 100% { transform: translate(-50%, -50%) translateX(0); } 50% { transform: translate(-50%, -50%) translateX(20px); } }
        .xuanwu-glow { background: radial-gradient(circle, #48dbfb, transparent); }
        .baihu { animation: baihu-pounce 2s ease-in-out infinite; }
        @keyframes baihu-pounce { 0%, 100% { transform: translate(-50%, -50%) scale(1); } 50% { transform: translate(-50%, -45%) scale(1.1); } }
        .baihu-glow { background: radial-gradient(circle, #fff, transparent); }
        .qinglong { animation: qinglong-fly 4s ease-in-out infinite; }
        @keyframes qinglong-fly { 0%, 100% { transform: translate(-50%, -50%) rotateZ(-5deg) translateY(0); } 50% { transform: translate(-50%, -50%) rotateZ(5deg) translateY(-15px); } }
        .qinglong-glow { background: radial-gradient(circle, #54a0ff, transparent); }
        .pet-info-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
        }
        .pet-info-card h3 { font-size: 1.8em; margin-bottom: 15px; }
        .pet-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin-top: 15px; }
        .pet-stat { background: rgba(255,255,255,0.2); padding: 15px; border-radius: 12px; text-align: center; }
        .pet-stat-value { font-size: 1.8em; font-weight: bold; }
        .pet-stat-label { font-size: 0.85em; opacity: 0.9; }
        .hunger-bar { background: rgba(255,255,255,0.3); height: 20px; border-radius: 10px; overflow: hidden; margin: 15px 0; }
        .hunger-fill { height: 100%; background: linear-gradient(90deg, #feca57, #ff6b6b); transition: width 0.5s; }
        .feed-btn {
            background: linear-gradient(135deg, #feca57, #ff9ff3);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s;
        }
        .feed-btn:hover { transform: translateY(-3px) scale(1.05); }
        .particles { position: absolute; width: 100%; height: 100%; overflow: hidden; pointer-events: none; }
        .particle { position: absolute; width: 10px; height: 10px; border-radius: 50%; animation: particle-float 3s ease-in-out infinite; }
        @keyframes particle-float { 0%, 100% { transform: translateY(0); opacity: 0; } 50% { transform: translateY(-100px); opacity: 1; } }
        .pet-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .pet-card {
            background: linear-gradient(135deg, #f5f7fa, #e8ecef);
            border-radius: 20px;
            padding: 30px 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s;
            border: 3px solid transparent;
        }
        .pet-card:hover { transform: translateY(-10px); border-color: #667eea; box-shadow: 0 20px 50px rgba(102,126,234,0.4); }
        .pet-card-icon { font-size: 5em; margin-bottom: 15px; }
        .pet-name { font-weight: bold; color: #2d3436; font-size: 1.3em; margin-bottom: 8px; }
        .pet-desc { color: #636e72; font-size: 0.9em; }
        .pet-element { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.8em; margin-top: 10px; display: inline-block; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #2d3436; }
        .form-group input, .form-group select { width: 100%; padding: 14px; border: 2px solid #dfe6e9; border-radius: 12px; font-size: 1em; }
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 16px 35px;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
        }
        .btn:hover { transform: translateY(-2px); }
        .user-info { background: linear-gradient(135deg, #dfe6e9, #b2bec3); padding: 25px; border-radius: 15px; margin-bottom: 20px; }
        .user-info h3 { color: #2d3436; margin-bottom: 12px; }
        .user-info p { color: #636e72; margin: 8px 0; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-card { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 25px; border-radius: 15px; text-align: center; }
        .stat-value { font-size: 2.5em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.9; }
        .leaderboard-item { background: linear-gradient(135deg, #f5f7fa, #e8ecef); padding: 18px; border-radius: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 15px; }
        .rank { background: #667eea; color: white; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .rank.gold { background: linear-gradient(135deg, #FFD700, #FFA500); }
        .rank.silver { background: linear-gradient(135deg, #C0C0C0, #A0A0A0); }
        .rank.bronze { background: linear-gradient(135deg, #CD7F32, #B8860B); }
        .message { padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center; }
        .message.success { background: #d4edda; color: #155724; }
        .message.error { background: #f8d7da; color: #721c24; }
        .message.info { background: #d1ecf1; color: #0c5460; }
        .beast-description { background: rgba(0,0,0,0.05); border-left: 4px solid #667eea; padding: 15px 20px; margin: 15px 0; border-radius: 0 10px 10px 0; font-style: italic; color: #636e72; }
        .feeding { animation: feed-animation 0.5s ease; }
        @keyframes feed-animation { 0% { transform: scale(1); } 50% { transform: scale(1.3); } 100% { transform: scale(1); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 山海经班级宠物积分系统</h1>
            <p class="subtitle">领养你的专属神兽，开启奇幻之旅</p>
        </div>
        <div class="tabs">
            <button class="tab active" onclick="showPanel('adopt', this)">🐾 领养宠物</button>
            <button class="tab" onclick="showPanel('my-pet', this)">🎮 我的宠物</button>
            <button class="tab" onclick="showPanel('points', this)">⭐ 积分中心</button>
            <button class="tab" onclick="showPanel('leaderboard', this)">🏆 排行榜</button>
        </div>
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
                <div id="pets-list" class="pet-grid"></div>
            </div>
        </div>
        <div id="my-pet-panel" class="panel">
            <div id="my-pet-content"><p class="message info">请先领养宠物</p></div>
        </div>
        <div id="points-panel" class="panel">
            <h2>⭐ 积分管理</h2>
            <div id="points-user-info"></div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div>
                    <h3 style="margin-bottom: 15px;">添加积分</h3>
                    <div class="form-group">
                        <label>积分数值</label>
                        <input type="number" id="points-input" placeholder="正数增加，负数减少">
                    </div>
                    <div class="form-group">
                        <label>积分原因</label>
                        <input type="text" id="reason-input" placeholder="例如：完成作业">
                    </div>
                    <div class="form-group">
                        <label>积分类别</label>
                        <select id="category-input">
                            <option value="作业">📝 作业</option>
                            <option value="表现">⭐ 表现</option>
                            <option value="奖励">🎁 奖励</option>
                            <option value="其他">📌 其他</option>
                        </select>
                    </div>
                    <button class="btn" onclick="addPoints()">添加积分</button>
                </div>
                <div id="points-history"><h3>积分历史</h3><div id="history-list"></div></div>
            </div>
        </div>
        <div id="leaderboard-panel" class="panel">
            <h2>🏆 积分排行榜</h2>
            <div id="leaderboard-list"></div>
        </div>
    </div>
    <script>
        let currentUser = null;
        let currentPet = null;
        const BEASTS = {
            1: { name: '麒麟', icon: '🐉', element: '土', rarity: '传说', description: '《山海经》记载：麒麟能活两千年，性情温和，不履生虫，不折生草。', color: '#ffd700' },
            2: { name: '凤凰', icon: '🦅', element: '火', rarity: '传说', description: '《山海经》记载：丹穴之山有鸟焉，五采而文，名曰凤凰。浴火重生。', color: '#ff6b6b' },
            3: { name: '九尾狐', icon: '🦊', element: '幻', rarity: '史诗', description: '《山海经》记载：青丘之山有兽焉，其状如狐而九尾。通灵达意。', color: '#ff9ff3' },
            4: { name: '玄武', icon: '🐢', element: '水', rarity: '传说', description: '《山海经》记载：北方之神，龟蛇合体。司水，防御无双。', color: '#48dbfb' },
            5: { name: '白虎', icon: '🐯', element: '金', rarity: '传说', description: '《山海经》记载：西方之神，主杀伐。威猛无匹，百兽震惶。', color: '#ffffff' },
            6: { name: '青龙', icon: '🐲', element: '木', rarity: '传说', description: '《山海经》记载：东方之神，主生机。腾云驾雾，呼风唤雨。', color: '#54a0ff' }
        };
        function showPanel(name, btn) {
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById(name + '-panel').classList.add('active');
            if (btn) btn.classList.add('active');
            if (name === 'leaderboard') loadLeaderboard();
            if (name === 'my-pet') loadMyPet();
            if (name === 'points') loadPointsInfo();
        }
        async function createUser() {
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const displayName = document.getElementById('display_name').value;
            if (!username || !email || !displayName) { alert('请填写所有字段'); return; }
            try {
                const res = await fetch('/api/users', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ username, email, display_name: displayName }) });
                const data = await res.json();
                if (data.success) {
                    currentUser = data.data;
                    localStorage.setItem('userId', currentUser.id);
                    document.getElementById('user-section').innerHTML = '<div class="user-info"><h3>✅ 欢迎，' + currentUser.display_name + '！</h3><p>总积分：' + currentUser.total_points + '</p></div>';
                    document.getElementById('pet-section').style.display = 'block';
                    loadPets();
                } else { alert('创建失败：' + (data.error || '未知错误')); }
            } catch (e) { alert('请求失败：' + e.message); }
        }
        async function loadPets() {
            try {
                const res = await fetch('/api/pets/types');
                const data = await res.json();
                if (data.success) {
                    const petsHtml = data.data.map(pet => {
                        const beast = BEASTS[pet.id];
                        return '<div class="pet-card" onclick="adoptPet(' + pet.id + ', \'' + pet.name + '\')"><div class="pet-card-icon">' + pet.icon + '</div><div class="pet-name">' + pet.name + '</div><div class="pet-desc">' + pet.description + '</div><div class="pet-element">' + beast.element + '属性 · ' + beast.rarity + '</div></div>';
                    }).join('');
                    document.getElementById('pets-list').innerHTML = petsHtml;
                }
            } catch (e) { document.getElementById('pets-list').innerHTML = '<div class="message error">加载失败：' + e.message + '</div>'; }
        }
        async function adoptPet(petTypeId, petName) {
            if (!currentUser) { alert('请先创建账号'); return; }
            const nickname = prompt('给你的' + petName + '起个名字：', petName);
            try {
                const res = await fetch('/api/users/' + currentUser.id + '/pets', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ pet_type_id: petTypeId, nickname: nickname || petName }) });
                const data = await res.json();
                if (data.success) {
                    currentPet = data.data;
                    currentPet.hunger = 50;
                    alert('🎉 恭喜领养成功！');
                    showPanel('my-pet', document.querySelector('[onclick*="my-pet"]'));
                } else { alert('领养失败：' + (data.error || '未知错误')); }
            } catch (e) { alert('请求失败：' + e.message); }
        }
        async function loadMyPet() {
            const userId = currentUser?.id || localStorage.getItem('userId');
            if (!userId) { document.getElementById('my-pet-content').innerHTML = '<div class="message info">请先领养宠物</div>'; return; }
            try {
                const res = await fetch('/api/users/' + userId + '/pets');
                const data = await res.json();
                if (data.success && data.data.length > 0) {
                    const pet = data.data[0];
                    currentPet = pet;
                    if (!pet.hunger) pet.hunger = 50;
                    currentPet.hunger = pet.hunger;
                    const beast = BEASTS[pet.pet_type_id];
                    const beastClass = beast.name.toLowerCase().replace(/[^\\w]/g, '');
                    document.getElementById('my-pet-content').innerHTML = '<div class="pet-3d-container"><div class="pet-3d-stage"><div class="beast-glow ' + beastClass + '-glow"></div><div class="beast ' + beastClass + '" id="pet-beast">' + (pet.icon || beast.icon) + '</div><div class="particles">' + generateParticles(beast.color) + '</div></div></div><div class="pet-info-card"><h3>' + (pet.icon || beast.icon) + ' ' + pet.nickname + '</h3><div class="beast-description">' + beast.description + '</div><div class="pet-stats"><div class="pet-stat"><div class="pet-stat-value">' + pet.current_stage + '</div><div class="pet-stat-label">进化阶段</div></div><div class="pet-stat"><div class="pet-stat-value">' + pet.total_points + '</div><div class="pet-stat-label">累计积分</div></div><div class="pet-stat"><div class="pet-stat-value">' + beast.element + '</div><div class="pet-stat-label">元素属性</div></div></div><div style="margin-top: 20px;"><div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>🍖 饱食度</span><span id="hunger-value">' + pet.hunger + '%</span></div><div class="hunger-bar"><div class="hunger-fill" id="hunger-fill" style="width: ' + pet.hunger + '%"></div></div></div></div><div style="text-align: center; margin-top: 20px;"><h3>喂养你的神兽</h3><p style="color: #636e72; margin-bottom: 15px;">消耗积分喂养神兽，提升饱食度</p><button class="feed-btn" onclick="feedPet(10)">🍎 喂养10积分</button><button class="feed-btn" onclick="feedPet(30)">🥩 喂养30积分</button><button class="feed-btn" onclick="feedPet(50)">🍗 喂养50积分</button></div>';
                } else { document.getElementById('my-pet-content').innerHTML = '<div class="message info">还没有领养宠物</div>'; }
            } catch (e) { document.getElementById('my-pet-content').innerHTML = '<div class="message error">加载失败：' + e.message + '</div>'; }
        }
        function generateParticles(color) {
            let particles = '';
            for (let i = 0; i < 10; i++) { particles += '<div class="particle" style="left: ' + (Math.random() * 100) + '%; animation-delay: ' + (Math.random() * 3) + 's; background: ' + color + ';"></div>'; }
            return particles;
        }
        async function feedPet(points) {
            if (!currentUser || !currentPet) { alert('请先领养宠物'); return; }
            if (currentUser.total_points < points) { alert('积分不足！当前积分：' + currentUser.total_points); return; }
            try {
                const res = await fetch('/api/users/' + currentUser.id + '/points', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ points: -points, reason: '喂养' + currentPet.nickname, category: '喂养', user_pet_id: currentPet.id }) });
                const data = await res.json();
                if (data.success) {
                    currentPet.hunger = Math.min(100, currentPet.hunger + points);
                    currentUser.total_points -= points;
                    document.getElementById('hunger-value').textContent = currentPet.hunger + '%';
                    document.getElementById('hunger-fill').style.width = currentPet.hunger + '%';
                    const beast = document.getElementById('pet-beast');
                    beast.classList.add('feeding');
                    setTimeout(() => beast.classList.remove('feeding'), 500);
                    alert('✅ 喂养成功！');
                } else { alert('喂养失败：' + (data.error || '未知错误')); }
            } catch (e) { alert('请求失败：' + e.message); }
        }
        async function loadPointsInfo() {
            const userId = currentUser?.id || localStorage.getItem('userId');
            if (!userId) { document.getElementById('points-user-info').innerHTML = '<div class="message info">请先创建账号</div>'; return; }
            try {
                const res = await fetch('/api/users/' + userId);
                const data = await res.json();
                if (data.success) {
                    currentUser = data.data;
                    document.getElementById('points-user-info').innerHTML = '<div class="stats"><div class="stat-card"><div class="stat-value">' + currentUser.total_points + '</div><div class="stat-label">总积分</div></div><div class="stat-card"><div class="stat-value">' + currentUser.display_name + '</div><div class="stat-label">用户名</div></div></div>';
                    const historyRes = await fetch('/api/users/' + userId + '/points/records');
                    const historyData = await historyRes.json();
                    if (historyData.success) {
                        const historyHtml = historyData.data.map(record => '<div class="leaderboard-item"><div class="rank" style="background: ' + (record.points > 0 ? 'linear-gradient(135deg, #4caf50, #2e7d32)' : 'linear-gradient(135deg, #f44336, #c62828)') + '">' + (record.points > 0 ? '+' : '') + record.points + '</div><div style="flex: 1"><div><strong>' + record.reason + '</strong></div><div style="color: #636e72; font-size: 0.85em">' + record.category + '</div></div></div>').join('');
                        document.getElementById('history-list').innerHTML = historyHtml || '<p style="color: #636e72;">暂无记录</p>';
                    }
                }
            } catch (e) { console.error(e); }
        }
        async function addPoints() {
            const userId = currentUser?.id || localStorage.getItem('userId');
            if (!userId) { alert('请先创建账号'); return; }
            const points = parseInt(document.getElementById('points-input').value);
            const reason = document.getElementById('reason-input').value;
            const category = document.getElementById('category-input').value;
            if (!points || !reason) { alert('请填写完整信息'); return; }
            try {
                const res = await fetch('/api/users/' + userId + '/points', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ points, reason, category, user_pet_id: currentPet?.id }) });
                const data = await res.json();
                if (data.success) {
                    currentUser.total_points = (currentUser.total_points || 0) + points;
                    alert('✅ 积分添加成功！');
                    document.getElementById('points-input').value = '';
                    document.getElementById('reason-input').value = '';
                    loadPointsInfo();
                } else { alert('添加失败：' + (data.error || '未知错误')); }
            } catch (e) { alert('请求失败：' + e.message); }
        }
        async function loadLeaderboard() {
            try {
                const res = await fetch('/api/leaderboard');
                const data = await res.json();
                if (data.success) {
                    if (data.data.length === 0) { document.getElementById('leaderboard-list').innerHTML = '<div class="message info">暂无排行数据</div>'; return; }
                    const leaderboardHtml = data.data.map((user, index) => {
                        const rankClass = index === 0 ? 'gold' : index === 1 ? 'silver' : index === 2 ? 'bronze' : '';
                        return '<div class="leaderboard-item"><div class="rank ' + rankClass + '">' + (index + 1) + '</div><div style="flex: 1"><div><strong>' + user.display_name + '</strong></div><div style="color: #636e72; font-size: 0.85em">@' + user.username + '</div></div><div style="font-size: 1.8em; font-weight: bold; color: #667eea">' + user.total_points + ' ⭐</div></div>';
                    }).join('');
                    document.getElementById('leaderboard-list').innerHTML = leaderboardHtml;
                }
            } catch (e) { document.getElementById('leaderboard-list').innerHTML = '<div class="message error">加载失败：' + e.message + '</div>'; }
        }
        window.onload = function() {
            const savedUserId = localStorage.getItem('userId');
            if (savedUserId) {
                fetch('/api/users/' + savedUserId).then(res => res.json()).then(data => {
                    if (data.success) {
                        currentUser = data.data;
                        document.getElementById('user-section').innerHTML = '<div class="user-info"><h3>✅ 欢迎回来，' + currentUser.display_name + '！</h3><p>总积分：' + currentUser.total_points + '</p></div>';
                        document.getElementById('pet-section').style.display = 'block';
                        loadPets();
                    }
                }).catch(e => console.error(e));
            }
            loadLeaderboard();
        };
    </script>
</body>
</html>
"""

# ========== 首页 ==========

# ========== 用户API ==========

@app.post("/api/users")
async def create_user(user: UserCreate):
    """创建用户"""
    user_id = mock_db['next_user_id']
    mock_db['next_user_id'] += 1
    new_user = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "display_name": user.display_name,
        "total_points": 0
    }
    mock_db['users'][user_id] = new_user
    logger.info(f"创建用户 {user.username}")
    return {"success": True, "data": new_user}

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """获取用户"""
    user = mock_db['users'].get(user_id)
    if not user:
        return JSONResponse(content={"success": False, "error": "用户不存在"}, status_code=404)
    return {"success": True, "data": user}

# ========== 宠物API ==========

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

@app.post("/api/users/{user_id}/pets")
async def adopt_pet(user_id: int, pet: PetAdopt):
    """领养宠物"""
    for p in mock_db['user_pets'].values():
        if p['user_id'] == user_id:
            return JSONResponse(content={"success": False, "error": "已有宠物"}, status_code=400)
    pet_names = {1: '麒麟', 2: '凤凰', 3: '九尾狐', 4: '玄武', 5: '白虎', 6: '青龙'}
    pet_icons = {1: '🐉', 2: '🦅', 3: '🦊', 4: '🐢', 5: '🐯', 6: '🐲'}
    pet_id = mock_db['next_pet_id']
    mock_db['next_pet_id'] += 1
    new_pet = {
        "id": pet_id,
        "user_id": user_id,
        "pet_type_id": pet.pet_type_id,
        "nickname": pet.nickname or pet_names.get(pet.pet_type_id, '宠物'),
        "icon": pet_icons.get(pet.pet_type_id, '🐉'),
        "current_stage": 1,
        "total_points": 0,
        "hunger": 50
    }
    mock_db['user_pets'][pet_id] = new_pet
    logger.info(f"用户 {user_id} 领养宠物")
    return {"success": True, "data": new_pet}

@app.get("/api/users/{user_id}/pets")
async def get_user_pets(user_id: int):
    """获取用户宠物"""
    pets = [p for p in mock_db['user_pets'].values() if p['user_id'] == user_id]
    return {"success": True, "data": pets}

# ========== 积分API ==========

@app.post("/api/users/{user_id}/points")
async def add_points(user_id: int, point: PointAdd):
    """添加积分"""
    record = {
        "id": len(mock_db['point_records']) + 1,
        "user_id": user_id,
        "points": point.points,
        "reason": point.reason,
        "category": point.category,
        "created_at": datetime.now().isoformat()
    }
    mock_db['point_records'].append(record)
    if user_id in mock_db['users']:
        mock_db['users'][user_id]['total_points'] += point.points
    if point.user_pet_id and point.user_pet_id in mock_db['user_pets']:
        mock_db['user_pets'][point.user_pet_id]['total_points'] += point.points
    logger.info(f"用户 {user_id} 积分变动 {point.points}")
    return {"success": True, "data": record}

@app.get("/api/users/{user_id}/points/records")
async def get_point_records(user_id: int, limit: int = 20):
    """获取积分记录"""
    records = [r for r in mock_db['point_records'] if r['user_id'] == user_id]
    return {"success": True, "data": records[-limit:]}

# ========== 排行榜 ==========

@app.get("/api/leaderboard")
async def get_leaderboard(limit: int = 10):
    """获取排行榜"""
    users = sorted(mock_db['users'].values(), key=lambda x: x['total_points'], reverse=True)
    return {"success": True, "data": users[:limit]}

# ========== 启动 ==========

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🚀 启动服务，端口: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
