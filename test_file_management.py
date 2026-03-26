import requests
import os
import time

# 测试文件路径
TEST_FILES = [
    {
        "path": "test_file.txt",
        "type": "text/plain"
    }
]

# 测试函数
def test_file_management():
    print("开始测试文件管理功能...")
    
    # 1. 获取初始文档列表
    print("\n1. 获取初始文档列表...")
    response = requests.get("http://localhost:8000/documents")
    print(f"文档列表API响应状态码: {response.status_code}")
    if response.status_code == 200:
        initial_docs = response.json()
        print(f"初始文档数量: {initial_docs.get('total', 0)}")
    else:
        print(f"获取文档列表失败: {response.text}")
        return
    
    # 2. 上传测试文件
    print("\n2. 上传测试文件...")
    for test_file in TEST_FILES:
        file_path = test_file["path"]
        file_type = test_file["type"]
        
        if not os.path.exists(file_path):
            # 创建测试文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("测试文件内容\n这是一个测试文件，用于验证文件管理功能。")
            print(f"创建测试文件: {file_path}")
        
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, file_type)}
            response = requests.post("http://localhost:8000/upload", files=files)
            print(f"上传文件 {file_path} 响应状态码: {response.status_code}")
            if response.status_code == 200:
                upload_result = response.json()
                print(f"上传结果: {upload_result.get('message')}")
                if upload_result.get('success'):
                    uploaded_file_id = upload_result.get('file_id')
                    print(f"上传文件ID: {uploaded_file_id}")
                else:
                    print(f"上传失败: {upload_result.get('message')}")
            else:
                print(f"上传失败: {response.text}")
    
    # 等待1秒，确保文件上传完成
    time.sleep(1)
    
    # 3. 获取更新后的文档列表
    print("\n3. 获取更新后的文档列表...")
    response = requests.get("http://localhost:8000/documents")
    print(f"文档列表API响应状态码: {response.status_code}")
    if response.status_code == 200:
        updated_docs = response.json()
        print(f"更新后文档数量: {updated_docs.get('total', 0)}")
        if updated_docs.get('documents'):
            for doc in updated_docs.get('documents'):
                print(f"  - {doc.get('filename')} (ID: {doc.get('id')}, 类型: {doc.get('file_type')})")
    else:
        print(f"获取文档列表失败: {response.text}")
    
    # 4. 测试预览功能
    print("\n4. 测试预览功能...")
    if updated_docs.get('documents'):
        for doc in updated_docs.get('documents'):
            doc_id = doc.get('id')
            filename = doc.get('filename')
            print(f"预览文档: {filename} (ID: {doc_id})")
            response = requests.get(f"http://localhost:8000/preview/{doc_id}")
            print(f"预览API响应状态码: {response.status_code}")
            if response.status_code == 200:
                preview_result = response.json()
                if preview_result.get('success'):
                    print(f"  预览成功，文件类型: {preview_result.get('file_type')}")
                    content_type = preview_result.get('content_type')
                    print(f"  内容类型: {content_type}")
                else:
                    print(f"  预览失败: {preview_result.get('message')}")
            else:
                print(f"  预览失败: {response.text}")
    
    # 5. 测试删除功能
    print("\n5. 测试删除功能...")
    if updated_docs.get('documents'):
        for doc in updated_docs.get('documents'):
            doc_id = doc.get('id')
            filename = doc.get('filename')
            print(f"删除文档: {filename} (ID: {doc_id})")
            response = requests.delete(f"http://localhost:8000/documents/{doc_id}")
            print(f"删除API响应状态码: {response.status_code}")
            if response.status_code == 200:
                delete_result = response.json()
                if delete_result.get('success'):
                    print(f"  删除成功: {delete_result.get('message')}")
                else:
                    print(f"  删除失败: {delete_result.get('message')}")
            else:
                print(f"  删除失败: {response.text}")
    
    # 等待1秒，确保文件删除完成
    time.sleep(1)
    
    # 6. 获取删除后的文档列表
    print("\n6. 获取删除后的文档列表...")
    response = requests.get("http://localhost:8000/documents")
    print(f"文档列表API响应状态码: {response.status_code}")
    if response.status_code == 200:
        final_docs = response.json()
        print(f"删除后文档数量: {final_docs.get('total', 0)}")
    else:
        print(f"获取文档列表失败: {response.text}")
    
    # 7. 清理测试文件
    print("\n7. 清理测试文件...")
    for test_file in TEST_FILES:
        file_path = test_file["path"]
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"删除测试文件: {file_path}")
    
    print("\n测试完成")

# 主函数
if __name__ == "__main__":
    test_file_management()