import requests
import os

# 测试模型上传功能
def test_upload_model():
    # 后端API地址
    url = 'http://127.0.0.1:8000/api/model/upload'
    
    # 创建一个测试文件
    test_file_path = 'test_model.txt'
    with open(test_file_path, 'w') as f:
        f.write('This is a test model file')
    
    # 准备文件数据
    files = {'model': open(test_file_path, 'rb')}
    
    # 发送请求
    response = requests.post(url, files=files)
    
    # 打印响应
    print('Response status code:', response.status_code)
    print('Response content:', response.json())
    
    # 清理测试文件
    os.remove(test_file_path)

# 测试获取模型列表功能
def test_get_models():
    # 后端API地址
    url = 'http://127.0.0.1:8000/api/model/list'
    
    # 发送请求
    response = requests.get(url)
    
    # 打印响应
    print('\nGet models response:')
    print('Response status code:', response.status_code)
    print('Response content:', response.json())

if __name__ == '__main__':
    print('Testing model upload...')
    test_upload_model()
    print('\nTesting get models...')
    test_get_models()
