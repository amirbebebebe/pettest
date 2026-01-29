"""
媒体运营自动化系统 - 配置文件
小红书爆款宠物内容专家版
"""

import os
from pathlib import Path
from datetime import datetime
import json

# ==================== 基础配置 ====================

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# 内容目录
CONTENT_DIR = PROJECT_ROOT / "content"
CONTENT_DIR.mkdir(exist_ok=True)

# 日志目录
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ==================== AI API 配置 ====================
# 选择AI提供商：openai 或 volcano
AI_PROVIDER = os.getenv("AI_PROVIDER", "volcano")  # 默认使用火山引擎

# OpenAI API (用于生成文案 - 备选)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

# 火山引擎 API (豆包大模型 - 推荐)
VOLCANO_API_KEY = os.getenv("VOLCANO_API_KEY", "")
VOLCANO_API_SECRET = os.getenv("VOLCANO_API_SECRET", "")
VOLCANO_ENDPOINT_ID = os.getenv("VOLCANO_ENDPOINT_ID", "")  # 部署的模型ID
VOLCANO_MODEL = os.getenv("VOLCANO_MODEL", "doubao-pro-32k")  # 豆包Pro 32K
VOLCANO_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"

# 图像生成 API (支持OpenAI DALL-E和火山Seedream)
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY", "")
IMAGE_API_BASE = os.getenv("IMAGE_API_BASE", "https://api.openai.com/v1")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "dall-e-3")

# 火山引擎图像生成配置
VOLCANO_IMAGE_MODEL = os.getenv("VOLCANO_IMAGE_MODEL", "doubao-seedream-4-5-251128")
VOLCANO_IMAGE_SIZE = os.getenv("VOLCANO_IMAGE_SIZE", "2K")  # 2K, 1024x1024等
VOLCANO_IMAGE_WATERMARK = os.getenv("VOLCANO_IMAGE_WATERMARK", "true")

# ==================== 平台配置 ====================

# 小红书配置
XIAOHONGSHU_COOKIE = os.getenv("XIAOHONGSHU_COOKIE", "")
XIAHONGSHU_XS = os.getenv("XIAHONGSHU_XS", "")

# 公众号配置
WECHAT_APPID = os.getenv("WECHAT_APPID", "")
WECHAT_APPSECRET = os.getenv("WECHAT_APPSECRET", "")
WECHAT_TOKEN = os.getenv("WECHAT_TOKEN", "")

# ==================== 🐱 宠物内容策略配置 ====================

# 宠物类型（混合模式）
PET_TYPES = ["猫咪", "狗狗", "猫咪和狗狗"]

# 宠物话题分类
PET_TOPIC_CATEGORIES = {
    "基础知识": [
        "猫咪不能吃的食物",
        "狗狗不能吃的食物",
        "猫咪的寿命",
        "狗狗的寿命",
        "猫咪多久洗一次澡",
        "狗狗多久洗一次澡",
        "猫咪驱虫频率",
        "狗狗驱虫频率",
        "猫咪打疫苗时间",
        "狗狗打疫苗时间"
    ],
    "行为解读": [
        "猫咪摇尾巴代表什么",
        "狗狗摇尾巴代表什么",
        "猫咪呼噜呼噜的声音",
        "狗狗拆家原因",
        "猫咪蹭你的原因",
        "猫咪炸毛是什么意思",
        "狗狗露肚皮的意思",
        "猫咪弓背的原因",
        "狗狗追尾巴的原因",
        "猫咪瞳孔变化的含义"
    ],
    "趣味挑战": [
        "猫咪最讨厌的味道",
        "狗狗最讨厌的味道",
        "猫咪能看懂电视吗",
        "狗狗能记住多少单词",
        "猫咪的梦境",
        "狗狗的梦境",
        "猫咪为什么怕黄瓜",
        "狗狗为什么爱追松鼠",
        "猫咪的胡须作用",
        "狗狗的舌头功能"
    ],
    "热点结合": [
        "宠物版春节",
        "宠物版情人节",
        "宠物版双十一",
        "宠物版夏天",
        "宠物版冬天",
        "宠物版开学季",
        "宠物版过年",
        "宠物版中秋",
        "宠物版国庆",
        "宠物版母亲节"
    ]
}

# 宠物图片风格配置
PET_IMAGE_STYLES = {
    "main_poster": {
        "style": "大字报风格，简洁有力，醒目的标题字体，现代设计感",
        "colors": ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3"],
        "elements": ["宠物爪子", "宠物表情", "可爱图标"]
    },
    "question_card": {
        "style": "大字报+卡通搞笑风格，可爱的卡通背景，有趣的贴纸元素",
        "colors": ["#FFE4E1", "#E6E6FA", "#FFF0F5", "#E0FFFF"],
        "elements": ["卡通宠物", "问号气泡", "选择按钮A/B", "趣味装饰"]
    }
}

# ==================== 内容生成配置 ====================

# 发布计划
PUBLISH_SCHEDULE = {
    "morning": {
        "time": "08:00",  # 北京时间早上8点
        "type": "知识测试",
        "hot_topic_weight": 0.3  # 热点权重30%
    },
    "evening": {
        "time": "20:00",  # 北京时间晚上8点
        "type": "趣味挑战",
        "hot_topic_weight": 0.5  # 热点权重50%（晚间蹭热点更重要）
    }
}

