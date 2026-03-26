import requests
import os

# 上传 Excel 文件
test_file = 'backend/tests/八17期末下.xlsx'

if os.path.exists(test_file):
    url = 'http://localhost:8000/upload'
    files = {'file': open(test_file, 'rb')}
    
    response = requests.post(url, files=files)
    print('上传响应:', response.json())
    
    # 获取文档ID
    doc_id = response.json().get('file_id')
    if doc_id:
        # 测试预览
        preview_url = f'http://localhost:8000/preview/{doc_id}'
        preview_response = requests.get(preview_url)
        print('预览响应状态码:', preview_response.status_code)
        print('预览响应内容:', preview_response.json())
    else:
        print('上传失败，无法获取文档ID')
else:
    print('文件不存在')
