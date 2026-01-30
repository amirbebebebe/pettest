#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions 小红书发布器
使用Selenium + Chrome直接发布内容
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import XIAOHONGSHU_COOKIE


class GitHubActionsPublisher:
    """GitHub Actions环境下的发布器"""
    
    def __init__(self):
        self.cookie = XIAOHONGSHU_COOKIE
        self.driver = None
    
    def setup_driver(self):
        """设置ChromeDriver"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        print("🚀 初始化Chrome浏览器...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # 启动浏览器
        self.driver = webdriver.Chrome(options=chrome_options)
        
        print("✅ Chrome浏览器启动成功")
        return True
    
    def login_with_cookies(self):
        """使用cookies登录"""
        print("📱 登录小红书...")
        
        self.driver.get("https://www.xiaohongshu.com/")
        time.sleep(3)
        
        # 添加cookies
        if self.cookie:
            print("🍪 使用预置cookies登录...")
            cookies = parse_cookie_string(self.cookie)
            for name, value in cookies.items():
                self.driver.add_cookie({"name": name, "value": value})
            
            # 刷新页面
            self.driver.refresh()
            time.sleep(3)
        
        # 检查登录状态
        try:
            # 尝试查找登录后的元素
            self.driver.find_element("xpath", "//div[contains(@class, 'avatar')]")
            print("✅ 登录成功！")
            return True
        except:
            print("❌ 登录失败，需要扫码登录")
            return False
    
    def publish_note(self, title: str, content: str, image_paths: list) -> dict:
        """发布笔记"""
        print(f"📝 发布笔记: {title}")
        
        try:
            # 跳转发布页面
            self.driver.get("https://www.xiaohongshu.com/creator/publish/publish")
            time.sleep(3)
            
            # 检查是否需要登录
            if "登录" in self.driver.page_source:
                print("❌ 未登录，请先登录")
                return {"status": "failed", "error": "Not logged in"}
            
            # 输入标题
            title_input = self.driver.find_element("xpath", "//input[contains(@placeholder, '标题')]")
            title_input.clear()
            title_input.send_keys(title)
            
            # 输入正文
            content_area = self.driver.find_element("xpath", "//textarea[contains(@placeholder, '说')]")
            content_area.clear()
            content_area.send_keys(content)
            
            # 上传图片（如果有）
            for img_path in image_paths:
                if os.path.exists(img_path):
                    file_input = self.driver.find_element("xpath", "//input[@type='file']")
                    file_input.send_keys(img_path)
                    time.sleep(2)
            
            # 点击发布按钮
            publish_btn = self.driver.find_element("xpath", "//button[contains(text(), '发布')]")
            publish_btn.click()
            
            # 等待发布完成
            time.sleep(5)
            
            print("✅ 笔记发布成功！")
            return {"status": "success", "title": title}
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return {"status": "failed", "error": str(e)}
    
    def cleanup(self):
        """清理资源"""
        if self.driver:
            self.driver.quit()
            print("🔒 浏览器已关闭")


def parse_cookie_string(cookie_str: str) -> dict:
    """解析cookie字符串为字典"""
    cookies = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            name, value = item.split("=", 1)
            cookies[name.strip()] = value.strip()
    return cookies


def publish_content(post_type: str = "both"):
    """发布内容"""
    publisher = GitHubActionsPublisher()
    
    try:
        # 设置浏览器
        publisher.setup_driver()
        
        # 登录
        publisher.login_with_cookies()
        
        # 发布今日内容
        today = datetime.now().strftime("%Y-%m-%d")
        content_dir = Path(__file__).parent.parent / "content" / today
        
        if not content_dir.exists():
            print(f"❌ 今日内容不存在: {content_dir}")
            return
        
        # 查找内容文件
        for content_file in sorted(content_dir.glob("*.json")):
            print(f"📄 处理内容文件: {content_file.name}")
            
            with open(content_file, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            # 收集图片
            image_paths = []
            for img in content_data.get("images", []):
                img_path = Path(__file__).parent.parent / img
                if img_path.exists():
                    image_paths.append(str(img_path))
            
            # 发布
            result = publisher.publish_note(
                title=content_data.get("title", ""),
                content=content_data.get("content", ""),
                image_paths=image_paths
            )
            
            print(f"📊 发布结果: {result}")
            
            # 标记为已发布
            content_file.rename(content_file.with_suffix(content_file.suffix + ".published"))
            
            # 避免发布太快
            time.sleep(10)
        
        print("🎉 所有内容发布完成！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        publisher.cleanup()


if __name__ == "__main__":
    post_type = sys.argv[1] if len(sys.argv) > 1 else "both"
    publish_content(post_type)
