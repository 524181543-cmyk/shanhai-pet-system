"""
山海经班级宠物积分系统 - FastAPI集成
将Flask应用集成到FastAPI主服务中
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import sys
import json
from typing import Optional

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from storage.database.supabase_client import get_supabase_client
from utils.logger import setup_logger

logger = setup_logger(__name__)

# 初始化Supabase客户端
db_client = get_supabase_client()


def create_pet_routes(app: FastAPI):
    """为FastAPI应用添加宠物系统的路由"""
    
    # ========== 前端页面 ==========
    
    @app.get("/", response_class=HTMLResponse)
    async def index():
        """返回前端页面"""
        try:
            frontend_path = os.path.join(project_root, 'src', 'frontend', 'index.html')
            with open(frontend_path, 'r', encoding='utf-8') as f:
                return HTMLResponse(content=f.read(), status_code=200)
        except Exception as e:
            logger.error(f"读取前端页面失败: {str(e)}")
            return JSONResponse(content={'error': '页面不存在'}, status_code=404)
    
    # ========== 用户相关API ==========
    
    @app.post("/api/users")
    async def create_user(request: Request):
        """创建用户"""
        try:
            data = await request.json()
            username = data.get('username')
            email = data.get('email')
            display_name = data.get('display_name')
            
            if not all([username, email, display_name]):
                return JSONResponse(content={'error': '缺少必要参数'}, status_code=400)
            
            # 检查用户名是否已存在
            existing = db_client.table('users').select('*').eq('username', username).execute()
            if existing.data:
                return JSONResponse(content={'error': '用户名已存在'}, status_code=400)
            
            # 创建用户
            user_data = {
                'username': username,
                'email': email,
                'display_name': display_name,
                'total_points': 0
            }
            
            result = db_client.table('users').insert(user_data).execute()
            
            logger.info(f"创建用户成功: {username}")
            return JSONResponse(content={'success': True, 'data': result.data[0]}, status_code=201)
            
        except Exception as e:
            logger.error(f"创建用户失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    @app.get("/api/users/{user_id}")
    async def get_user(user_id: int):
        """获取用户信息"""
        try:
            result = db_client.table('users').select('*').eq('id', user_id).execute()
            
            if not result.data:
                return JSONResponse(content={'error': '用户不存在'}, status_code=404)
            
            return JSONResponse(content={'success': True, 'data': result.data[0]}, status_code=200)
            
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    # ========== 宠物类型相关API ==========
    
    @app.get("/api/pets/types")
    async def get_pet_types():
        """获取所有宠物类型（山海经生物）"""
        try:
            result = db_client.table('pet_types').select('*').execute()
            return JSONResponse(content={'success': True, 'data': result.data}, status_code=200)
            
        except Exception as e:
            logger.error(f"获取宠物类型失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    @app.get("/api/pets/types/{pet_type_id}")
    async def get_pet_type_detail(pet_type_id: int):
        """获取宠物类型详情（包含进化阶段）"""
        try:
            # 获取宠物类型
            pet_type = db_client.table('pet_types').select('*').eq('id', pet_type_id).execute()
            if not pet_type.data:
                return JSONResponse(content={'error': '宠物类型不存在'}, status_code=404)
            
            # 获取该宠物的所有进化阶段
            stages = db_client.table('pet_stages').select('*').eq('pet_type_id', pet_type_id).order('stage_level').execute()
            
            # 获取该宠物的所有技能
            skills = db_client.table('pet_skills').select('*').eq('pet_type_id', pet_type_id).order('stage_level').execute()
            
            result = {
                'pet_type': pet_type.data[0],
                'stages': stages.data,
                'skills': skills.data
            }
            
            return JSONResponse(content={'success': True, 'data': result}, status_code=200)
            
        except Exception as e:
            logger.error(f"获取宠物类型详情失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    # ========== 用户宠物相关API ==========
    
    @app.post("/api/users/{user_id}/pets")
    async def adopt_pet(user_id: int, request: Request):
        """用户领养宠物"""
        try:
            data = await request.json()
            pet_type_id = data.get('pet_type_id')
            nickname = data.get('nickname')
            
            if not pet_type_id:
                return JSONResponse(content={'error': '缺少宠物类型ID'}, status_code=400)
            
            # 检查用户是否已有宠物
            existing = db_client.table('user_pets').select('*').eq('user_id', user_id).execute()
            if existing.data:
                return JSONResponse(content={'error': '该用户已有宠物'}, status_code=400)
            
            # 检查宠物类型是否存在
            pet_type = db_client.table('pet_types').select('*').eq('id', pet_type_id).execute()
            if not pet_type.data:
                return JSONResponse(content={'error': '宠物类型不存在'}, status_code=404)
            
            # 创建用户宠物
            pet_data = {
                'user_id': user_id,
                'pet_type_id': pet_type_id,
                'nickname': nickname or pet_type.data[0]['name'],
                'current_stage': 1,
                'total_points': 0,
                'unlocked_stages': {'1': True},
                'unlocked_skills': {}
            }
            
            result = db_client.table('user_pets').insert(pet_data).execute()
            
            logger.info(f"用户 {user_id} 领养宠物成功")
            return JSONResponse(content={'success': True, 'data': result.data[0]}, status_code=201)
            
        except Exception as e:
            logger.error(f"领养宠物失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    @app.get("/api/users/{user_id}/pets")
    async def get_user_pets(user_id: int):
        """获取用户的所有宠物"""
        try:
            # 获取用户宠物
            user_pets = db_client.table('user_pets').select('''
                *,
                pet_types (*)
            ''').eq('user_id', user_id).execute()
            
            return JSONResponse(content={'success': True, 'data': user_pets.data}, status_code=200)
            
        except Exception as e:
            logger.error(f"获取用户宠物失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    @app.get("/api/users/{user_id}/pets/{pet_id}")
    async def get_user_pet_detail(user_id: int, pet_id: int):
        """获取用户宠物详情"""
        try:
            # 获取用户宠物
            user_pet = db_client.table('user_pets').select('''
                *,
                pet_types (*)
            ''').eq('id', pet_id).eq('user_id', user_id).execute()
            
            if not user_pet.data:
                return JSONResponse(content={'error': '宠物不存在'}, status_code=404)
            
            pet_data = user_pet.data[0]
            pet_type_id = pet_data['pet_type_id']
            current_stage = pet_data['current_stage']
            
            # 获取当前阶段的详情
            stage_info = db_client.table('pet_stages').select('*').eq('pet_type_id', pet_type_id).eq('stage_level', current_stage).execute()
            
            # 获取已解锁的技能
            unlocked_skills = pet_data.get('unlocked_skills', {})
            skills_info = []
            if unlocked_skills:
                skill_ids = list(unlocked_skills.keys())
                skills_result = db_client.table('pet_skills').select('*').in_('id', skill_ids).execute()
                skills_info = skills_result.data if skills_result.data else []
            
            result = {
                'pet': pet_data,
                'current_stage_info': stage_info.data[0] if stage_info.data else None,
                'unlocked_skills': skills_info
            }
            
            return JSONResponse(content={'success': True, 'data': result}, status_code=200)
            
        except Exception as e:
            logger.error(f"获取宠物详情失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    # ========== 积分相关API ==========
    
    @app.post("/api/users/{user_id}/points")
    async def add_points(user_id: int, request: Request):
        """给用户添加积分"""
        try:
            data = await request.json()
            points = data.get('points')
            reason = data.get('reason')
            category = data.get('category')
            user_pet_id = data.get('user_pet_id')
            
            if not all([points, reason, category]):
                return JSONResponse(content={'error': '缺少必要参数'}, status_code=400)
            
            # 创建积分记录
            record_data = {
                'user_id': user_id,
                'points': points,
                'reason': reason,
                'category': category,
                'user_pet_id': user_pet_id
            }
            
            result = db_client.table('point_records').insert(record_data).execute()
            
            # 更新用户总积分
            user = db_client.table('users').select('total_points').eq('id', user_id).execute()
            if user.data:
                new_total = user.data[0]['total_points'] + points
                db_client.table('users').update({'total_points': new_total}).eq('id', user_id).execute()
            
            # 更新宠物积分
            if user_pet_id:
                pet = db_client.table('user_pets').select('total_points').eq('id', user_pet_id).execute()
                if pet.data:
                    new_pet_total = pet.data[0]['total_points'] + points
                    db_client.table('user_pets').update({'total_points': new_pet_total}).eq('id', user_pet_id).execute()
                    
                    # 检查是否可以解锁新阶段
                    check_and_unlock_stages(user_pet_id, new_pet_total)
            
            logger.info(f"用户 {user_id} 获得 {points} 积分")
            return JSONResponse(content={'success': True, 'data': result.data[0]}, status_code=201)
            
        except Exception as e:
            logger.error(f"添加积分失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    def check_and_unlock_stages(pet_id: int, total_points: int):
        """检查并解锁宠物新阶段"""
        try:
            # 获取宠物信息
            pet = db_client.table('user_pets').select('*, pet_types (*)').eq('id', pet_id).execute()
            if not pet.data:
                return
            
            pet_data = pet.data[0]
            pet_type_id = pet_data['pet_type_id']
            current_stage = pet_data['current_stage']
            
            # 获取所有阶段
            stages = db_client.table('pet_stages').select('*').eq('pet_type_id', pet_type_id).order('stage_level').execute()
            
            unlocked_stages = pet_data.get('unlocked_stages', {})
            unlocked_skills = pet_data.get('unlocked_skills', {})
            
            # 检查每个阶段是否可以解锁
            for stage in stages.data:
                if total_points >= stage['required_points'] and str(stage['stage_level']) not in unlocked_stages:
                    # 解锁该阶段
                    unlocked_stages[str(stage['stage_level'])] = True
                    
                    # 更新当前阶段
                    if stage['stage_level'] > current_stage:
                        current_stage = stage['stage_level']
                    
                    # 解锁该阶段的技能
                    skills = db_client.table('pet_skills').select('*').eq('pet_type_id', pet_type_id).eq('stage_level', stage['stage_level']).execute()
                    for skill in skills.data:
                        unlocked_skills[str(skill['id'])] = True
                    
                    logger.info(f"宠物 {pet_id} 解锁阶段 {stage['stage_level']}: {stage['stage_name']}")
            
            # 更新数据库
            db_client.table('user_pets').update({
                'current_stage': current_stage,
                'unlocked_stages': unlocked_stages,
                'unlocked_skills': unlocked_skills
            }).eq('id', pet_id).execute()
            
        except Exception as e:
            logger.error(f"解锁阶段失败: {str(e)}")
    
    @app.get("/api/users/{user_id}/points/records")
    async def get_point_records(user_id: int, limit: int = 20, offset: int = 0):
        """获取用户积分记录"""
        try:
            result = db_client.table('point_records').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).offset(offset).execute()
            
            return JSONResponse(content={'success': True, 'data': result.data}, status_code=200)
            
        except Exception as e:
            logger.error(f"获取积分记录失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    # ========== 排行榜相关API ==========
    
    @app.get("/api/leaderboard")
    async def get_leaderboard(limit: int = 10):
        """获取积分排行榜"""
        try:
            result = db_client.table('users').select('id, username, display_name, total_points, avatar_url').order('total_points', desc=True).limit(limit).execute()
            
            return JSONResponse(content={'success': True, 'data': result.data}, status_code=200)
            
        except Exception as e:
            logger.error(f"获取排行榜失败: {str(e)}")
            return JSONResponse(content={'error': str(e)}, status_code=500)
    
    logger.info("山海经班级宠物积分系统路由已注册")
