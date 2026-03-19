"""
山海经宠物图片生成工具
用于生成不同阶段的山海经生物形态图片
"""
import asyncio
import os
from coze_coding_dev_sdk import ImageGenerationClient
from coze_coding_utils.runtime_ctx.context import new_context
import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)


# 山海经宠物配置
PET_TYPES = [
    {
        "name": "麒麟",
        "description": "麒麟，中国传统瑞兽，性情温和，传说能活两千年。古人认为，麒麟出没处，必有祥瑞。",
        "element": "土",
        "rarity": "传说",
        "stages": [
            {
                "level": 1,
                "name": "麒麟幼崽",
                "required_points": 0,
                "description": "刚刚诞生的麒麟幼崽，身形娇小，眼神清澈，虽无神力却已显灵性。"
            },
            {
                "level": 2,
                "name": "灵麟",
                "required_points": 100,
                "description": "经过修炼的麒麟，开始展现神异之能，身上隐隐有光芒流转。"
            },
            {
                "level": 3,
                "name": "祥瑞麒麟",
                "required_points": 300,
                "description": "瑞气环绕的麒麟，脚踏祥云，具有护佑一方的神力。"
            },
            {
                "level": 4,
                "name": "圣麟神兽",
                "required_points": 600,
                "description": "麒麟之尊，拥有开天辟地的威能，所到之处万物复苏。"
            }
        ]
    },
    {
        "name": "凤凰",
        "description": "凤凰，百鸟之王，传说中不死鸟，浴火重生，象征永生与重生。",
        "element": "火",
        "rarity": "传说",
        "stages": [
            {
                "level": 1,
                "name": "凤凰雏鸟",
                "required_points": 0,
                "description": "火中诞生的凤凰雏鸟，羽毛带着微弱的火光，充满生机。"
            },
            {
                "level": 2,
                "name": "火凤",
                "required_points": 100,
                "description": "浴火成长的凤凰，羽翼渐丰，开始掌握火焰之力。"
            },
            {
                "level": 3,
                "name": "涅槃凤凰",
                "required_points": 300,
                "description": "经历过涅槃的凤凰，更加华美，掌握重生之秘。"
            },
            {
                "level": 4,
                "name": "神凤天鸟",
                "required_points": 600,
                "description": "凤凰至尊，展翅间可焚天煮海，不死不灭。"
            }
        ]
    },
    {
        "name": "九尾狐",
        "description": "九尾狐，山海经中的灵兽，拥有九条尾巴，智慧超群，善于幻术。",
        "element": "木",
        "rarity": "史诗",
        "stages": [
            {
                "level": 1,
                "name": "狐妖幼崽",
                "required_points": 0,
                "description": "刚出生的小狐狸，只有一条尾巴，灵动可爱，充满好奇。"
            },
            {
                "level": 2,
                "name": "三尾灵狐",
                "required_points": 80,
                "description": "修炼有成，生出三条尾巴，开始掌握幻术之力。"
            },
            {
                "level": 3,
                "name": "六尾妖狐",
                "required_points": 240,
                "description": "功力大增，六尾摇曳，幻术造诣精深。"
            },
            {
                "level": 4,
                "name": "九尾天狐",
                "required_points": 500,
                "description": "九尾全出，通天彻地之能，举手投足间可颠倒众生。"
            }
        ]
    },
    {
        "name": "白泽",
        "description": "白泽，能说人话，通万物之情，晓天下万物状貌，是知万物之精怪的神兽。",
        "element": "金",
        "rarity": "史诗",
        "stages": [
            {
                "level": 1,
                "name": "白泽幼兽",
                "required_points": 0,
                "description": "幼年白泽，通体雪白，眼神智慧，能感知周围灵气。"
            },
            {
                "level": 2,
                "name": "灵智白泽",
                "required_points": 80,
                "description": "智慧大开，能识百种精怪，为人类驱邪避凶。"
            },
            {
                "level": 3,
                "name": "通灵白泽",
                "required_points": 240,
                "description": "通晓万物，能预知祸福，是智慧与祥瑞的化身。"
            },
            {
                "level": 4,
                "name": "圣兽白泽",
                "required_points": 500,
                "description": "知晓天下所有精怪，智慧如海，能化解一切灾厄。"
            }
        ]
    },
    {
        "name": "应龙",
        "description": "应龙，古代中国神话传说中的生双翅的龙，是天神之一，具有强大的战斗力。",
        "element": "水",
        "rarity": "史诗",
        "stages": [
            {
                "level": 1,
                "name": "应龙幼龙",
                "required_points": 0,
                "description": "刚破壳的应龙，翅膀柔软，只能在水面滑翔。"
            },
            {
                "level": 2,
                "name": "飞龙",
                "required_points": 80,
                "description": "翅膀渐硬，能翱翔天际，开始掌握水系法术。"
            },
            {
                "level": 3,
                "name": "腾龙",
                "required_points": 240,
                "description": "威武雄壮，呼风唤雨，具有龙族的强大力量。"
            },
            {
                "level": 4,
                "name": "天龙应龙",
                "required_points": 500,
                "description": "应龙至尊，翻江倒海，是水族之主，天界战神。"
            }
        ]
    },
    {
        "name": "毕方",
        "description": "毕方，古代传说中的火灾之兆，外形像丹顶鹤，只有一条腿，身体为蓝色、有红色的斑点。",
        "element": "火",
        "rarity": "稀有",
        "stages": [
            {
                "level": 1,
                "name": "毕方雏鸟",
                "required_points": 0,
                "description": "单脚站立的蓝色小鸟，羽翼上有红色斑点。"
            },
            {
                "level": 2,
                "name": "炎鸟",
                "required_points": 60,
                "description": "羽翼渐丰，能够制造小火苗，是火灾的预兆。"
            },
            {
                "level": 3,
                "name": "火羽毕方",
                "required_points": 180,
                "description": "浑身燃烧着蓝色火焰，所到之处可引发大火。"
            },
            {
                "level": 4,
                "name": "神火毕方",
                "required_points": 400,
                "description": "火之化身，展翅间烈焰滔天，无人能挡。"
            }
        ]
    },
    {
        "name": "貔貅",
        "description": "貔貅，中国古代神话传说之神兽，有嘴无肛，能吞万物而不泄，可招财聚宝。",
        "element": "土",
        "rarity": "稀有",
        "stages": [
            {
                "level": 1,
                "name": "貔貅幼兽",
                "required_points": 0,
                "description": "小貔貅，外形似狮，眼神机灵，喜欢收集闪亮的东西。"
            },
            {
                "level": 2,
                "name": "招财貔貅",
                "required_points": 60,
                "description": "能够招财进宝，身上的财运越来越浓。"
            },
            {
                "level": 3,
                "name": "聚宝灵兽",
                "required_points": 180,
                "description": "财气逼人，能为主人带来无尽的财富。"
            },
            {
                "level": 4,
                "name": "财神貔貅",
                "required_points": 400,
                "description": "貔貅之尊，掌管天下财气，是财富的象征。"
            }
        ]
    },
    {
        "name": "饕餮",
        "description": "饕餮，传说中的凶兽，贪食，能吞噬天地万物，是贪婪的象征。",
        "element": "金",
        "rarity": "稀有",
        "stages": [
            {
                "level": 1,
                "name": "饕餮幼兽",
                "required_points": 0,
                "description": "小饕餮，外形似狼，胃口很小，但很贪吃。"
            },
            {
                "level": 2,
                "name": "贪食兽",
                "required_points": 60,
                "description": "食量大增，能吞下比自身体型大的猎物。"
            },
            {
                "level": 3,
                "name": "暴食凶兽",
                "required_points": 180,
                "description": "凶残无比，能吞噬一切，无所不食。"
            },
            {
                "level": 4,
                "name": "吞天饕餮",
                "required_points": 400,
                "description": "饕餮之王，一张巨口可吞天地，是恐惧的化身。"
            }
        ]
    },
    {
        "name": "鲲鹏",
        "description": "鲲鹏，庄子《逍遥游》中的神兽，鲲之大不知其几千里也，化而为鸟，其名为鹏。",
        "element": "水",
        "rarity": "传说",
        "stages": [
            {
                "level": 1,
                "name": "鱼苗",
                "required_points": 0,
                "description": "深海中的小鱼苗，体型虽小却蕴含巨能。"
            },
            {
                "level": 2,
                "name": "巨鲲",
                "required_points": 100,
                "description": "体型庞大的鲲，在深海中游弋，气势磅礴。"
            },
            {
                "level": 3,
                "name": "化鹏",
                "required_points": 300,
                "description": "正在转化的鲲鹏，鱼鳍化为羽翼，即将翱翔天际。"
            },
            {
                "level": 4,
                "name": "鲲鹏神兽",
                "required_points": 600,
                "description": "真正的鲲鹏，扶摇直上九万里，天地任逍遥。"
            }
        ]
    },
    {
        "name": "英招",
        "description": "英招，人面马身，身上有虎纹，生鸟翼，声音如榴，是看管天帝花园的神兽。",
        "element": "木",
        "rarity": "稀有",
        "stages": [
            {
                "level": 1,
                "name": "英招幼兽",
                "required_points": 0,
                "description": "小马驹般的生物，人面兽身，翅膀还未长出。"
            },
            {
                "level": 2,
                "name": "翼马",
                "required_points": 60,
                "description": "背上生出翅膀，能在空中飞行，速度极快。"
            },
            {
                "level": 3,
                "name": "守护兽",
                "required_points": 180,
                "description": "看守神园的守护者，威武非凡，忠于职守。"
            },
            {
                "level": 4,
                "name": "天园神兽",
                "required_points": 400,
                "description": "天帝花园的守护神，神威赫赫，百兽敬畏。"
            }
        ]
    }
]

