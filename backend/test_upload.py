import requests
import os

# 测试文件上传
def test_upload():
    url = 'http://localhost:8001/upload'
    file_path = 'test_upload.txt'
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    print('上传响应:', response.status_code)
    print('响应内容:', response.json())

if __name__ == '__main__':
    test_upload()
