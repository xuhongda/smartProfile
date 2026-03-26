import requests

# 获取所有文档
doc_url = 'http://localhost:8000/documents'
doc_response = requests.get(doc_url)
documents = doc_response.json()

print('文档接口响应:')
print(documents)
print()
print('文档字段:')
if 'documents' in documents:
    for i, doc in enumerate(documents['documents']):
        print(f'文档 {i+1} 字段: {list(doc.keys())}')
