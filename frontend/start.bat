@echo off

REM 切换到脚本所在目录
cd /d "%~dp0"

echo 启动SmartProfile前端服务...
echo ================================

REM 检查npm是否安装
echo 检查npm是否安装...
npm --version
if %errorlevel% neq 0 (
    echo 错误: npm未安装或未添加到环境变量
    echo 请先安装Node.js
    pause
    exit /b 1
)

REM 检查是否在正确的目录
echo 检查是否在正确的目录...
if not exist "package.json" (
    echo 错误: 请在frontend目录下运行此脚本
    pause
    exit /b 1
)

REM 检查依赖是否已安装
echo 检查依赖是否已安装...
if not exist "node_modules" (
    echo 依赖未安装，正在安装...
    npm install
    if %errorlevel% neq 0 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动前端服务
echo 正在启动Vite开发服务器...
echo 前端服务将在 http://localhost:5173/ 启动
npm run dev

pause