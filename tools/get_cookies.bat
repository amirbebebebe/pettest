@echo off
chcp 65001 >nul
echo ============================================
echo    小红书 Cookies 获取工具
echo ============================================
echo.
echo 步骤说明:
echo   1. 按 Win+R 输入: chrome https://www.xiaohongshu.com
echo   2. 登录账号: 13810119101
echo   3. 按 F12 打开开发者工具
echo   4. 按 Ctrl+Shift+P
echo   5. 输入: network cookies
echo   6. 在Console中输入: console.log(document.cookie)
echo   7. 复制所有输出内容
echo.
echo 关键cookies需要包含:
echo   - web_session
echo   - a1
echo.
echo 请将cookies保存到: data\xhs_cookies.txt
echo.
echo ============================================
pause
