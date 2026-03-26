import requests
import json

# 测试后端预览接口
doc_id = 1
preview_url = f'http://localhost:8000/preview/{doc_id}'

response = requests.get(preview_url)
print('后端预览接口响应:')
print('状态码:', response.status_code)
print('响应内容:', json.dumps(response.json(), ensure_ascii=False, indent=2))

# 测试前端预览数据处理
print('\n测试前端数据处理:')
data = response.json()
if data.get('success'):
    content = data.get('content')
    print(f'文件类型: {data.get("file_type")}')
    print(f'内容类型: {data.get("content_type")}')
    print(f'内容长度: {len(content)} 条记录')
    if content:
        print('前5条记录:')
        for i, item in enumerate(content[:5]):
            print(f'  记录 {i+1}: {json.dumps(item, ensure_ascii=False)}')
else:
    print('预览失败:', data.get('detail'))
