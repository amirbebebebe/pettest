#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书 Cookies 管理工具
用于加载和验证小红书登录状态
"""

import os
import json
from pathlib import Path


class XhsCookies:
    """小红书cookies管理器"""
    
    COOKIES_FILE = Path(__file__).parent.parent / "data" / "xhs_cookies.txt"
    ENV_FILE = Path(__file__).parent.parent / ".env"
    
    @classmethod
    def load(cls) -> dict:
        """加载cookies"""
        cookies = {}
        
        # 方式1：从文件加载
        if cls.COOKIES_FILE.exists():
            content = cls.COOKIES_FILE.read_text().strip()
            if content:
                for item in content.split(";"):
                    item = item.strip()
                    if "=" in item:
                        key, value = item.split("=", 1)
                        cookies[key.strip()] = value.strip()
                return cookies
        
        # 方式2：从环境变量加载
        env_cookie = os.getenv("XIAOHONGSHU_COOKIE", "")
        if env_cookie:
            for item in env_cookie.split(";"):
                item = item.strip()
                if "=" in item:
                    key, value = item.split("=", 1)
                    cookies[key.strip()] = value.strip()
        
        return cookies
    
    @classmethod
    def save_to_env(cls, cookies_str: str):
        """保存cookies到环境变量文件"""
        content = ""
        if cls.ENV_FILE.exists():
            content = cls.ENV_FILE.read_text()
        
        # 更新或添加cookie行
        lines = []
        found = False
        for line in content.split("\n"):
            if line.startswith("XIAOHONGSHU_COOKIE="):
                lines.append(f"XIAOHONGSHU_COOKIE={cookies_str}")
                found = True
            else:
                lines.append(line)
        
        if not found:
            lines.append(f"XIAOHONGSHU_COOKIE={cookies_str}")
        
        cls.ENV_FILE.write_text("\n".join(lines))
        print(f"✅ Cookies已保存到 {cls.ENV_FILE}")
    
    @classmethod
    def validate(cls) -> bool:
        """验证cookies是否有效"""
        cookies = cls.load()
        required_keys = ["web_session", "a1"]
        return all(key in cookies for key in required_keys)
    
    @classmethod
    def get_header(cls) -> str:
        """获取请求头用的cookie字符串"""
        cookies = cls.load()
        return "; ".join([f"{k}={v}" for k, v in cookies.items()])
    
    @classmethod
    def save_from_file(cls, file_path: str = None):
        """从文件保存cookies到环境变量"""
        if file_path is None:
            file_path = cls.COOKIES_FILE
        
        path = Path(file_path)
        if not path.exists():
            print(f"❌ 文件不存在: {path}")
            return False
        
        cookies_str = path.read_text().strip()
        cls.save_to_env(cookies_str)
        return True


def main():
    """主函数 - 用于命令行测试"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "load":
            cookies = XhsCookies.load()
            print(f"已加载 {len(cookies)} 个cookies")
            for k, v in cookies.items():
                print(f"  {k}: {v[:20]}..." if len(v) > 20 else f"  {k}: {v}")
        
        elif command == "validate":
            if XhsCookies.validate():
                print("✅ Cookies有效")
            else:
                print("❌ Cookies无效或缺失必要字段")
        
        elif command == "save":
            XhsCookies.save_from_file()
            print("✅ 已保存到环境变量")
        
        elif command == "header":
            print(XhsCookies.get_header())
        
        else:
            print("未知命令: load, validate, save, header")
    
    else:
        # 默认显示状态
        cookies = XhsCookies.load()
        print(f"📱 小红书Cookies状态")
        print(f"  文件: {XhsCookies.COOKIES_FILE}")
        print(f"  环境: {'✅' if os.getenv('XIAOHONGSHU_COOKIE') else '❌'}")
        print(f"  有效: {'✅' if XhsCookies.validate() else '❌'}")
        print(f"  数量: {len(cookies)} 个cookies")


if __name__ == "__main__":
    main()
