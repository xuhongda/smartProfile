import requests
import os

def test_file_upload():
    """测试文件上传功能"""
    print("=== 测试文件上传功能 ===")
    
    # 创建一个测试文件
    test_content = "这是一个测试文件，用于测试文件上传和搜索功能。包含关键词：测试、上传、搜索"
    test_file_path = "test_upload.txt"
    
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        # 上传文件
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f)}
            response = requests.post('http://localhost:8000/upload', files=files)
        
        print(f"上传响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        if response.status_code == 200 and response.json().get('success'):
            print("文件上传成功！")
        else:
            print("文件上传失败！")
    finally:
        # 清理测试文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_search():
    """测试搜索功能"""
    print("\n=== 测试搜索功能 ===")
    
    # 测试搜索关键词
    keywords = ["测试", "上传", "搜索"]
    
    for keyword in keywords:
        print(f"\n搜索关键词: {keyword}")
        response = requests.get(f'http://localhost:8000/search?q={keyword}')
        print(f"搜索响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        if response.status_code == 200 and response.json().get('success'):
            results = response.json().get('results', [])
            print(f"找到 {len(results)} 个结果")
        else:
            print("搜索失败！")

if __name__ == "__main__":
    test_file_upload()
    test_search()
