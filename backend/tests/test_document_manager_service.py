import sys
import os

# 添加backend目录到Python搜索路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.services import container
from database import SessionLocal

def test_document_manager_service():
    """测试文档管理服务"""
    print("=== 测试文档管理服务 ===")
    
    # 获取文档管理服务
    document_manager_service = container.resolve('document_manager_service')
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 测试创建文档
        test_filename = "test_document.txt"
        test_file_type = "txt"
        test_content = "这是一个测试文档"
        
        doc, message = document_manager_service.create_document(
            db, test_filename, test_file_type, test_content
        )
        assert doc.id is not None, "文档创建失败"
        assert doc.filename == test_filename, "文档名错误"
        assert doc.file_type == test_file_type, "文档类型错误"
        assert doc.content == test_content, "文档内容错误"
        print(f"✓ 文档创建测试通过: {message}")
        
        # 测试获取文档
        retrieved_doc = document_manager_service.get_document(db, doc.id)
        assert retrieved_doc.id == doc.id, "文档获取失败"
        assert retrieved_doc.filename == test_filename, "文档名错误"
        print("✓ 文档获取测试通过")
        
        # 测试获取文档列表
        doc_list = document_manager_service.get_documents(db)
        assert doc_list.total >= 1, "文档列表获取失败"
        assert len(doc_list.documents) >= 1, "文档列表为空"
        print(f"✓ 文档列表获取测试通过，共 {doc_list.total} 个文档")
        
        # 测试更新文档
        updated_content = "这是更新后的测试文档"
        updated_doc = document_manager_service.update_document(
            db, doc.id, updated_content, test_file_type
        )
        assert updated_doc.content == updated_content, "文档更新失败"
        print("✓ 文档更新测试通过")
        
        # 测试删除文档
        delete_result = document_manager_service.delete_document(db, doc.id)
        assert delete_result == True, "文档删除失败"
        print("✓ 文档删除测试通过")
        
        # 测试删除不存在的文档
        try:
            document_manager_service.get_document(db, doc.id)
            assert False, "应该抛出文档不存在异常"
        except ValueError as e:
            assert "文档不存在" in str(e), "异常信息错误"
        print("✓ 删除不存在文档测试通过")
        
    finally:
        db.close()
    
    print("=== 文档管理服务测试通过 ===")

if __name__ == "__main__":
    test_document_manager_service()
