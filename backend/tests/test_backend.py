import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试数据库连接
print("测试数据库连接...")
try:
    from database import init_db, get_db, Document
    print("✓ 数据库模块导入成功")
    
    # 初始化数据库
    init_db()
    print("✓ 数据库初始化成功")
    
    # 测试获取数据库会话
    db = next(get_db())
    print("✓ 数据库会话获取成功")
    
    # 测试Document模型
    print(f"✓ Document模型导入成功，表名: {Document.__tablename__}")
    
    # 测试文件解析库
    print("\n测试文件解析库...")
    import pandas
    print("✓ pandas导入成功")
    
    import openpyxl
    print("✓ openpyxl导入成功")
    
    import docx
    print("✓ docx导入成功")
    
    import chardet
    print("✓ chardet导入成功")
    
    # 测试FastAPI应用
    print("\n测试FastAPI应用...")
    from main import app
    print("✓ FastAPI应用导入成功")
    print(f"✓ 应用标题: {app.title}")
    print(f"✓ 应用版本: {app.version}")
    
    print("\n所有核心依赖测试通过！")
except Exception as e:
    print(f"✗ 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