# 技能配置
SKILL_TEMPLATES = {
    "特效": [
        "祥瑞光环", "神光护体", "灵气缭绕", "天降异象",
        "火焰之翼", "冰霜铠甲", "雷电缠绕", "风之轨迹"
    ],
    "被动": [
        "福运加身", "智慧启迪", "力量增幅", "速度提升",
        "防御强化", "生命汲取", "暴击几率", "闪避增强"
    ],
    "主动": [
        "神兽咆哮", "元素冲击", "幻影分身", "时空穿梭",
        "治愈之光", "毁灭之雨", "守护结界", "狂暴之力"
    ]
}


async def generate_pet_image(client: ImageGenerationClient, pet_name: str, stage_name: str, description: str) -> str:
    """
    生成宠物图片
    
    Args:
        client: 图片生成客户端
        pet_name: 宠物名称
        stage_name: 阶段名称
        description: 阶段描述
        
    Returns:
        图片URL
    """
    # 构造生成提示词
    prompt = f"""
    中国神话山海经风格的{pet_name}，{stage_name}形态。
    外观描述：{description}
    艺术风格：中国古典神话插画风格，色彩浓郁，充满神秘感。
    背景：中国山水画风格，云雾缭绕，仙气飘飘。
    整体氛围：神圣、威严、充满灵性。
    """
    
    try:
        logger.info(f"正在生成图片: {pet_name} - {stage_name}")
        response = await client.generate_async(prompt=prompt.strip(), size="2K")
        
        if response.success and response.image_urls:
            logger.info(f"图片生成成功: {pet_name} - {stage_name}")
            return response.image_urls[0]
        else:
            logger.error(f"图片生成失败: {pet_name} - {stage_name}, 错误: {response.error_messages}")
            return None
    except Exception as e:
        logger.error(f"图片生成异常: {pet_name} - {stage_name}, 错误: {str(e)}")
        return None


