import requests
import os

# 重新上传 Excel 文件
test_files = [
    'backend/tests/八17期末下.xlsx',
    'backend/tests/成绩单.xlsx'
]

for file_path in test_files:
    if os.path.exists(file_path):
        url = 'http://localhost:8000/upload'
        files = {'file': open(file_path, 'rb')}
        
        response = requests.post(url, files=files)
        print(f'上传文件: {file_path}')
        print(f'响应: {response.json()}')
        print('---')
    else:
        print(f'文件不存在: {file_path}')

# 测试搜索物理
search_url = 'http://localhost:8000/search'
params = {'q': '物理'}
search_response = requests.get(search_url, params=params)
result = search_response.json()
print('搜索关键词: "物理"')
print(f'结果数量: {result["total"]}')
print('结果详情:')
for item in result["results"]:
    print(f'  - 文件名: {item["filename"]}')
    print(f'    摘要: {item["snippet"]}')
