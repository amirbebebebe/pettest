#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地小红书登录工具 - 使用Playwright
在本地浏览器中登录小红书并获取cookies
"""

import asyncio
from playwright.async_api import async_playwright
import json
import os
from pathlib import Path


async def get_xhs_cookies():
    """使用Playwright获取小红书cookies"""
    
    print("🚀 启动浏览器...")
    
    async with async_playwright() as p:
        # 启动浏览器（无头模式=False，方便查看）
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        # 创建新页面
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        print("📱 打开小红书登录页面...")
        await page.goto('https://www.xiaohongshu.com/', timeout=30000)
        
        # 等待页面加载
        await page.wait_for_load_state('networkidle')
        
        print("⏳ 请在浏览器中完成登录...")
        print("   1. 点击登录按钮")
        print("   2. 使用手机号 13810119101 登录")
        print("   3. 完成短信验证码验证")
        
        # 等待用户登录（检测登录成功标志）
        try:
            # 等待最多120秒让用户完成登录
            await page.wait_for_function(
                """() => {
                    const cookies = document.cookie;
                    return cookies.includes('web_session') && cookies.includes('a1');
                }""",
                timeout=120000  # 120秒超时
            )
            print("✅ 检测到登录成功！")
        except asyncio.TimeoutError:
            print("⏰ 等待超时，请确保已登录")
            print("   提示：登录后页面会显示您的头像")
        
        # 获取cookies
        cookies = await context.cookies('https://www.xiaohongshu.com/')
        
        # 关闭浏览器
        await browser.close()
        
        # 转换为字符串格式
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        cookie_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
        
        return cookie_str, cookie_dict


async def save_cookies(cookie_str: str, output_dir: str = None):
    """保存cookies到文件"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存原始格式
    cookie_file = output_dir / "xhs_cookies.txt"
    cookie_file.write_text(cookie_str)
    print(f"✅ Cookies已保存到: {cookie_file}")
    
    # 保存JSON格式（备份）
    json_file = output_dir / "xhs_cookies.json"
    json_file.write_text(json.dumps(dict(c.split("=", 1) for c in cookie_str.split("; ") if "=" in c), indent=2, ensure_ascii=False))
    print(f"✅ JSON格式已保存到: {json_file}")
    
    return str(cookie_file)


async def main():
    """主函数"""
    print("=" * 50)
    print("🐱 小红书 Cookies 获取工具 (Playwright版)")
    print("=" * 50)
    print()
    
    try:
        # 获取cookies
        cookie_str, cookie_dict = await get_xhs_cookies()
        
        print(f"\n📊 获取到 {len(cookie_dict)} 个cookies")
        print()
        
        # 显示关键cookies
        key_cookies = ['web_session', 'a1', 'webid', 'xhs_tracker_id']
        print("关键cookies:")
        for key in key_cookies:
            if key in cookie_dict:
                value = cookie_dict[key]
                display = value[:15] + "..." if len(value) > 15 else value
                print(f"  ✅ {key}: {display}")
            else:
                print(f"  ❌ {key}: 未找到")
        
        print()
        
        # 保存到文件
        saved_path = await save_cookies(cookie_str)
        
        print()
        print("=" * 50)
        print("🎉 完成！")
        print("=" * 50)
        print()
        print("下一步操作:")
        print(f"  1. Cookies已保存到: {saved_path}")
        print("  2. 上传到服务器:")
        print("     scp data/xhs_cookies.txt root@43.129.244.154:/opt/xhs-automation/data/")
        print()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