async def generate_all_pet_images():
    """生成所有宠物的所有阶段图片"""
    ctx = new_context(method="generate_pet_images")
    client = ImageGenerationClient(ctx=ctx)
    
    pet_images = {}
    
    for pet_type in PET_TYPES:
        pet_name = pet_type["name"]
        pet_images[pet_name] = {}
        
        for stage in pet_type["stages"]:
            stage_name = stage["name"]
            description = stage["description"]
            
            image_url = await generate_pet_image(client, pet_name, stage_name, description)
            if image_url:
                pet_images[pet_name][stage["level"]] = image_url
            
            # 避免请求过快
            await asyncio.sleep(2)
    
    return pet_images


def save_pet_images_info(pet_images: dict, output_file: str = "assets/pet_images.json"):
    """保存宠物图片信息到JSON文件"""
    import json
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pet_images, f, ensure_ascii=False, indent=2)
    
    logger.info(f"宠物图片信息已保存到: {output_file}")


async def main():
    """主函数"""
    logger.info("开始生成山海经宠物图片...")
    
    # 生成所有宠物图片
    pet_images = await generate_all_pet_images()
    
    # 保存图片信息
    save_pet_images_info(pet_images)
    
    logger.info("宠物图片生成完成！")


if __name__ == "__main__":
    asyncio.run(main())
