import requests
import os
import glob

def upload_file(file_path):
    """上传文件到后端服务"""
    url = 'http://localhost:8000/upload'
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(url, files=files)
            
        print(f"上传文件 {os.path.basename(file_path)} 响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"上传文件 {os.path.basename(file_path)} 失败: {str(e)}")
        return False

def search_files():
    """搜索上传的文件内容"""
    keywords = ['物理', '成绩', '教学']
    
    for keyword in keywords:
        print(f"\n=== 搜索关键词: {keyword} ===")
        try:
            response = requests.get(f'http://localhost:8000/search?q={keyword}')
            print(f"搜索响应: {response.status_code}")
            result = response.json()
            print(f"响应内容: {result}")
            print(f"找到 {result.get('total', 0)} 个结果")
        except Exception as e:
            print(f"搜索失败: {str(e)}")

def main():
    """主测试函数"""
    print("开始测试上传test文件夹中的文件...")
    print("=" * 70)
    
    # 获取test文件夹中的所有word和excel文件
    test_folder = 'test'
    word_files = glob.glob(os.path.join(test_folder, '*.docx'))
    excel_files = glob.glob(os.path.join(test_folder, '*.xlsx'))
    
    all_files = word_files + excel_files
    print(f"找到 {len(all_files)} 个测试文件: {[os.path.basename(f) for f in all_files]}")
    print("-" * 70)
    
    # 上传所有文件
    success_count = 0
    for file_path in all_files:
        if upload_file(file_path):
            success_count += 1
        print("-" * 70)
    
    print(f"上传完成，成功上传 {success_count}/{len(all_files)} 个文件")
    print("=" * 70)
    
    # 搜索文件内容
    print("开始搜索上传的文件内容...")
    print("=" * 70)
    search_files()
    print("=" * 70)
    print("测试完成")

if __name__ == "__main__":
    main()