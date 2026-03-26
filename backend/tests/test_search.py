import requests

def test_search():
    """测试搜索功能"""
    # 测试搜索关键词
    keywords = ['测试', '上传', '文件']
    
    for keyword in keywords:
        print(f"\n=== 搜索关键词: {keyword} ===")
        response = requests.get(f'http://localhost:8000/search?q={keyword}')
        print(f"搜索响应: {response.status_code}")
        print(f"响应内容: {response.json()}")

if __name__ == "__main__":
    test_search()