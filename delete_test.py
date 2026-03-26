import requests

# 测试删除模型功能
def test_delete_model():
    # 后端API地址
    url = 'http://127.0.0.1:8000/api/model/test_model.txt'
    
    # 发送请求
    response = requests.delete(url)
    
    # 打印响应
    print('Response status code:', response.status_code)
    print('Response content:', response.json())

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
    print('Testing delete model...')
    test_delete_model()
    print('\nTesting get models...')
    test_get_models()
