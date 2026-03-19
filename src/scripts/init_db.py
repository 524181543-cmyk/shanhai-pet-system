"""
数据库初始化脚本
用于插入山海经宠物类型、阶段和技能数据
"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))

from storage.database.supabase_client import get_supabase_client
from utils.logger import setup_logger

logger = setup_logger(__name__)


# 山海经宠物配置
PET_TYPES = [
    {
        "name": "麒麟",
        "description": "麒麟，中国传统瑞兽，性情温和，传说能活两千年。古人认为，麒麟出没处，必有祥瑞。",
        "element": "土",
        "rarity": "传说",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "麒麟幼崽", "required_points": 0, "description": "刚刚诞生的麒麟幼崽，身形娇小，眼神清澈，虽无神力却已显灵性。"},
            {"level": 2, "name": "灵麟", "required_points": 100, "description": "经过修炼的麒麟，开始展现神异之能，身上隐隐有光芒流转。"},
            {"level": 3, "name": "祥瑞麒麟", "required_points": 300, "description": "瑞气环绕的麒麟，脚踏祥云，具有护佑一方的神力。"},
            {"level": 4, "name": "圣麟神兽", "required_points": 600, "description": "麒麟之尊，拥有开天辟地的威能，所到之处万物复苏。"}
        ]
    },
    {
        "name": "凤凰",
        "description": "凤凰，百鸟之王，传说中不死鸟，浴火重生，象征永生与重生。",
        "element": "火",
        "rarity": "传说",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "凤凰雏鸟", "required_points": 0, "description": "火中诞生的凤凰雏鸟，羽毛带着微弱的火光，充满生机。"},
            {"level": 2, "name": "火凤", "required_points": 100, "description": "浴火成长的凤凰，羽翼渐丰，开始掌握火焰之力。"},
            {"level": 3, "name": "涅槃凤凰", "required_points": 300, "description": "经历过涅槃的凤凰，更加华美，掌握重生之秘。"},
            {"level": 4, "name": "神凤天鸟", "required_points": 600, "description": "凤凰至尊，展翅间可焚天煮海，不死不灭。"}
        ]
    },
    {
        "name": "九尾狐",
        "description": "九尾狐，山海经中的灵兽，拥有九条尾巴，智慧超群，善于幻术。",
        "element": "木",
        "rarity": "史诗",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "狐妖幼崽", "required_points": 0, "description": "刚出生的小狐狸，只有一条尾巴，灵动可爱，充满好奇。"},
            {"level": 2, "name": "三尾灵狐", "required_points": 80, "description": "修炼有成，生出三条尾巴，开始掌握幻术之力。"},
            {"level": 3, "name": "六尾妖狐", "required_points": 240, "description": "功力大增，六尾摇曳，幻术造诣精深。"},
            {"level": 4, "name": "九尾天狐", "required_points": 500, "description": "九尾全出，通天彻地之能，举手投足间可颠倒众生。"}
        ]
    },
    {
        "name": "白泽",
        "description": "白泽，能说人话，通万物之情，晓天下万物状貌，是知万物之精怪的神兽。",
        "element": "金",
        "rarity": "史诗",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "白泽幼兽", "required_points": 0, "description": "幼年白泽，通体雪白，眼神智慧，能感知周围灵气。"},
            {"level": 2, "name": "灵智白泽", "required_points": 80, "description": "智慧大开，能识百种精怪，为人类驱邪避凶。"},
            {"level": 3, "name": "通灵白泽", "required_points": 240, "description": "通晓万物，能预知祸福，是智慧与祥瑞的化身。"},
            {"level": 4, "name": "圣兽白泽", "required_points": 500, "description": "知晓天下所有精怪，智慧如海，能化解一切灾厄。"}
        ]
    },
    {
        "name": "应龙",
        "description": "应龙，古代中国神话传说中的生双翅的龙，是天神之一，具有强大的战斗力。",
        "element": "水",
        "rarity": "史诗",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "应龙幼龙", "required_points": 0, "description": "刚破壳的应龙，翅膀柔软，只能在水面滑翔。"},
            {"level": 2, "name": "飞龙", "required_points": 80, "description": "翅膀渐硬，能翱翔天际，开始掌握水系法术。"},
            {"level": 3, "name": "腾龙", "required_points": 240, "description": "威武雄壮，呼风唤雨，具有龙族的强大力量。"},
            {"level": 4, "name": "天龙应龙", "required_points": 500, "description": "应龙至尊，翻江倒海，是水族之主，天界战神。"}
        ]
    },
    {
        "name": "毕方",
        "description": "毕方，古代传说中的火灾之兆，外形像丹顶鹤，只有一条腿，身体为蓝色、有红色的斑点。",
        "element": "火",
        "rarity": "稀有",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "毕方雏鸟", "required_points": 0, "description": "单脚站立的蓝色小鸟，羽翼上有红色斑点。"},
            {"level": 2, "name": "炎鸟", "required_points": 60, "description": "羽翼渐丰，能够制造小火苗，是火灾的预兆。"},
            {"level": 3, "name": "火羽毕方", "required_points": 180, "description": "浑身燃烧着蓝色火焰，所到之处可引发大火。"},
            {"level": 4, "name": "神火毕方", "required_points": 400, "description": "火之化身，展翅间烈焰滔天，无人能挡。"}
        ]
    },
    {
        "name": "貔貅",
        "description": "貔貅，中国古代神话传说之神兽，有嘴无肛，能吞万物而不泄，可招财聚宝。",
        "element": "土",
        "rarity": "稀有",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "貔貅幼兽", "required_points": 0, "description": "小貔貅，外形似狮，眼神机灵，喜欢收集闪亮的东西。"},
            {"level": 2, "name": "招财貔貅", "required_points": 60, "description": "能够招财进宝，身上的财运越来越浓。"},
            {"level": 3, "name": "聚宝灵兽", "required_points": 180, "description": "财气逼人，能为主人带来无尽的财富。"},
            {"level": 4, "name": "财神貔貅", "required_points": 400, "description": "貔貅之尊，掌管天下财气，是财富的象征。"}
        ]
    },
    {
        "name": "饕餮",
        "description": "饕餮，传说中的凶兽，贪食，能吞噬天地万物，是贪婪的象征。",
        "element": "金",
        "rarity": "稀有",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "饕餮幼兽", "required_points": 0, "description": "小饕餮，外形似狼，胃口很小，但很贪吃。"},
            {"level": 2, "name": "贪食兽", "required_points": 60, "description": "食量大增，能吞下比自身体型大的猎物。"},
            {"level": 3, "name": "暴食凶兽", "required_points": 180, "description": "凶残无比，能吞噬一切，无所不食。"},
            {"level": 4, "name": "吞天饕餮", "required_points": 400, "description": "饕餮之王，一张巨口可吞天地，是恐惧的化身。"}
        ]
    },
    {
        "name": "鲲鹏",
        "description": "鲲鹏，庄子《逍遥游》中的神兽，鲲之大不知其几千里也，化而为鸟，其名为鹏。",
        "element": "水",
        "rarity": "传说",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "鱼苗", "required_points": 0, "description": "深海中的小鱼苗，体型虽小却蕴含巨能。"},
            {"level": 2, "name": "巨鲲", "required_points": 100, "description": "体型庞大的鲲，在深海中游弋，气势磅礴。"},
            {"level": 3, "name": "化鹏", "required_points": 300, "description": "正在转化的鲲鹏，鱼鳍化为羽翼，即将翱翔天际。"},
            {"level": 4, "name": "鲲鹏神兽", "required_points": 600, "description": "真正的鲲鹏，扶摇直上九万里，天地任逍遥。"}
        ]
    },
    {
        "name": "英招",
        "description": "英招，人面马身，身上有虎纹，生鸟翼，声音如榴，是看管天帝花园的神兽。",
        "element": "木",
        "rarity": "稀有",
        "base_image_url": "",
        "stages": [
            {"level": 1, "name": "英招幼兽", "required_points": 0, "description": "小马驹般的生物，人面兽身，翅膀还未长出。"},
            {"level": 2, "name": "翼马", "required_points": 60, "description": "背上生出翅膀，能在空中飞行，速度极快。"},
            {"level": 3, "name": "守护兽", "required_points": 180, "description": "看守神园的守护者，威武非凡，忠于职守。"},
            {"level": 4, "name": "天园神兽", "required_points": 400, "description": "天帝花园的守护神，神威赫赫，百兽敬畏。"}
        ]
    }
]

# 技能模板
SKILL_TEMPLATES = [
    {"type": "特效", "names": ["祥瑞光环", "神光护体", "灵气缭绕", "天降异象"]},
    {"type": "被动", "names": ["福运加身", "智慧启迪", "力量增幅", "速度提升"]},
    {"type": "主动", "names": ["神兽咆哮", "元素冲击", "幻影分身", "时空穿梭"]}
]


def init_database():
    """初始化数据库"""
    db_client = get_supabase_client()
    
    logger.info("开始初始化数据库...")
    
    # 插入宠物类型
    for pet_type in PET_TYPES:
        try:
            # 检查是否已存在
            existing = db_client.table('pet_types').select('*').eq('name', pet_type['name']).execute()
            if existing.data:
                logger.info(f"宠物类型 {pet_type['name']} 已存在，跳过")
                continue
            
            # 插入宠物类型
            pet_type_data = {
                'name': pet_type['name'],
                'description': pet_type['description'],
                'element': pet_type['element'],
                'rarity': pet_type['rarity'],
                'base_image_url': pet_type.get('base_image_url', '')
            }
            
            result = db_client.table('pet_types').insert(pet_type_data).execute()
            pet_type_id = result.data[0]['id']
            logger.info(f"插入宠物类型: {pet_type['name']} (ID: {pet_type_id})")
            
            # 插入宠物阶段
            for stage in pet_type['stages']:
                stage_data = {
                    'pet_type_id': pet_type_id,
                    'stage_level': stage['level'],
                    'stage_name': stage['name'],
                    'required_points': stage['required_points'],
                    'image_url': f"https://via.placeholder.com/300x300?text={pet_type['name']}+Lv{stage['level']}",
                    'description': stage['description']
                }
                
                db_client.table('pet_stages').insert(stage_data).execute()
                logger.info(f"  插入阶段: {stage['name']}")
            
            # 插入技能
            for skill_template in SKILL_TEMPLATES:
                for skill_name in skill_template['names']:
                    import random
                    skill_data = {
                        'pet_type_id': pet_type_id,
                        'stage_level': random.randint(2, 4),
                        'skill_name': skill_name,
                        'skill_type': skill_template['type'],
                        'effect_description': f"{skill_name}效果描述",
                        'effect_config': {}
                    }
                    
                    db_client.table('pet_skills').insert(skill_data).execute()
            
            logger.info(f"  插入技能完成")
            
        except Exception as e:
            logger.error(f"插入宠物类型 {pet_type['name']} 失败: {str(e)}")
    
    logger.info("数据库初始化完成！")


if __name__ == "__main__":
    init_database()
