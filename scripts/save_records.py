#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录保存器
保存每日运营记录和统计数据
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_today_date, DATA_DIR


class RecordSaver:
    """记录保存器"""

    def __init__(self):
        self.records_dir = DATA_DIR / "records"
        self.records_dir.mkdir(parents=True, exist_ok=True)

        self.stats_dir = DATA_DIR / "statistics"
        self.stats_dir.mkdir(parents=True, exist_ok=True)

    def load_daily_record(self, date: str = None) -> dict:
        """加载某日的记录"""
        if date is None:
            date = get_today_date()

        record_file = self.records_dir / f"{date}_content.json"
        publish_file = self.records_dir / f"{date}_publish_results.json"

        record = {
            "date": date,
            "content": None,
            "publish_results": None
        }

        if record_file.exists():
            with open(record_file, 'r', encoding='utf-8') as f:
                record["content"] = json.load(f)

        if publish_file.exists():
            with open(publish_file, 'r', encoding='utf-8') as f:
                record["publish_results"] = json.load(f)

        return record

    def save_daily_summary(self, date: str = None) -> dict:
        """保存每日汇总"""
        if date is None:
            date = get_today_date()

        record = self.load_daily_record(date)

        summary = {
            "date": date,
            "generated": record["content"] is not None,
            "published": {},
            "platforms": []
        }

        # 统计发布结果
        if record["publish_results"]:
            for platform, result in record["publish_results"].items():
                status = result.get("status", "unknown")
                summary["published"][platform] = status
                summary["platforms"].append({
                    "name": platform,
                    "status": status,
                    "id": result.get("note_id") or result.get("media_id", "")
                })

        # 保存汇总
        summary_file = self.records_dir / f"{date}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        return summary

    def update_statistics(self):
        """更新整体统计数据"""
        stats = {
            "last_updated": datetime.now().isoformat(),
            "total_posts": 0,
            "total_published": 0,
            "platform_stats": defaultdict(lambda: {"generated": 0, "published": 0}),
            "daily_posts": [],
            "category_distribution": defaultdict(int)
        }

        # 遍历所有记录文件
        for record_file in self.records_dir.glob("*_summary.json"):
            date_str = record_file.stem.replace("_summary", "")

            try:
                with open(record_file, 'r', encoding='utf-8') as f:
                    summary = json.load(f)

                # 统计每日发布
                if summary.get("generated"):
                    stats["total_posts"] += 1
                    stats["daily_posts"].append({
                        "date": date_str,
                        "generated": True,
                        "published": list(summary["published"].values())
                    })

                    # 统计平台
                    for platform, status in summary["published"].items():
                        stats["platform_stats"][platform]["generated"] += 1
                        if status == "success":
                            stats["total_published"] += 1
                            stats["platform_stats"][platform]["published"] += 1

            except Exception as e:
                print(f"⚠️ 处理记录文件失败: {record_file} - {e}")

        # 统计内容类别
        for content_file in self.records_dir.glob("*_content.json"):
            try:
                with open(content_file, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    category = content.get("category", "未分类")
                    stats["category_distribution"][category] += 1
            except Exception as e:
                print(f"⚠️ 处理内容文件失败: {content_file} - {e}")

        # 转换defaultdict为普通dict
        stats["platform_stats"] = dict(stats["platform_stats"])
        stats["category_distribution"] = dict(stats["category_distribution"])

        # 按日期排序
        stats["daily_posts"].sort(key=lambda x: x["date"], reverse=True)

        # 保存统计
        stats_file = self.stats_dir / "overall_statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        return stats

    def generate_report(self) -> str:
        """生成运营报告"""
        stats = self.update_statistics()
        today = get_today_date()

        report_lines = [
            "=" * 60,
            "📊 媒体运营自动化系统 - 运营报告",
            "=" * 60,
            f"📅 报告日期: {today}",
            f"⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "📈 整体统计:",
            "-" * 40,
            f"   总生成内容: {stats['total_posts']} 篇",
            f"   总成功发布: {stats['total_published']} 篇",
            f"   发布成功率: {stats['total_published']/stats['total_posts']*100:.1f}%" if stats['total_posts'] > 0 else "   发布成功率: N/A",
            "",
            "📱 平台统计:",
            "-" * 40,
        ]

        for platform, platform_stats in stats["platform_stats"].items():
            platform_name = "小红书" if platform == "xiaohongshu" else "公众号"
            rate = platform_stats["published"] / platform_stats["generated"] * 100 if platform_stats["generated"] > 0 else 0
            report_lines.append(f"   {platform_name}:")
            report_lines.append(f"      生成: {platform_stats['generated']} 篇")
            report_lines.append(f"      发布: {platform_stats['published']} 篇")
            report_lines.append(f"      成功率: {rate:.1f}%")

        report_lines.extend([
            "",
            "📂 类别分布:",
            "-" * 40,
        ])

        for category, count in sorted(stats["category_distribution"].items(), key=lambda x: x[1], reverse=True):
            report_lines.append(f"   {category}: {count} 篇")

        report_lines.extend([
            "",
            "📅 近期发布记录:",
            "-" * 40,
        ])

        for daily in stats["daily_posts"][:7]:  # 最近7天
            date = daily["date"]
            published_count = sum(1 for p in daily["published"] if p == "success")
            report_lines.append(f"   {date}: {published_count}/2 平台发布成功")

        report_lines.extend([
            "",
            "=" * 60,
            "报告生成完毕",
            "=" * 60,
        ])

        report = "\n".join(report_lines)
        print(report)

        # 保存报告
        report_file = self.records_dir / f"report_{today}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n💾 报告已保存到: {report_file}")

        return report


def main():
    """主函数"""
    print("=" * 60)
    print("💾 媒体运营自动化 - 记录保存器")
    print("=" * 60)

    saver = RecordSaver()

    # 保存今日汇总
    print("📝 保存今日汇总...")
    summary = saver.save_daily_summary()
    print(f"   状态: {'已生成' if summary['generated'] else '未生成'}")

    if summary["published"]:
        for platform, status in summary["published"].items():
            platform_name = "小红书" if platform == "xiaohongshu" else "公众号"
            print(f"   {platform_name}: {status}")

    # 更新统计
    print("\n📊 更新整体统计数据...")
    stats = saver.update_statistics()
    print(f"   总生成: {stats['total_posts']} 篇")
    print(f"   总发布: {stats['total_published']} 篇")

    # 生成报告
    print("\n📋 生成运营报告...")
    saver.generate_report()

    print("\n✅ 记录保存完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
