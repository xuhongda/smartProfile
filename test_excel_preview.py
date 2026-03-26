import requests
import json

# 测试Excel预览API
def test_excel_preview():
    print("测试Excel预览API...")
    # 假设我们有一个Excel文档的ID为2
    doc_id = 2
    url = f"http://localhost:8000/preview/{doc_id}"
    response = requests.get(url)
    print(f"预览API响应状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"预览结果成功: {result['success']}")
        print(f"预览文件名: {result.get('filename')}")
        print(f"预览文件类型: {result.get('file_type')}")
        print(f"预览内容类型: {result.get('content_type')}")
