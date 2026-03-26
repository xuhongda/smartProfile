import requests
import io

def test_error_handling():
    """测试错误处理功能"""
    # 测试上传不支持的文件类型
    print("=== 测试上传不支持的文件类型 ===")
    url = 'http://localhost:8000/upload'
    
    # 创建一个不支持的文件类型（.jpg）
    files = {'file': ('test.jpg', io.BytesIO(b'fake image data'), 'image/jpeg')}
    response = requests.post(url, files=files)
    print(f"上传不支持文件类型响应: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 测试搜索空关键词
    print("\n=== 测试搜索空关键词 ===")
    response = requests.get('http://localhost:8000/search?q=')
    print(f"搜索空关键词响应: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 测试删除不存在的文档
    print("\n=== 测试删除不存在的文档 ===")
    response = requests.delete('http://localhost:8000/documents/999')
    print(f"删除不存在文档响应: {response.status_code}")
    print(f"响应内容: {response.json()}")

if __name__ == "__main__":
    test_error_handling()