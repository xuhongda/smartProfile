import requests
import json

# 测试搜索API
def test_search():
    print("测试搜索API...")
    url = "http://localhost:8000/search?q=测试"
    response = requests.get(url)
    print(f"搜索API响应状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"搜索结果成功: {result['success']}")
        print(f"搜索结果数量: {result['total']}")
        if result['results']:
            print("\n搜索结果详情:")
            for i, item in enumerate(result['results']):
                print(f"\n结果 {i+1}:")
                print(f"  ID: {item.get('id')}")
                print(f"  文件名: {item.get('filename')}")
                print(f"  文件类型: {item.get('file_type')}")
                print(f"  文件路径: {item.get('file_path')}")
                print(f"  创建时间: {item.get('created_at')}")
            return result['results']
    return []

# 测试预览API
def test_preview(doc_id, filename):
    print(f"\n测试预览API (ID: {doc_id}, 文件名: {filename})...")
    url = f"http://localhost:8000/preview/{doc_id}"
    response = requests.get(url)
    print(f"预览API响应状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"预览结果成功: {result['success']}")
        print(f"预览文件名: {result.get('filename')}")
        print(f"预览文件类型: {result.get('file_type')}")
        print(f"预览内容类型: {result.get('content_type')}")
        if 'content' in result:
            content = result['content']
            if isinstance(content, str):
                print(f"预览内容长度: {len(content)}")
                print(f"预览内容前100字符: {content[:100]}...")
            else:
                print(f"预览内容类型: {type(content)}")
                if isinstance(content, list):
                    print(f"预览内容列表长度: {len(content)}")
                    if content:
                        print(f"第一个元素: {content[0]}")
    else:
        print(f"预览API失败: {response.text}")

# 主函数
if __name__ == "__main__":
    print("开始测试搜索和预览功能...")
    results = test_search()
    if results:
        # 测试第一个结果的预览
        first_result = results[0]
        test_preview(first_result['id'], first_result['filename'])
        
        # 如果有多个结果，测试第二个结果的预览
        if len(results) > 1:
            second_result = results[1]
            test_preview(second_result['id'], second_result['filename'])
    print("测试完成")