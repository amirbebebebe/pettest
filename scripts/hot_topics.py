#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点追踪器
自动追踪微博、抖音、小红书等平台的热门话题
并将其与宠物内容结合
"""

import sys
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    HOT_TOPIC_CONFIG, PET_TOPIC_CATEGORIES, get_today_date, save_json_file
)


class HotTopicTracker:
    """热点话题追踪器"""

    def __init__(self):
        self.config = HOT_TOPIC_CONFIG
        self.topics_dir = Path(__file__).parent.parent / "data" / "hot_topics"
        self.topics_dir.mkdir(parents=True, exist_ok=True)

    def get_mock_hot_topics(self) -> List[Dict]:
        """
        获取模拟热点话题
        实际使用时，可以接入微博热搜API、抖音热点API等
        """
        # 当前时间相关热点
        current_month = datetime.now().month
        current_day = datetime.now().day
        current_weekday = datetime.now().weekday()

        # 节假日/节气热点
        holiday_topics = {
            1: ["新年愿望", "春节", "年终奖", "跨年", "元旦"],
            2: ["春节", "情人节", "年后复工", "立春"],
            3: ["妇女节", "315消费者权益日", "春游", "植树节"],
            4: ["清明节", "愚人节", "踏青", "春暖花开"],
            5: ["劳动节", "母亲节", "青年节", "立夏"],
            6: ["儿童节", "端午节", "父亲节", "高考"],
            7: ["建党节", "暑假", "毕业季", "夏日清凉"],
            8: ["八一建军节", "七夕", "七夕节", "夏日清凉"],
            9: ["教师节", "中秋节", "白露", "秋分"],
            10: ["国庆节", "中秋节", "重阳节", "黄金周"],
            11: ["双十一", "感恩节", "光棍节", "秋冬换季"],
            12: ["双十二", "圣诞节", "跨年", "年终总结", "冬至"]
        }

        # 星期相关热点
        weekday_topics = {
            0: ["周一综合症", "新的一周", "工作日"],
            1: ["周一上班", "新周开始", "周一头条"],
            2: ["周二快乐", "周中休息", "工作日"],
            3: ["周三过半", "周中", "工作日"],
            4: ["周四期待", "周五前夜", "周四快乐"],
            5: ["周五啦", "周末出行", "周五快乐", "周末计划"],
            6: ["周末愉快", "周日休闲", "周末生活", "周日晚上"]
        }

        # 通用热点话题池（模拟）
        general_hot_topics = [
            # 社会热点
            "职场生存", "副业赚钱", "打工人", "租房", "相亲",
            # 生活热点
            "一人食", "租房改造", "精致生活", "极简生活", "养生",
            # 娱乐热点
            "追剧", "综艺", "电影", "游戏", "追星",
            # 情感热点
            "恋爱", "婚姻", "友情", "原生家庭", "自我成长",
            # 季节热点
            "换季穿搭", "换季护肤", "夏季清凉", "冬季保暖", "春季过敏",
            # 时间节点
            "周末计划", "假期旅行", "宅家生活", "下班后的生活"
        ]

        # 宠物相关热点（用于关联）
        pet_hot_topics = [
            "宠物情缘", "毛孩子", "萌宠", "宠物日常", "铲屎官",
            "猫奴", "狗奴", "宠物表情包", "宠物趣事", "宠物美容"
        ]

        # 组合热点话题
        hot_topics = []

        # 添加节假日热点
        month_topics = holiday_topics.get(current_month, [])
        for topic in month_topics[:2]:
            hot_topics.append({
                "topic": topic,
                "category": "节日节气",
                "heat": random.randint(80, 100),
                "source": "calendar"
            })

        # 添加星期热点
        if current_weekday in weekday_topics:
            for topic in weekday_topics[current_weekday][:1]:
                hot_topics.append({
                    "topic": topic,
                    "category": "时间节点",
                    "heat": random.randint(60, 90),
                    "source": "calendar"
                })

        # 添加通用热点
        for topic in random.sample(general_hot_topics, min(8, len(general_hot_topics))):
            hot_topics.append({
                "topic": topic,
                "category": "社会生活",
                "heat": random.randint(50, 85),
                "source": "general"
            })

        # 添加宠物热点
        for topic in random.sample(pet_hot_topics, min(5, len(pet_hot_topics))):
            hot_topics.append({
                "topic": topic,
                "category": "宠物相关",
                "heat": random.randint(55, 90),
                "source": "pet"
            })

        # 按热度排序
        hot_topics.sort(key=lambda x: x["heat"], reverse=True)

        return hot_topics

    def generate_pet_questions(self, topic: str = None, count: int = 3) -> List[Dict]:
        """
        生成宠物问题（基于热点话题关联）
        """
        questions = []

        # 如果没有指定话题，从各类别中随机选择
        if not topic:
            all_topics = []
            for category, topics in PET_TOPIC_CATEGORIES.items():
                if category != "热点结合":  # 排除热点结合类别
                    for t in topics:
                        all_topics.append((category, t))

            # 随机选择问题类型
            question_types = random.sample(
                PET_TOPIC_CATEGORIES.keys(),
                min(count, len(PET_TOPIC_CATEGORIES.keys()))
            )

            for qtype in question_types:
                category_topics = PET_TOPIC_CATEGORIES[qtype]
                selected_topic = random.choice(category_topics)

                question = self._generate_single_question(qtype, selected_topic)
                if question:
                    questions.append(question)
        else:
            # 基于指定话题生成问题
            for i in range(count):
                qtype = random.choice(list(PET_TOPIC_CATEGORIES.keys()))
                category_topics = PET_TOPIC_CATEGORIES[qtype]
                selected_topic = random.choice(category_topics)

                question = self._generate_single_question(qtype, selected_topic)
                if question:
                    questions.append(question)

        return questions[:count]

    def _generate_single_question(self, question_type: str, topic: str) -> Optional[Dict]:
        """生成单个宠物问题"""

        # 问题库
        question_bank = {
            "基础知识": [
                {
                    "question": f"关于{topic}，你知道多少？",
                    "options": {
                        "A": "了解很多，能详细说明",
                        "B": "只知道一点点"
                    },
                    "correct": "A"
                },
                {
                    "question": f"养宠物的人必须知道的一件事：{topic}",
                    "options": {
                        "A": "正确答案",
                        "B": "错误答案"
                    },
                    "correct": "A"
                }
            ],
            "行为解读": [
                {
                    "question": f"当你家的宠物{topic}时，它在想什么？",
                    "options": {
                        "A": "在表达开心/满足",
                        "B": "在表达不满/烦躁"
                    },
                    "correct": "A"
                },
                {
                    "question": f"如果你的宠物{topic}，你应该怎么做？",
                    "options": {
                        "A": "立即回应",
                        "B": "不予理会"
                    },
                    "correct": "A"
                }
            ],
            "趣味挑战": [
                {
                    "question": f"测试你对{topic}的了解程度！",
                    "options": {
                        "A": "全部答对",
                        "B": "错一两个"
                    },
                    "correct": "A"
                },
                {
                    "question": f"关于{topic}，99%的主人都会答错！",
                    "options": {
                        "A": "我不信",
                        "B": "真的吗"
                    },
                    "correct": "A"
                }
            ]
        }

        if question_type in question_bank:
            q = random.choice(question_bank[question_type])
            return {
                "type": question_type,
                "topic": topic,
                "question": q["question"],
                "options": q["options"],
                "correct_answer": q["correct"],
                "explanation": f"关于{topic}的正确答案是{q['correct']}，你答对了吗？"
            }

        return None

    def integrate_hot_topic(self, base_topic: str, hot_topics: List[Dict]) -> str:
        """
        将热点话题与宠物内容结合
        生成一个融合后的主题
        """
        if not hot_topics:
            return base_topic

        # 选择一个合适的热点话题
        # 优先选择宠物相关或生活类热点
        relevant_topics = [
            t for t in hot_topics
            if t["category"] in ["宠物相关", "社会生活", "时间节点", "节日节气"]
            and t["heat"] > 60
        ]

        if not relevant_topics:
            relevant_topics = hot_topics[:3]

        hot_topic = random.choice(relevant_topics)

        # 融合方式
        fusion_styles = [
            f"当{hot_topic['topic']}遇上宠物：{base_topic}",
            f"{hot_topic['topic']}期间，宠物{base_topic}",
            f"宠物视角看{hot_topic['topic']}：{base_topic}",
            f"{hot_topic['topic']}限定：{base_topic}",
            f"铲屎官必知：{hot_topic['topic']}与{base_topic}"
        ]

        return random.choice(fusion_styles)

    def save_hot_topics(self, topics: List[Dict], post_type: str = "morning"):
        """保存热点话题记录"""
        date_str = get_today_date()
        filepath = self.topics_dir / f"{date_str}_{post_type}_hot_topics.json"

        record = {
            "date": date_str,
            "post_type": post_type,
            "fetched_at": datetime.now().isoformat(),
            "topics": topics
        }

        save_json_file(filepath, record)
        print(f"💾 热点话题已保存到: {filepath}")

        return filepath

    def load_saved_topics(self, date: str = None, post_type: str = None) -> List[Dict]:
        """加载保存的热点话题"""
        if date is None:
            date = get_today_date()

        if post_type:
            filepath = self.topics_dir / f"{date}_{post_type}_hot_topics.json"
            if filepath.exists():
                data = json.load(open(filepath, 'r', encoding='utf-8'))
                return data.get("topics", [])
        else:
            # 加载当天所有热点
            all_topics = []
            for f in self.topics_dir.glob(f"{date}_*_hot_topics.json"):
                data = json.load(open(f, 'r', encoding='utf-8'))
                all_topics.extend(data.get("topics", []))
            return all_topics

        return []

    def get_today_topics(self, post_type: str = "morning") -> Dict:
        """
        获取今日热点话题（用于内容生成）
        返回包含原始热点和宠物问题的字典
        """
        # 获取热点话题
        hot_topics = self.get_mock_hot_topics()

        # 保存热点
        self.save_hot_topics(hot_topics, post_type)

        # 生成宠物问题
        questions = self.generate_pet_questions(count=3)

        return {
            "date": get_today_date(),
            "post_type": post_type,
            "hot_topics": hot_topics,
            "questions": questions,
            "pet_type": random.choice(["猫咪", "狗狗", "猫咪和狗狗"])
        }


def main():
    """主函数 - 测试热点追踪"""
    print("=" * 60)
    print("🔥 热点话题追踪器 - 测试运行")
    print("=" * 60)

    tracker = HotTopicTracker()

    # 测试获取热点
    print("\n📊 获取今日热点话题...")
    hot_topics = tracker.get_mock_hot_topics()

    print(f"找到 {len(hot_topics)} 个热点话题：")
    for i, topic in enumerate(hot_topics[:5], 1):
        print(f"  {i}. {topic['topic']} ({topic['category']}) - 热度: {topic['heat']}")

    # 测试生成问题
    print("\n❓ 生成宠物问题...")
    questions = tracker.generate_pet_questions(count=3)

    for i, q in enumerate(questions, 1):
        print(f"\n问题 {i} ({q['type']})")
        print(f"  Q: {q['question']}")
        print(f"  A: {q['options']['A']}")
        print(f"  B: {q['options']['B']}")
        print(f"  正确答案: {q['correct_answer']}")

    # 测试热点融合
    print("\n🔗 测试热点融合...")
    if hot_topics:
        fused = tracker.integrate_hot_topic("日常护理知识", hot_topics)
        print(f"融合主题: {fused}")

    # 保存热点
    print("\n💾 保存热点话题...")
    tracker.save_hot_topics(hot_topics, "morning")

    print("\n✅ 测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
