from playwright.sync_api import sync_playwright
from pathlib import Path
import time

print('=' * 50)
print('🐱 小红书 Cookies 获取工具')
print('=' * 50)
print()

data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    print('🚀 启动浏览器...')
    
    browser = p.chromium.launch(headless=False, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1280, 'height': 720})
    page = context.new_page()
    
    print('📱 打开小红书登录页面...')
    page.goto('https://www.xiaohongshu.com/', timeout=60000)
    
    print()
    print('⏳ 请在浏览器中完成登录：')
    print('   1. 点击右上角【登录】按钮')
    print('   2. 选择【手机号登录】')
    print('   3. 输入手机号：13810119101')
    print('   4. 点击【获取验证码】')
    print('   5. 查看手机短信，输入验证码')
    print('   6. 登录成功后，确保看到右上角显示头像')
    print()
    print('✅ 登录完成后，')
    print('   【按回车键】保存cookies并退出...')
    input()
    
    print()
    print('💾 正在保存cookies...')
    
    cookies = context.cookies('https://www.xiaohongshu.com/')
    cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
    
    with open('data/xhs_cookies.txt', 'w') as f:
        f.write(cookie_str)
    
    browser.close()
    
    print()
    print('=' * 50)
    print('🎉 完成！')
    print('=' * 50)
    print(f'📁 保存到: data/xhs_cookies.txt')
    print(f'📊 共 {len(cookies)} 个cookies')
    print()
    print('下一步：上传到服务器')
    print(' scp data/xhs_cookies.txt root@43.129.244.154:/opt/xhs-automation/data/')
