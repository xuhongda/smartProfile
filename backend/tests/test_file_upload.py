import requests
import os

def test_file_upload():
    """测试文件上传功能"""
    url = 'http://localhost:8000/upload'
    
    # 测试文本文件上传
    test_file_path = os.path.join(os.path.dirname(__file__), '..', 'test_upload.txt')
    with open(test_file_path, 'rb') as f:
        files = {'file': ('test_upload.txt', f, 'text/plain')}
        response = requests.post(url, files=files)
        
    print(f"文本文件上传响应: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 测试上传后是否能在文档列表中看到
    response = requests.get('http://localhost:8000/documents')
    print(f"\n文档列表响应: {response.status_code}")
    print(f"文档列表: {response.json()}")

if __name__ == "__main__":
    test_file_upload()