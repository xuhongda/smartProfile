from core.services.ingestion_service import ingestion_service
from core.services.meta_store import meta_store
from database import get_db
import os

# 测试初始化
print("测试 IngestionService 初始化...")

# 获取数据库会话
db = next(get_db())

# 测试写入单个文档
print("\n测试写入单个文档...")
test_file_path = "test_ingestion.txt"
test_content = "这是一个测试文档，用于验证数据写入服务的功能。" * 10  # 生成较长的文本以测试切片

results = ingestion_service.ingest_document(db, test_file_path, test_content)
print(f"写入结果: {results}")
print(f"成功写入 {len(results)} 个文档块")

# 验证数据是否写入 SQLite
print("\n验证数据写入 SQLite...")
if results:
    doc_ids = [result["id"] for result in results]
    docs = meta_store.get_documents_by_uuids(db, doc_ids)
    print(f"从 SQLite 中获取到 {len(docs)} 个文档")
    for doc in docs:
        print(f"  - ID: {doc.uuid}, 文件名: {doc.filename}, 内容长度: {len(doc.content)}")

# 测试批量写入
print("\n测试批量写入...")
batch_docs = [
    {
        "file_path": "batch_test1.txt",
        "content_text": "批量测试文档 1，用于验证批量写入功能。" * 5
    },
    {
        "file_path": "batch_test2.txt",
        "content_text": "批量测试文档 2，用于验证批量写入功能。" * 5
    }
]

batch_results = ingestion_service.ingest_batch(db, batch_docs)
print(f"批量写入结果: {len(batch_results)} 个文档块")

# 清理测试数据
print("\n清理测试数据...")
all_test_ids = [result["id"] for result in results + batch_results]
for doc_id in all_test_ids:
    meta_store.delete_document(db, doc_id)

# 关闭数据库会话
db.close()

print("\nIngestionService 测试完成")