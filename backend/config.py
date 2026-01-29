"""
媒体运营自动化系统 - 配置文件
"""

import os
from pathlib import Path

# 基础路径配置
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 数据库配置
DATABASE_URL = f"sqlite:///{DATA_DIR}/media_automation.db"

# AI API 配置
# OpenAI API (用于生成文案)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# 图像生成 API (用于生成配图)
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY", "")
IMAGE_API_BASE = os.getenv("IMAGE_API_BASE", "https://api.openai.com/v1")

# 平台配置
PLATFORMS = {
    "xiaohongshu": {
        "name": "小红书",
        "enabled": True,
        "appkey": os.getenv("XIAOHONGSHU_APPKEY", ""),
        "secret": os.getenv("XIAOHONGSHU_SECRET", ""),
    },
    "wechat": {
        "name": "公众号",
        "enabled": True,
        "appid": os.getenv("WECHAT_APPID", ""),
        "appsecret": os.getenv("WECHAT_APPSECRET", ""),
    }
}

# 定时任务配置
SCHEDULER_CONFIG = {
    "enabled": True,
    "timezone": "Asia/Shanghai",
    "daily_publish_time": "08:00",  # 每天早上8点自动发布
}

# 内容生成配置
CONTENT_CONFIG = {
    "default_topic_category": "lifestyle",  # 默认话题分类
    "max_daily_posts": 3,  # 每天最大发布数量
    "image_style": "modern, minimalist",  # 默认图片风格
    "content_length": {
        "min_words": 300,
        "max_words": 800
    }
}

# 服务器配置
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": True,
    "reload": True
}

# 文件存储配置
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
