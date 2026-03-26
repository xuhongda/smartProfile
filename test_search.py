import requests

# 测试不同关键词
keywords = ['搜索', '修复', '效果', '数据1', '表格']

for keyword in keywords:
    search_url = 'http://localhost:8000/search'
    params = {'q': keyword}
    search_response = requests.get(search_url, params=params)
    result = search_response.json()
    print(f'搜索关键词: "{keyword}"')
    print(f'结果数量: {result["total"]}')
    print('---')
