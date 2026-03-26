import requests

# 测试其他关键词
keywords = ['数学', '英语', '政治', '历史', '地理', '生物']

for keyword in keywords:
    search_url = 'http://localhost:8000/search'
    params = {'q': keyword}
    search_response = requests.get(search_url, params=params)
    result = search_response.json()
    print(f'搜索关键词: "{keyword}"')
    print(f'结果数量: {result["total"]}')
    if result["total"] > 0:
        print(f'第一个结果: {result["results"][0]["filename"]}')
    print('---')