# 内容配置
CONTENT_CONFIG = {
    "posts_per_day": 2,
    "images_per_post": 4,
    "questions_per_post": 3,
    "min_words": 150,
    "max_words": 300,
    "image_size": "1024x1024",
    "image_quality": "standard",
    "question_types": ["基础知识", "行为解读", "趣味挑战"],
    "hot_topic_days": 7,  # 热点追踪最近7天
    "random_pet_type": True  # 随机选择猫咪或狗狗
}

# 🐱 宠物内容专用提示词模板 - 主图
MAIN_POSTER_PROMPT = """
Create a large text poster for Xiaohongshu (Chinese social media) about a pet ownership test quiz.

Design requirements:
- Style: Large text poster, bold and eye-catching, modern design
- Main text: "测测你是不是合格铲屎官？送宠物试用装了！" (Test if you're a qualified pet owner! Get free pet samples!)
- Text style: Bold, cute Chinese font
- Background: Warm and inviting pet-themed background
- Color scheme: Fresh and energetic (coral red, mint green, sunny yellow)
- Add cute pet elements (paws, hearts, stars)
- Overall vibe: Fun, interactive, inviting participation

Please output just the image prompt in English.
"""

# 🐱 宠物内容专用提示词模板 - 问题卡片
QUESTION_CARD_PROMPT = """
Create a fun cartoon-style question card for a pet ownership quiz on Xiaohongshu.

Context: {question}
Type: {question_type}
Options: A) {option_a}  B) {option_b}

Design requirements:
- Style: Large text poster + cute cartoon style, funny and entertaining
- Text: Big and bold question text with A/B options clearly shown
- Background: Cute cartoon pet background with fun elements
- Color scheme: Light and playful (light pink, light blue, mint green)
- Add comic elements: speech bubbles, question marks, playful stickers
- Overall vibe: Engaging, shareable, encourages comments

Please output just the image prompt in English.
"""

# 🐱 正文生成提示词模板
BODY_CONTENT_PROMPT = """
你是一位小红书爆款宠物内容专家。请为一篇宠物测试类笔记创作正文。

内容信息：
- 宠物类型：{pet_type}
- 问题数量：{question_count}个
- 测试类型：{test_type}

正文要求：
1. 开头：吸引眼球的引入（可以用emoji）
2. 互动引导：邀请粉丝参与测试
3. 结果分级：答对3个=优秀铲屎官，答对2个=合格铲屎官，答对1个=差劲铲屎官
4. 行动号召：请在评论区留下你的答案
5. 时效性：次日会揭晓答案
6. 福利诱饵：随机抽取1-3名优秀铲屎官送出宠物试用装
7. 号召：欢迎大家积极参与
8. 字数：{min_words}-{max_words}字
9. 风格：小红书风格，轻松活泼，适当使用emoji
10. 语言：简体中文，使用中文标点

请输出JSON格式：
{{
    "intro": "开头引入段落（2-3句话）",
    "body": "正文主体，包含互动引导和分级说明",
    "cta": "行动号召和福利说明",
    "hashtags": ["标签1", "标签2", "标签3", "标签4", "标签5"]
}}
"""

# ==================== 热点追踪配置 ====================

HOT_TOPIC_CONFIG = {
    "enabled": True,
    "search_platforms": ["weibo", "douyin", "xiaohongshu"],
    "refresh_interval": 3600,  # 每小时刷新
    "relevance_check": True,
    "pet_related_weight": 2.0,  # 宠物相关话题权重
    "general_hot_weight": 1.0   # 一般热点权重
}

# ==================== 发布配置 ====================

PUBLISH_CONFIG = {
    "xiaohongshu": {
        "enabled": True,
        "title_max_length": 20,
        "content_min_length": 100,
        "image_min_count": 1,
        "image_max_count": 9,
        "posting_times": ["08:00", "20:00"]
    },
    "wechat": {
        "enabled": False,  # 暂时专注小红书
        "title_max_length": 64,
        "content_min_length": 300,
        "image_min_count": 1,
        "image_max_count": 8
    }
}

# ==================== 日志配置 ====================

LOG_CONFIG = {
    "level": "INFO",
    "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    "rotation": "1 day",
    "retention": "30 days",
    "encoding": "utf-8"
}

# ==================== 工具函数 ====================

def get_today_date() -> str:
    """获取今天日期（YYYY-MM-DD格式）"""
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time() -> str:
    """获取当前时间（HH:MM:SS格式）"""
    return datetime.now().strftime("%H:%M:%S")

def load_json_file(filepath: Path) -> dict:
    """加载JSON文件"""
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json_file(filepath: Path, data: dict) -> None:
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_content_path(platform: str, date: str = None) -> Path:
    """获取内容存储路径"""
    if date is None:
        date = get_today_date()
    return CONTENT_DIR / platform / date

def get_post_time(post_type: str) -> str:
    """获取发布时间"""
    if post_type == "morning":
        return PUBLISH_SCHEDULE["morning"]["time"]
    elif post_type == "evening":
        return PUBLISH_SCHEDULE["evening"]["time"]
    else:
        return "12:00"  # 默认中午

# ==================== 数据库配置 ====================

DATABASE_URL = f"sqlite:///{DATA_DIR}/media_automation.db"
