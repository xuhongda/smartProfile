@echo off

REM 切换到脚本所在目录
cd /d "%~dp0"

echo 启动SmartProfile后端服务...
echo ================================

REM 检查Python是否安装
echo 检查Python是否安装...
python --version
if %errorlevel% neq 0 (
    echo 错误: Python未安装或未添加到环境变量
    pause
    exit /b 1
)

REM 检查是否在正确的目录
echo 检查是否在正确的目录...
if not exist "main.py" (
    echo 错误: 请在backend目录下运行此脚本
    pause
    exit /b 1
)

REM 启动后端服务
echo 正在启动FastAPI服务...
echo 后端服务将在 http://localhost:8000 启动
python -m uvicorn main:app --reload

pause