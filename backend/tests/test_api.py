import requests

def test_health_check():
    """测试健康检查接口"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"健康检查接口响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        return True
    except Exception as e:
        print(f"健康检查接口测试失败: {str(e)}")
        return False

def test_db_check():
    """测试数据库连接检查接口"""
    try:
        response = requests.get('http://localhost:8000/db-check', timeout=5)
        print(f"数据库检查接口响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        return True
    except Exception as e:
        print(f"数据库检查接口测试失败: {str(e)}")
        return False

def test_root():
    """测试根路径接口"""
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"根路径接口响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        return True
    except Exception as e:
        print(f"根路径接口测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试后端API接口...")
    print("=" * 50)
    
    test_root()
    print("-" * 50)
    
    test_health_check()
    print("-" * 50)
    
    test_db_check()
    print("=" * 50)
    print("测试完成")