#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平台发布器
自动将内容发布到小红书和公众号
"""

import sys
import argparse
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    XIAOHONGSHU_COOKIE, XIAHONGSHU_XS,
    WECHAT_APPID, WECHAT_APPSECRET, WECHAT_TOKEN,
    PUBLISH_CONFIG, get_today_date, load_json_file, get_content_path
)


class XiaohongshuPublisher:
    """小红书发布器"""

    def __init__(self):
        self.cookie = XIAOHONGSHU_COOKIE
        self.xs = XIAHONGSHU_XS
        self.base_url = "https://www.xiaohongshu.com"
        self.config = PUBLISH_CONFIG["xiaohongshu"]

    def _get_headers(self) -> dict:
        """获取请求头"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://www.xiaohongshu.com/",
            "Cookie": self.cookie
        }

    def _format_content(self, content: dict) -> dict:
        """格式化内容为小红书发布格式"""
        # 小红书标题限制
        title = content.get("title", "")[:self.config["title_max_length"]]

        # 小红书正文
        body = content.get("content", "")

        # 话题标签
        hashtags = content.get("hashtags", [])

        # 构建小红书格式的内容
        formatted = {
            "title": title,
            "content": body,
            "topic_tags": hashtags,
            "image_ids": [],  # 上传图片后获取的ID
            "visible_type": "public"  # 公开可见
        }

        return formatted

    def publish(self, content: dict) -> dict:
        """发布内容到小红书"""
        if not self.config["enabled"]:
            print("⚠️ 小红书发布已禁用")
            return {"status": "skipped", "reason": "publishing disabled"}

        if not self.cookie:
            print("❌ 未配置小红书Cookie，无法发布")
            return {"status": "failed", "reason": "no cookie configured"}

        print("📤 正在发布到小红书...")
        print(f"   标题: {content.get('title', '无标题')}")

        try:
            # TODO: 实现实际的小红书API调用
            # 由于小红书没有公开API，这里需要使用Selenium模拟登录发布
            # 或者使用第三方API服务

            # 模拟发布流程
            formatted = self._format_content(content)

            # 这里调用实际的小红书发布API
            # response = requests.post(
            #     f"{self.base_url}/api/sns/web/v1/note/publish",
            #     headers=self._get_headers(),
            #     json=formatted
            # )

            print("✅ 小红书发布请求已发送（模拟）")
            print(f"   格式化内容: {json.dumps(formatted, ensure_ascii=False)[:200]}...")

            return {
                "status": "success",
                "platform": "xiaohongshu",
                "note_id": f"note_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "published_at": datetime.now().isoformat(),
                "content": formatted
            }

        except Exception as e:
            print(f"❌ 小红书发布失败: {e}")
            return {
                "status": "failed",
                "platform": "xiaohongshu",
                "error": str(e)
            }


class WechatPublisher:
    """公众号发布器"""

    def __init__(self):
        self.appid = WECHAT_APPID
        self.appsecret = WECHAT_APPSECRET
        self.token = WECHAT_TOKEN
        self.base_url = "https://api.weixin.qq.com"
        self.config = PUBLISH_CONFIG["wechat"]

    def _get_access_token(self) -> Optional[str]:
        """获取access_token"""
        if not self.appid or not self.appsecret:
            print("❌ 未配置公众号APPID或APPSECRET")
            return None

        url = f"{self.base_url}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }

        try:
            import requests
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if "access_token" in data:
                return data["access_token"]
            else:
                print(f"❌ 获取access_token失败: {data.get('errmsg', '未知错误')}")
                return None

        except Exception as e:
            print(f"❌ 请求access_token失败: {e}")
            return None

    def _format_content(self, content: dict) -> dict:
        """格式化内容为公众号发布格式"""
        # 公众号标题
        title = content.get("title", "")[:self.config["title_max_length"]]

        # 公众号正文（需要添加一些格式）
        body = content.get("content", "")

        # 格式化HTML内容
        html_content = self._format_html(body)

        # 封面图
        image_path = content.get("image_path")

        formatted = {
            "title": title,
            "content": html_content,
            "content_source_url": "",  # 原文链接
            "thumb_media_id": "",  # 需要先上传图片获取
            "show_cover_pic": 1,  # 显示封面图
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }

        return formatted

    def _format_html(self, text: str) -> str:
        """将文本转换为HTML格式"""
        # 简单的段落格式化
        paragraphs = text.split('\n\n')
        html_paragraphs = []

        for para in paragraphs:
            if para.strip():
