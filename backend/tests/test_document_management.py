import requests

def test_document_management():
    """测试文档管理功能"""
    # 测试获取文档列表
    print("=== 测试获取文档列表 ===")
    response = requests.get('http://localhost:8000/documents')
    print(f"文档列表响应: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 获取文档ID
    documents = response.json().get('documents', [])
    if documents:
        doc_id = documents[0]['id']
        doc_filename = documents[0]['filename']
        
        # 测试删除文档
        print(f"\n=== 测试删除文档: {doc_filename} ===")
        delete_response = requests.delete(f'http://localhost:8000/documents/{doc_id}')
        print(f"删除响应: {delete_response.status_code}")
        print(f"响应内容: {delete_response.json()}")
        
        # 再次获取文档列表，确认文档已删除
        print("\n=== 再次获取文档列表 ===")
        response = requests.get('http://localhost:8000/documents')
        print(f"文档列表响应: {response.status_code}")
        print(f"响应内容: {response.json()}")
    else:
        print("\n没有文档可以删除")

if __name__ == "__main__":
    test_document_management()