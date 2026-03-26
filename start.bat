@echo off

echo 启动SmartProfile应用...
echo =======================
echo 1. 启动后端服务
echo 2. 启动前端服务
echo 3. 退出
echo =======================

set /p choice=请选择操作: 

if "%choice%"=="1" (
    echo 正在启动后端服务...
    start "SmartProfile后端" cmd /c "cd backend && start.bat"
    echo 后端服务已启动，请在浏览器中访问 http://localhost:8000
    pause
    goto end
)

if "%choice%"=="2" (
    echo 正在启动前端服务...
    start "SmartProfile前端" cmd /c "cd frontend && start.bat"
    echo 前端服务已启动，请在浏览器中访问 http://localhost:5173
    pause
    goto end
)

if "%choice%"=="3" (
    echo 退出...
    goto end
)

echo 无效的选择，请重新运行脚本
pause

:end