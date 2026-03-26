import requests

# 获取所有文档
doc_url = 'http://localhost:8000/documents'
doc_response = requests.get(doc_url)
documents = doc_response.json()

print('所有文档:')
for doc in documents['documents']:
    print(f'--- 文件: {doc["filename"]} ---')
    print(f'文件类型: {doc["file_type"]}')
    print(f'内容长度: {doc["content_length"]}')
    print(f'内容前100字符: {doc["content"][:100]}...')
    # 检查是否包含"物理"
    if '物理' in doc["content"]:
        print('✓ 内容中包含"物理"')
    else:
        print('✗ 内容中不包含"物理"')
    print()

# 测试不同的搜索方式
print('测试不同搜索方式:')
keywords = ['物理', '物', '理', '物理']
for keyword in keywords:
    search_url = 'http://localhost:8000/search'
    params = {'q': keyword}
    search_response = requests.get(search_url, params=params)
    result = search_response.json()
    print(f'搜索 "{keyword}": {result["total"]} 个结果')
