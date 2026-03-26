import requests

# 测试模型状态接口
try:
    response = requests.get('http://localhost:8000/api/model/status')
    print('Status Code:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', str(e))
