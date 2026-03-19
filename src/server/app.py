"""
山海经班级宠物积分系统 - 主应用
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from storage.database.supabase_client import get_supabase_client
from utils.logger import setup_logger

# 初始化日志
logger = setup_logger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化Supabase客户端
db_client = get_supabase_client()


# ========== 用户相关API ==========

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        display_name = data.get('display_name')
        
        if not all([username, email, display_name]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 检查用户名是否已存在
        existing = db_client.table('users').select('*').eq('username', username).execute()
        if existing.data:
            return jsonify({'error': '用户名已存在'}), 400
        
        # 创建用户
        user_data = {
            'username': username,
            'email': email,
            'display_name': display_name,
            'total_points': 0
        }
        
        result = db_client.table('users').insert(user_data).execute()
        
        logger.info(f"创建用户成功: {username}")
        return jsonify({'success': True, 'data': result.data[0]}), 201
        
    except Exception as e:
        logger.error(f"创建用户失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户信息"""
    try:
        result = db_client.table('users').select('*').eq('id', user_id).execute()
        
        if not result.data:
            return jsonify({'error': '用户不存在'}), 404
        
        return jsonify({'success': True, 'data': result.data[0]}), 200
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========== 宠物类型相关API ==========

@app.route('/api/pets/types', methods=['GET'])
def get_pet_types():
    """获取所有宠物类型（山海经生物）"""
    try:
        result = db_client.table('pet_types').select('*').execute()
        return jsonify({'success': True, 'data': result.data}), 200
        
    except Exception as e:
        logger.error(f"获取宠物类型失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/pets/types/<int:pet_type_id>', methods=['GET'])
def get_pet_type_detail(pet_type_id):
    """获取宠物类型详情（包含进化阶段）"""
    try:
        # 获取宠物类型
        pet_type = db_client.table('pet_types').select('*').eq('id', pet_type_id).execute()
        if not pet_type.data:
            return jsonify({'error': '宠物类型不存在'}), 404
        
        # 获取该宠物的所有进化阶段
        stages = db_client.table('pet_stages').select('*').eq('pet_type_id', pet_type_id).order('stage_level').execute()
        
        # 获取该宠物的所有技能
        skills = db_client.table('pet_skills').select('*').eq('pet_type_id', pet_type_id).order('stage_level').execute()
        
        result = {
            'pet_type': pet_type.data[0],
            'stages': stages.data,
            'skills': skills.data
        }
        
        return jsonify({'success': True, 'data': result}), 200
        
    except Exception as e:
        logger.error(f"获取宠物类型详情失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========== 用户宠物相关API ==========

@app.route('/api/users/<int:user_id>/pets', methods=['POST'])
def adopt_pet(user_id):
    """用户领养宠物"""
    try:
        data = request.json
        pet_type_id = data.get('pet_type_id')
        nickname = data.get('nickname')
        
        if not pet_type_id:
            return jsonify({'error': '缺少宠物类型ID'}), 400
        
        # 检查用户是否已有宠物
        existing = db_client.table('user_pets').select('*').eq('user_id', user_id).execute()
        if existing.data:
            return jsonify({'error': '该用户已有宠物'}), 400
        
        # 检查宠物类型是否存在
        pet_type = db_client.table('pet_types').select('*').eq('id', pet_type_id).execute()
        if not pet_type.data:
            return jsonify({'error': '宠物类型不存在'}), 404
        
        # 创建用户宠物
        pet_data = {
            'user_id': user_id,
            'pet_type_id': pet_type_id,
            'nickname': nickname or pet_type.data[0]['name'],
            'current_stage': 1,
            'total_points': 0,
            'unlocked_stages': {'1': True},  # 默认解锁第一阶段
            'unlocked_skills': {}
        }
        
        result = db_client.table('user_pets').insert(pet_data).execute()
        
        logger.info(f"用户 {user_id} 领养宠物成功")
        return jsonify({'success': True, 'data': result.data[0]}), 201
        
    except Exception as e:
        logger.error(f"领养宠物失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>/pets', methods=['GET'])
def get_user_pets(user_id):
    """获取用户的所有宠物"""
    try:
        # 获取用户宠物
        user_pets = db_client.table('user_pets').select('''
            *,
            pet_types (*)
        ''').eq('user_id', user_id).execute()
        
        return jsonify({'success': True, 'data': user_pets.data}), 200
        
    except Exception as e:
        logger.error(f"获取用户宠物失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>/pets/<int:pet_id>', methods=['GET'])
def get_user_pet_detail(user_id, pet_id):
    """获取用户宠物详情"""
    try:
        # 获取用户宠物
        user_pet = db_client.table('user_pets').select('''
            *,
            pet_types (*)
        ''').eq('id', pet_id).eq('user_id', user_id).execute()
        
        if not user_pet.data:
            return jsonify({'error': '宠物不存在'}), 404
        
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
            skills_info = db_client.table('pet_skills').select('*').in_('id', skill_ids).execute()
        
        result = {
            'pet': pet_data,
            'current_stage_info': stage_info.data[0] if stage_info.data else None,
            'unlocked_skills': skills_info.data if skills_info else []
        }
        
        return jsonify({'success': True, 'data': result}), 200
        
    except Exception as e:
        logger.error(f"获取宠物详情失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========== 积分相关API ==========

@app.route('/api/users/<int:user_id>/points', methods=['POST'])
def add_points(user_id):
    """给用户添加积分"""
    try:
        data = request.json
        points = data.get('points')
        reason = data.get('reason')
        category = data.get('category')
        user_pet_id = data.get('user_pet_id')
        
        if not all([points, reason, category]):
            return jsonify({'error': '缺少必要参数'}), 400
        
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
        return jsonify({'success': True, 'data': result.data[0]}), 201
        
    except Exception as e:
        logger.error(f"添加积分失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


def check_and_unlock_stages(pet_id, total_points):
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


@app.route('/api/users/<int:user_id>/points/records', methods=['GET'])
def get_point_records(user_id):
    """获取用户积分记录"""
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        result = db_client.table('point_records').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).offset(offset).execute()
        
        return jsonify({'success': True, 'data': result.data}), 200
        
    except Exception as e:
        logger.error(f"获取积分记录失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========== 排行榜相关API ==========

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """获取积分排行榜"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        result = db_client.table('users').select('id, username, display_name, total_points, avatar_url').order('total_points', desc=True).limit(limit).execute()
        
        return jsonify({'success': True, 'data': result.data}), 200
        
    except Exception as e:
        logger.error(f"获取排行榜失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========== 健康检查 ==========

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': '山海经班级宠物积分系统运行正常'}), 200


# ========== 前端页面 ==========

@app.route('/', methods=['GET'])
def index():
    """返回前端页面"""
    try:
        frontend_path = os.path.join(project_root, 'src', 'frontend', 'index.html')
        with open(frontend_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        logger.error(f"读取前端页面失败: {str(e)}")
        return jsonify({'error': '页面不存在'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
