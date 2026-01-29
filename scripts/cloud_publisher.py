#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 云端自动化发布服务
在云服务器上运行，接收GitHub Actions的Webhook触发，自动发布内容
"""

import sys
import json
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Optional
from flask import Flask, request, jsonify
import requests

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    VOLCANO_API_KEY, VOLCANO_API_SECRET, VOLCANO_MODEL, VOLCANO_API_BASE,
    WECHAT_APPID, WECHAT_APPSECRET, get_today_date
)

app = Flask(__name__)


class CloudPublisher:
    """云端发布器"""

    def __init__(self):
        self.wechat_appid = WECHAT_APPID
        self.wechat_appsecret = WECHAT_APPSECRET
        self.wechat_access_token = None
        self.last_token_time = None
        self.token_expire_seconds = 7000  # 微信token有效期2小时

    def get_wechat_token(self) -> Optional[str]:
        """获取微信access_token"""
        # 检查是否过期
        if (self.wechat_access_token and 
            self.last_token_time and 
            (datetime.now() - self.last_token_time).seconds < self.token_expire_seconds):
            return self.wechat_access_token

        if not self.wechat_appid or not self.wechat_appsecret:
            return None

        import requests
        
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.wechat_appid,
            "secret": self.wechat_appsecret
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if "access_token" in data:
                self.wechat_access_token = data["access_token"]
                self.last_token_time = datetime.now()
                return self.wechat_access_token
            
            return None
        except:
            return None

    def publish_to_xiaohongshu(self, title: str, content: str, image_paths: list) -> dict:
        """发布到小红书（使用xhs-mcp-server）"""
        print(f"🚀 发布到小红书...")
        print(f"   标题: {title}")
        print(f"   内容长度: {len(content)} 字")
        print(f"   图片数: {len(image_paths)}")

        try:
            # 构建命令
            images_str = ",".join(image_paths) if image_paths else ""
            
            cmd = [
                "python", "-m", "xhs_mcp_server.__publish__",
                "--title", title,
                "--content", content,
                "--images", images_str
            ]
            
            # 在后台线程执行
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("✅ 小红书发布成功!")
                return {"status": "success", "platform": "xiaohongshu"}
            else:
                print(f"❌ 小红书发布失败: {result.stderr}")
                return {"status": "failed", "platform": "xiaohongshu", "error": result.stderr}
                
        except Exception as e:
            print(f"❌ 发布错误: {e}")
            return {"status": "failed", "platform": "xiaohongshu", "error": str(e)}

    def publish_to_wechat(self, title: str, content: str, image_paths: list) -> dict:
        """发布到公众号"""
        print(f"📤 发布到公众号...")
        print(f"   标题: {title}")

        # 获取token
        token = self.get_wechat_token()
        if not token:
            return {"status": "failed", "platform": "wechat", "error": "No access token"}

        import requests

        # 上传封面图
        thumb_media_id = None
        if image_paths and len(image_paths) > 0:
            try:
                url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg"
                params = {"access_token": token}
                
                with open(image_paths[0], 'rb') as f:
                    files = {'media': f}
                    response = requests.post(url, params=params, files=files, timeout=30)
                    data = response.json()
                    
                if "media_id" in data:
                    thumb_media_id = data["media_id"]
                    print("✅ 封面上传成功")
            except Exception as e:
                print(f"⚠️ 封面上传失败: {e}")

        # 创建草稿
        article = {
            "title": title,
            "content": content,
            "thumb_media_id": thumb_media_id,
            "show_cover_pic": 1,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }

        try:
            url = f"https://api.weixin.qq.com/cgi-bin/draft/add"
            params = {"access_token": token}
            payload = {"articles": [article]}
            
            response = requests.post(url, params=params, json=payload, timeout=30)
            data = response.json()
            
            if data.get("errcode") == 0:
                print("✅ 公众号草稿创建成功!")
                return {
                    "status": "success",
                    "platform": "wechat",
                    "draft_id": data["media_id"]
                }
            else:
                return {"status": "failed", "platform": "wechat", "error": data}
                
        except Exception as e:
            return {"status": "failed", "platform": "wechat", "error": str(e)}

    def publish_all(self, content: dict) -> dict:
        """发布到所有平台"""
        results= {}
        
        # 提取内容
        body = content.get("body", {})
        intro = body.get("intro", "")
        main_body = body.get("body", "")
        cta = body.get("cta", "")
        
        title = "测测你是不是合格铲屎官？送宠物试用装了！"
        full_content = f"{intro}\n\n{main_body}\n\n{cta}"
        
        # 获取图片
        image_paths = []
        meta = content.get("meta", {})
        date_str = meta.get("date", get_today_date())
        images_dir = Path(__file__).parent / "content" / "xiaohongshu" / date_str
        
        if images_dir.exists():
            for img in sorted(images_dir.glob("*.png")):
                image_paths.append(str(img))
        
        # 并行发布到两个平台
        def publish_xhs():
            results["xiaohongshu"] = self.publish_to_xiaohongshu(title, full_content, image_paths)
        
        def publish_wechat():
            results["wechat"] = self.publish_to_wechat(title, full_content, image_paths)
        
        # 启动两个线程
        t1 = threading.Thread(target=publish_xhs)
        t2 = threading.Thread(target=publish_wechat)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        return results


# 初始化发布器
publisher = CloudPublisher()


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook端点：接收GitHub Actions的触发
    """
    try:
        data = request.json
        
        print(f"\n{'='*60}")
        print("🚀 收到Webhook触发!")
        print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📝 事件: {request.headers.get('X-GitHub-Event', 'unknown')}")
        print(f"{'='*60}\n")
        
        # 获取内容文件
        records_dir = Path(__file__).parent / "data" / "records"
        date_str = get_today_date()
        
        # 查找最新的内容文件
        content_files = list(records_dir.glob(f"{date_str}*_post.json"))
        content_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not content_files:
            return jsonify({
                "status": "error",
                "message": "未找到今日内容文件"
            }), 404
        
        # 加载内容
        with open(content_files[0], 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        print(f"✅ 加载内容: {content_files[0].name}")
        
        # 发布到所有平台
        results = publisher.publish_all(content)
        
        print(f"\n📊 发布结果:")
        print(json.dumps(results, ensure_ascii=False, indent=2))
        
        return jsonify({
            "status": "success",
            "message": "发布完成",
            "results": results
        })
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "time": datetime.now().isoformat()
    })


@app.route('/publish', methods=['POST'])
def manual_publish():
    """
    手动触发发布接口
    """
    try:
        content = request.json
        results = publisher.publish_all(content)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def run_flask():
    """运行Flask服务"""
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 云端自动化发布服务启动")
    print("="*60)
    print("📡 服务地址: http://0.0.0.0:5000")
    print("🔗 Webhook: http://你的域名/webhook")
    print("💡 健康检查: http://你的域名/health")
    print("="*60 + "\n")
    
    run_flask()
