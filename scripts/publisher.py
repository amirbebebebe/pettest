#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐱 小红书和公众号发布器
使用xhs-mcp-server和微信API发布内容
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    XIAOHONGSHU_COOKIE, WECHAT_APPID, WECHAT_APPSECRET, get_today_date
)


class XiaohongshuPublisher:
    """小红书发布器（使用xhs-mcp-server）"""

    def __init__(self):
        self.phone = "13810119101"  # 用户手机号
        self.cookie = XIAOHONGSHU_COOKIE

    def login(self) -> bool:
        """
        登录小红书（生成Cookie）
        需要在终端运行: env phone=你的手机号 python -m xhs_mcp_server.__login__
        """
        print("📱 登录小红书...")
        print("请在终端执行以下命令进行登录：")
        print(f"env phone={self.phone} python -m xhs_mcp_server.__login__")
        print("扫码后在小红书APP中确认登录")
        return True

    def publish_with_mcp(self, title: str, content: str, image_paths: List[str]) -> dict:
        """
        使用xhs-mcp-server发布笔记
        
        Args:
            title: 标题
            content: 正文内容
            image_paths: 图片路径列表
        """
        print(f"🚀 使用xhs-mcp-server发布笔记...")
        print(f"   标题: {title}")
        print(f"   内容长度: {len(content)} 字")
        print(f"   图片数: {len(image_paths)}")

        try:
            # 构建命令
            images_str = ",".join(image_paths) if image_paths else ""
            
            # 构建完整命令
            cmd = [
                "python", "-m", "xhs_mcp_server.__publish__",
                "--title", title,
                "--content", content,
                "--images", images_str
            ]
            
            print(f"执行命令: {' '.join(cmd)}")
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            print(f"返回码: {result.returncode}")
            print(f"stdout: {result.stdout}")
            if result.stderr:
                print(f"stderr: {result.stderr}")
            
            if result.returncode == 0:
                print("✅ 小红书发布成功!")
                return {
                    "status": "success",
                    "platform": "xiaohongshu",
                    "title": title,
                    "output": result.stdout
                }
            else:
                print(f"❌ 小红书发布失败")
                return {
                    "status": "failed",
                    "platform": "xiaohongshu",
                    "error": result.stderr or "Unknown error"
                }
                
        except subprocess.TimeoutExpired:
            print("❌ 发布超时（超过5分钟）")
            return {
                "status": "failed",
                "platform": "xiaohongshu",
                "error": "Timeout"
            }
        except Exception as e:
            print(f"❌ 发布错误: {e}")
            return {
                "status": "failed",
                "platform": "xiaohongshu",
                "error": str(e)
            }

    def publish_simulation(self, title: str, content: str, image_paths: List[str]) -> dict:
        """
        模拟发布（用于测试）
        """
        print(f"📤 模拟发布到小红书...")
        print(f"   标题: {title}")
        print(f"   图片数: {len(image_paths)}")
        
        return {
            "status": "success",
            "platform": "xiaohongshu",
            "note_id": f"note_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": title,
            "published_at": datetime.now().isoformat(),
            "mode": "simulation"
        }


class WechatPublisher:
    """公众号发布器（使用微信官方API）"""

    def __init__(self):
        self.appid = WECHAT_APPID
        self.appsecret = WECHAT_APPSECRET
        self.access_token = None

    def get_access_token(self) -> Optional[str]:
        """获取access_token"""
        if not self.appid or not self.appsecret:
            print("❌ 未配置公众号APPID或APPSECRET")
            return None

        import requests
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }

        try:
            print("🔑 获取access_token...")
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if "access_token" in data:
                self.access_token = data["access_token"]
                print("✅ 获取access_token成功")
                return self.access_token
            else:
                print(f"❌ 获取失败: {data.get('errmsg', '未知错误')}")
                return None

        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return None

    def upload_image(self, image_path: str) -> Optional[str]:
        """上传图片获取media_id"""
        if not self.access_token:
            if not self.get_access_token():
                return None

        import requests
        
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg"
        params = {"access_token": self.access_token}

        try:
            print(f"📤 上传图片: {image_path}")
            with open(image_path, 'rb') as f:
                files = {'media': f}
                response = requests.post(url, params=params, files=files, timeout=30)
                data = response.json()

            if "media_id" in data:
                print("✅ 图片上传成功")
                return data["media_id"]
            else:
                print(f"❌ 图片上传失败: {data}")
                return None

        except Exception as e:
            print(f"❌ 上传失败: {e}")
            return None

    def create_draft(self, title: str, content: str, thumb_media_id: str = None) -> Optional[str]:
        """创建草稿"""
        if not self.access_token:
            if not self.get_access_token():
                return None

        import requests

        url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
        params = {"access_token": self.access_token}

        article = {
            "title": title,
            "content": content,
            "thumb_media_id": thumb_media_id,
            "show_cover_pic": 1,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }

        payload = {"articles": [article]}

        try:
            print("📝 创建草稿...")
            response = requests.post(url, params=params, json=payload, timeout=30)
            data = response.json()

            if data.get("errcode") == 0:
                media_id = data["media_id"]
                print("✅ 草稿创建成功")
                return media_id
            else:
                print(f"❌ 创建失败: {data}")
                return None

        except Exception as e:
            print(f"❌ 创建草稿失败: {e}")
            return None

    def publish_draft(self, media_id: str) -> bool:
        """发布草稿"""
        if not self.access_token:
            if not self.get_access_token():
                return False

        import requests

        url = f"https://api.weixin.qq.com/cgi-bin/draft/publish"
        params = {"access_token": self.access_token}
        payload = {"media_id": media_id}

        try:
            print("📤 发布草稿...")
            response = requests.post(url, params=params, json=payload, timeout=30)
            data = response.json()

            if data.get("errcode") == 0:
                print("✅ 草稿发布成功")
                return True
            else:
                print(f"❌ 发布失败: {data}")
                return False

        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False

    def publish(self, title: str, content: str, image_paths: List[str] = None, auto_publish: bool = False) -> dict:
        """
        发布到公众号
        
        Args:
            title: 标题
            content: 正文内容
            image_paths: 图片路径列表
            auto_publish: 是否直接发布（True=发布，False=只创建草稿）
        """
        print(f"📤 发布到公众号...")
        print(f"   标题: {title}")
        
        # 上传封面图（如果有）
        thumb_media_id = None
        if image_paths and len(image_paths) > 0:
            thumb_media_id = self.upload_image(image_paths[0])

        # 创建草稿
        media_id = self.create_draft(title, content, thumb_media_id)
        
        if not media_id:
            return {
                "status": "failed",
                "platform": "wechat",
                "error": "Failed to create draft"
            }

        # 如果需要，自动发布
        if auto_publish:
            success = self.publish_draft(media_id)
            if not success:
                return {
                    "status": "failed",
                    "platform": "wechat",
                    "draft_id": media_id,
                    "error": "Failed to publish draft"
                }

        return {
            "status": "success",
            "platform": "wechat",
            "draft_id": media_id,
            "title": title,
            "auto_published": auto_publish,
            "published_at": datetime.now().isoformat()
        }


