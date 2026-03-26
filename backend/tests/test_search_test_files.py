import requests

def search_files():
    """搜索上传的文件内容"""
    # 使用文件中实际包含的关键词进行搜索
    keywords = ['物理', '成绩', '教学', '声音', '压强', '浮力']
    
    for keyword in keywords:
        print(f"\n=== 搜索关键词: {keyword} ===")
        try:
            response = requests.get(f'http://localhost:8000/search?q={keyword}')
            print(f"搜索响应: {response.status_code}")
            result = response.json()
            print(f"响应内容: {result}")
            print(f"找到 {result.get('total', 0)} 个结果")
            
            # 打印搜索结果的摘要
            if result.get('results'):
                print("搜索结果摘要:")
                for i, item in enumerate(result['results']):
                    print(f"{i+1}. {item['filename']}")
                    print(f"   摘要: {item['snippet'][:100]}...")
        except Exception as e:
            print(f"搜索失败: {str(e)}")

def main():
    """主测试函数"""
    print("开始搜索上传的测试文件内容...")
    print("=" * 70)
    search_files()
    print("=" * 70)
    print("测试完成")

if __name__ == "__main__":
    main()