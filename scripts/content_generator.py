#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐱 小红书宠物内容生成器
自动生成爆款宠物测试类图文内容
"""

import sys
import json
import random
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    OPENAI_API_KEY, OPENAI_MODEL, OPENAI_API_BASE,
    IMAGE_API_KEY, IMAGE_API_BASE, IMAGE_MODEL,
    CONTENT_CONFIG, PET_TOPIC_CATEGORIES, PET_IMAGE_STYLES,
    MAIN_POSTER_PROMPT, QUESTION_CARD_PROMPT, BODY_CONTENT_PROMPT,
    get_today_date, save_json_file, get_content_path
)
from hot_topics import HotTopicTracker


class PetContentGenerator:
    """小红书宠物内容生成器"""

    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.api_base = OPENAI_API_BASE
        self.image_api_key = IMAGE_API_KEY
        self.image_api_base = IMAGE_API_BASE
        self.image_model = IMAGE_MODEL
        self.hot_tracker = HotTopicTracker()

    def _call_openai_api(self, prompt: str) -> Optional[str]:
        """调用OpenAI API生成内容"""
        if not self.api_key:
            print("❌ 错误: 未配置OPENAI_API_KEY")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位小红书爆款内容专家，擅长创作高互动、高评论的宠物测试类内容。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.8,
            "max_tokens": 2000
        }

        try:
            print(f"📡 调用OpenAI API ({self.model})...")
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print("✅ API调用成功")
            return content

        except requests.exceptions.RequestException as e:
            print(f"❌ API调用失败: {e}")
            return None

    def _call_image_api(self, prompt: str, output_path: Path) -> bool:
        """调用图像生成API生成配图"""
        if not self.image_api_key:
            print("⚠️ 未配置图像生成API，跳过图片生成")
            return False

        headers = {
            "Authorization": f"Bearer {self.image_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.image_model,
            "prompt": prompt,
            "n": 1,
            "size": CONTENT_CONFIG["image_size"],
            "quality": CONTENT_CONFIG["image_quality"]
        }

        try:
            print(f"🎨 调用图像生成API ({self.image_model})...")
            response = requests.post(
                f"{self.image_api_base}/images/generations",
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()

            result = response.json()
            image_url = result["data"][0]["url"]

            # 下载图片
            print("📥 下载生成的图片...")
            image_response = requests.get(image_url, timeout=60)
            image_response.raise_for_status()

            with open(output_path, 'wb') as f:
                f.write(image_response.content)

            print(f"✅ 图片已保存到: {output_path}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ 图片生成失败: {e}")
            return False

    def generate_questions(self, pet_type: str = "猫咪") -> List[Dict]:
        """生成3个宠物问题"""
        # 从热点追踪器获取问题
        topic_data = self.hot_tracker.get_today_topics("morning")
        questions = topic_data.get("questions", [])

        # 如果问题不足，从预设库补充
        if len(questions) < 3:
            # 各类别问题库
            basic_knowledge = [
                {
                    "question": f"以下哪种食物{pet_type}绝对不能吃？",
                    "options": {"A": "鸡肉", "B": "巧克力"},
                    "correct": "B"
                },
                {
                    "question": f"{pet_type}多久需要驱虫一次？",
                    "options": {"A": "1个月", "B": "3个月"},
                    "correct": "B"
                }
            ]

            behavior_interpretation = [
                {
                    "question": f"如果{pet_type}对你露出肚皮，说明什么？",
                    "options": {"A": "想让你摸", "B": "完全信任你"},
                    "correct": "B"
                },
                {
                    "question": f"{pet_type}快速摇尾巴代表什么？",
                    "options": {"A": "开心", "B": "烦躁"},
                    "correct": "B"
                }
            ]

            fun_challenges = [
                {
                    "question": f"你觉得{pet_type}能听懂你说话吗？",
                    "options": {"A": "能听懂", "B": "完全听不懂"},
                    "correct": "A"
                },
                {
                    "question": f"如果{pet_type}会说话，第一句会说什么？",
                    "options": {"A": "铲屎的", "B": "喵/汪"},
                    "correct": "A"
                }
            ]

            all_questions = basic_knowledge + behavior_interpretation + fun_challenges
            random.shuffle(all_questions)

            for q in all_questions:
                if len(questions) >= 3:
                    break
                questions.append({
                    "type": "随机问题",
                    "question": q["question"],
                    "options": q["options"],
                    "correct_answer": q["correct"],
                    "explanation": f"正确答案是{q['correct']}，你答对了吗？"
                })

        return questions[:3]

    def generate_body_content(self, pet_type: str, questions: List[Dict]) -> Dict:
        """生成正文内容"""
        prompt = BODY_CONTENT_PROMPT.format(
            pet_type=pet_type,
            question_count=len(questions),
            test_type="宠物知识测试",
            min_words=CONTENT_CONFIG["min_words"],
            max_words=CONTENT_CONFIG["max_words"]
        )

        response = self._call_openai_api(prompt)

        if not response:
            # 使用默认模板
            return self._default_body_content(pet_type, questions)

        try:
            # 尝试解析JSON
            content_data = json.loads(response)
            return content_data
        except json.JSONDecodeError:
            # 尝试提取JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                content_data = json.loads(response[start:end])
                return content_data

            return self._default_body_content(pet_type, questions)

    def _default_body_content(self, pet_type: str, questions: List[Dict]) -> Dict:
        """默认正文内容"""
        intro = f"🐱 各位铲屎官们看过来！今天给大家准备了一份{pet_type}知识测试卷，看看你是合格还是差劲的铲屎官？"

        # 构建问题列表
        question_list = ""
        for i, q in enumerate(questions, 1):
            question_list += f"\n❓ 第{i}题：{q['question']}\n   A. {q['options']['A']}  B. {q['options']['B']}\n"

        body = f"""📋 测试规则：
{question_list}
📝 评分标准：
✅ 答对3个 = 优秀铲屎官 🌟
✅ 答对2个 = 合格铲屎官 💪
✅ 答对1个 = 差劲铲屎官 😅