def load_content(file_path: str) -> Optional[dict]:
    """加载生成的内容"""
    path = Path(file_path)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def find_latest_content() -> Optional[dict]:
    """查找最新的内容文件"""
    records_dir = Path(__file__).parent.parent / "data" / "records"
    
    if not records_dir.exists():
        return None

    # 查找今日的内容文件
    date_str = get_today_date()
    
    # 按修改时间排序查找
    content_files = list(records_dir.glob(f"{date_str}*_post.json"))
    content_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    if content_files:
        return load_content(str(content_files[0]))
    
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
    parser.add_argument(
        "--local",
        action="store_true",
        help="使用本地MCP发布（需要安装xhs-mcp-server）"
    )
    parser.add_argument(
        "--auto-publish",
        action="store_true",
        help="公众号：自动发布草稿（默认只创建草稿）"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🚀 媒体运营自动化 - 平台发布器")
    print("=" * 60)
    print(f"📅 发布日期: {get_today_date()}")
    print(f"📡 发布平台: {args.platform}")
    print(f"🖥️  发布模式: {'本地MCP' if args.local else '模拟'}")
    print("=" * 60)

    # 加载内容
    if args.content:
        content = load_content(args.content)
        if not content:
            print(f"❌ 无法加载内容文件: {args.content}")
            return
    else:
        print("🔍 查找今日生成的内容...")
        content = find_latest_content()
        if not content:
            print("❌ 未找到今日生成的内容")
            print("💡 请先运行: python scripts/content_generator.py --type morning")
            return

    print("✅ 找到内容文件")

    # 提取内容
    body = content.get("body", {})
    intro = body.get("intro", "")
    main_body = body.get("body", "")
    cta = body.get("cta", "")
    
    # 构建标题和内容
    title = f"测测你是不是合格铲屎官？送宠物试用装了！"
    full_content = f"{intro}\n\n{main_body}\n\n{cta}"

    # 获取图片路径
    image_paths = []
    meta = content.get("meta", {})
    date_str = meta.get("date", get_today_date())
    images_dir = Path(__file__).parent.parent / "content" / "xiaohongshu" / date_str
    
    if images_dir.exists():
        for img in sorted(images_dir.glob("*.png")):
            image_paths.append(str(img))
        print(f"📷 找到 {len(image_paths)} 张图片")

    results = {}

    # 发布到小红书
    if args.platform in ["xiaohongshu", "all"]:
        publisher = XiaohongshuPublisher()
        
        if args.local and image_paths:
            results["xiaohongshu"] = publisher.publish_with_mcp(title, full_content, image_paths)
        else:
            results["xiaohongshu"] = publisher.publish_simulation(title, full_content, image_paths)
            if not args.local:
                print("💡 提示: 使用 --local 参数可在本地环境使用真实MCP发布")

    # 发布到公众号
    if args.platform in ["wechat", "all"]:
        publisher = WechatPublisher()
        results["wechat"] = publisher.publish(title, full_content, image_paths if 'image_paths' in dir() else [], args.auto_publish)

    # 打印结果
    print("\n" + "=" * 60)
    print("📊 发布结果汇总:")
    print("-" * 60)

    for platform, result in results.items():
        platform_name = "小红书" if platform == "xiaohongshu" else "公众号"
        status = result.get("status", "unknown")
        print(f"\n{platform_name}:")
        print(f"  状态: {status}")
        
        if result.get("note_id"):
            print(f"  笔记ID: {result['note_id']}")
        if result.get("draft_id"):
            print(f"  草稿ID: {result['draft_id']}")
        if result.get("mode"):
            print(f"  模式: {result['mode']}")

    print("\n" + "=" * 60)

    # 保存发布记录
    records_dir = Path(__file__).parent.parent / "data" / "records"
    records_dir.mkdir(parents=True, exist_ok=True)
    
    record_file = records_dir / f"{get_today_date()}_publish_results.json"
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"💾 发布记录已保存到: {record_file}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
