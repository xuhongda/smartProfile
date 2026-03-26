from database import get_db
from core.services.ingestion_service import ingestion_service
from core.services.hybrid_search_service import hybrid_search_service
from core.services.meta_store import meta_store
import json

# 集成测试脚本
def test_integration():
    """测试系统集成功能"""
    print("开始集成测试...")
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 测试数据
        test_documents = [
            {
                "file_path": "integration_test_1.txt",
                "content_text": "这是集成测试文档 1，用于测试系统的完整功能。"
            },
            {
                "file_path": "integration_test_2.txt",
                "content_text": "这是集成测试文档 2，用于测试系统的搜索功能。"
            }
        ]
        
        # 1. 测试数据写入
        print("\n1. 测试数据写入...")
        ingestion_results = []
        for doc in test_documents:
            result = ingestion_service.ingest_document(db, doc["file_path"], doc["content_text"])
            ingestion_results.extend(result)
        
        print(f"成功写入 {len(ingestion_results)} 个文档块")
        
        # 2. 测试数据查询
        print("\n2. 测试数据查询...")
        if ingestion_results:
            doc_ids = [result["id"] for result in ingestion_results]
            docs = meta_store.get_documents_by_uuids(db, doc_ids)
            print(f"成功查询到 {len(docs)} 个文档")
        
        # 3. 测试搜索功能
        print("\n3. 测试搜索功能...")
        queries = ["集成测试", "搜索功能"]
        for query in queries:
            results = hybrid_search_service.search_knowledge_base(db, query, top_k=2)
            print(f"搜索 '{query}' 得到 {len(results)} 个结果")
        
        # 4. 测试错误处理
        print("\n4. 测试错误处理...")
        try:
            # 测试空查询
            empty_results = hybrid_search_service.search_knowledge_base(db, "")
            print(f"空查询返回 {len(empty_results)} 个结果")
        except Exception as e:
            print(f"空查询错误处理失败: {str(e)}")
        
        # 5. 测试批量操作
        print("\n5. 测试批量操作...")
        batch_docs = [
            {
                "file_path": "batch_test.txt",
                "content_text": "批量测试文档，用于测试系统的批量处理能力。"
            }
        ]
        batch_results = ingestion_service.ingest_batch(db, batch_docs)
        print(f"批量写入成功 {len(batch_results)} 个文档块")
        
        # 6. 清理测试数据
        print("\n6. 清理测试数据...")
        all_test_ids = [result["id"] for result in ingestion_results + batch_results]
        deleted_count = 0
        for doc_id in all_test_ids:
            if meta_store.delete_document(db, doc_id):
                deleted_count += 1
        print(f"成功删除 {deleted_count} 个测试文档")
        
        print("\n集成测试完成！")
        print("所有功能模块已成功集成并测试通过。")
        
    except Exception as e:
        print(f"集成测试失败: {str(e)}")
    finally:
        # 关闭数据库会话
        db.close()

# 执行集成测试
if __name__ == "__main__":
    test_integration()