💬 请在评论区留下你的答案，明天揭晓正确答案！"""

        cta = """🎁 福利时间！
随机抽取1-3名优秀铲屎官送出宠物试用装！
赶紧在评论区晒出你的答案吧～

👉 关注我，每天分享更多宠物知识！
欢迎大家积极参与，一起做更好的铲屎官！"""

        return {
            "intro": intro,
            "body": body,
            "cta": cta,
            "hashtags": [
                f"{pet_type}",
                "铲屎官",
                "宠物测试",
                "养宠知识",
                "宠物试用装"
            ]
        }

    def generate_image_prompts(self, questions: List[Dict]) -> Dict:
        """生成图片提示词"""
        prompts = {
            "main_poster": MAIN_POSTER_PROMPT,
            "question_cards": []
        }

        # 为每个问题生成图片提示词
        for i, q in enumerate(questions, 1):
            card_prompt = QUESTION_CARD_PROMPT.format(
                question=q['question'],
                question_type=q['type'],
                option_a=q['options']['A'],
                option_b=q['options']['B']
            )

            prompts["question_cards"].append({
                "question_num": i,
                "prompt": card_prompt
            })

        return prompts

    def generate_complete_post(self, post_type: str = "morning") -> Dict:
        """生成完整的帖子内容"""
        print("=" * 60)
        print("🐱 小红书宠物内容生成器")
        print("=" * 60)
        print(f"📅 生成日期: {get_today_date()}")
        print(f"⏰ 发布时段: {post_type} ({'早间' if post_type == 'morning' else '晚间'})")
        print("=" * 60)

        # 1. 选择宠物类型
        pet_type = random.choice(["猫咪", "狗狗", "猫咪和狗狗"])
        print(f"🐾 宠物类型: {pet_type}")

        # 2. 获取热点话题
        print("\n🔥 获取今日热点...")
        hot_topics = self.hot_tracker.get_mock_hot_topics()
        top_hot = hot_topics[0] if hot_topics else {"topic": "日常"}
        print(f"   热点: {top_hot['topic']} (热度: {top_hot['heat']})")

        # 3. 生成问题
        print("\n❓ 生成测试问题...")
        questions = self.generate_questions(pet_type)

        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q['question'][:30]}...")
            print(f"      A. {q['options']['A']} | B. {q['options']['B']}")

        # 4. 生成正文
        print("\n📝 生成正文内容...")
        body_content = self.generate_body_content(pet_type, questions)

        # 5. 生成图片提示词
        print("\n🎨 生成图片提示词...")
        image_prompts = self.generate_image_prompts(questions)

        # 6. 构建完整帖子
        post = {
            "meta": {
                "date": get_today_date(),
                "post_type": post_type,
                "pet_type": pet_type,
                "hot_topic": top_hot['topic'],
                "generated_at": datetime.now().isoformat()
            },
            "questions": questions,
            "body": body_content,
            "image_prompts": image_prompts,
            "call_to_action": {
                "scoring": {
                    "excellent": "答对3个 = 优秀铲屎官 🌟",
                    "qualified": "答对2个 = 合格铲屎官 💪",
                    "poor": "答对1个 = 差劲铲屎官 😅"
                },
                "action": "请在评论区留下你的答案",
                "reveal_time": "次日会揭晓答案",
                "giveaway": "随机抽取1-3名优秀铲屎官送出宠物试用装",
                "encouragement": "欢迎大家积极参与"
            }
        }

        # 7. 保存帖子
        print("\n💾 保存内容...")
        date_str = get_today_date()
        content_dir = get_content_path("xiaohongshu", date_str)
        content_dir.mkdir(parents=True, exist_ok=True)

        filepath = content_dir / f"post_{post_type}_{date_str}.json"
        save_json_file(filepath, post)

        # 保存到data/records
        records_dir = Path(__file__).parent.parent / "data" / "records"
        records_dir.mkdir(parents=True, exist_ok=True)
        record_file = records_dir / f"{date_str}_{post_type}_post.json"
        save_json_file(record_file, post)

        # 8. 显示预览
        print("\n" + "=" * 60)
        print("📋 内容预览")
        print("=" * 60)
        print(f"🐾 宠物: {pet_type}")
        print(f"🔥 热点: {top_hot['topic']}")
        print(f"\n📝 正文开头:")
        print(f"   {body_content['intro']}")
        print(f"\n💬 CTA:")
        print(f"   {body_content['cta']}")
        print(f"\n🏷️ 标签:")
        print(f"   {' '.join(body_content['hashtags'])}")
        print("=" * 60)
        print("✅ 内容生成完成!")
        print("=" * 60)

        return post


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="小红书宠物内容生成器")
    parser.add_argument(
        "--type",
        type=str,
        default="morning",
        choices=["morning", "evening", "both"],
        help="发布类型: morning(早间), evening(晚间), both(都生成)"
    )

    args = parser.parse_args()

    generator = PetContentGenerator()

    if args.type == "both":
        # 生成早晚两篇
        morning_post = generator.generate_complete_post("morning")
        print("\n" + "=" * 60)
        evening_post = generator.generate_complete_post("evening")
    else:
        # 生成单篇
        generator.generate_complete_post(args.type)


if __name__ == "__main__":
    main()