# 替换换行符为<br>
                para_html = para.replace('\n', '<br>')
                html_paragraphs.append(f"<p>{para_html}</p>")

        return '\n'.join(html_paragraphs)

    def publish(self, content: dict) -> dict:
        """发布内容到公众号"""
        if not self.config["enabled"]:
            print("⚠️ 公众号发布已禁用")
            return {"status": "skipped", "reason": "publishing disabled"}

        if not self.appid or not self.appsecret:
            print("❌ 未配置公众号凭证，无法发布")
            return {"status": "failed", "reason": "no credentials configured"}

        print("📤 正在发布到公众号...")
        print(f"   标题: {content.get('title', '无标题')}")

        try:
            # 获取access_token
            access_token = self._get_access_token()
            if not access_token:
                return {"status": "failed", "reason": "no access token"}

            # 格式化内容
            formatted = self._format_content(content)

            # 发布草稿
            # 注意：公众号需要先创建草稿，然后发布
            # 这里使用发布草稿的接口
            url = f"{self.base_url}/cgi-bin/draft/submit"
            params = {"access_token": access_token}

            payload = {
                "media_id": ""  # 草稿media_id
            }

            # TODO: 实现实际的公众号API调用
            # 完整的流程：
            # 1. 上传图片获取thumb_media_id
            # 2. 创建草稿
            # 3. 发布草稿

            print("✅ 公众号发布请求已发送（模拟）")
            print(f"   格式化内容: {json.dumps(formatted, ensure_ascii=False)[:200]}...")

            return {
                "status": "success",
                "platform": "wechat",
                "media_id": f"media_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "published_at": datetime.now().isoformat(),
                "content": formatted
            }

        except Exception as e:
            print(f"❌ 公众号发布失败: {e}")
            return {
                "status": "failed",
                "platform": "wechat",
                "error": str(e)
            }


def load_latest_content() -> Optional[dict]:
    """加载今日生成的内容"""
    date_str = get_today_date()

    # 尝试从记录文件加载
    records_dir = Path(__file__).parent.parent / "data" / "records"
    record_file = records_dir / f"{date_str}_content.json"

    if record_file.exists():
        return load_json_file(record_file)

    # 尝试从内容目录加载
    content_dir = get_content_path("xiaohongshu", date_str)

    if content_dir.exists():
        for json_file in content_dir.glob("*.json"):
            content = load_json_file(json_file)
            if content:
                return content

    print("❌ 未找到今日生成的内容")
    return None


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="平台内容发布器")
    parser.add_argument(
        "--platform",
        type=str,
        default="all",
        choices=["xiaohongshu", "wechat", "all"],
        help="发布平台 (默认: all)"
    )
    parser.add_argument(
        "--content",
        type=str,
        default=None,
        help="指定内容文件路径 (默认: 自动加载今日内容)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🚀 媒体运营自动化 - 平台发布器")
    print("=" * 60)
    print(f"📅 发布日期: {get_today_date()}")
    print(f"⏰ 发布时间: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📡 发布平台: {args.platform}")
    print("=" * 60)

    # 加载内容
    if args.content:
        content = load_json_file(Path(args.content))
    else:
        content = load_latest_content()

    if not content:
        print("❌ 没有可发布的内容")
        sys.exit(1)

    results = {}

    # 发布到小红书
    if args.platform in ["xiaohongshu", "all"]:
        publisher = XiaohongshuPublisher()
        results["xiaohongshu"] = publisher.publish(content)

    # 发布到公众号
    if args.platform in ["wechat", "all"]:
        publisher = WechatPublisher()
        results["wechat"] = publisher.publish(content)

    # 保存发布记录
    records_dir = Path(__file__).parent.parent / "data" / "records"
    records_dir.mkdir(parents=True, exist_ok=True)

    record_file = records_dir / f"{get_today_date()}_publish_results.json"

    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("📊 发布结果汇总:")
    print("-" * 60)

    for platform, result in results.items():
        status = result.get("status", "unknown")
        platform_name = "小红书" if platform == "xiaohongshu" else "公众号"
        print(f"   {platform_name}: {status}")

        if result.get("note_id"):
            print(f"      文章ID: {result['note_id']}")
        if result.get("media_id"):
            print(f"      媒体ID: {result['media_id']}")

    print("-" * 60)
    print(f"💾 记录已保存到: {record_file}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
