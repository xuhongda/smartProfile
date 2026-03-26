from core.services.meta_store import meta_store
from database import get_db
import uuid

# 测试初始化
print("测试 MetaStore 初始化...")

# 获取数据库会话
db = next(get_db())

# 测试获取文档数量
print("\n测试获取文档数量...")
count = meta_store.get_document_count(db)
print(f"文档数量: {count}")

# 测试创建文档
print("\n测试创建文档...")
test_filename = "test_document.txt"
test_file_type = "txt"
test_content = "这是一个测试文档，用于验证 MetaStore 功能"
test_uuid = str(uuid.uuid4())
try:
    document = meta_store.create_document(db, test_filename, test_file_type, test_content, test_uuid)
    print(f"成功创建文档: {document.uuid}")
    print(f"文档信息: filename={document.filename}, file_type={document.file_type}")
except Exception as e:
    print(f"创建文档失败: {str(e)}")

# 测试根据 UUID 获取文档
print("\n测试根据 UUID 获取文档...")
retrieved_doc = meta_store.get_document_by_uuid(db, test_uuid)
if retrieved_doc:
    print(f"成功获取文档: {retrieved_doc.uuid}")
    print(f"文档内容: {retrieved_doc.content[:50]}...")
else:
    print("获取文档失败")

# 测试批量获取文档
print("\n测试批量获取文档...")
# 创建另一个文档
another_uuid = str(uuid.uuid4())
another_doc = meta_store.create_document(db, "another_test.txt", "txt", "另一个测试文档", another_uuid)
doc_uuids = [test_uuid, another_uuid]
batch_docs = meta_store.get_documents_by_uuids(db, doc_uuids)
print(f"批量获取文档数量: {len(batch_docs)}")
for doc in batch_docs:
    print(f"  - {doc.uuid}: {doc.filename}")

# 测试获取所有文档
print("\n测试获取所有文档...")
all_docs = meta_store.get_all_documents(db, limit=10)
print(f"获取到的文档数量: {len(all_docs)}")
for doc in all_docs[:3]:  # 只显示前3个
    print(f"  - {doc.uuid}: {doc.filename}")

# 测试删除文档
print("\n测试删除文档...")
delete_success = meta_store.delete_document(db, test_uuid)
if delete_success:
    print(f"成功删除文档: {test_uuid}")
else:
    print("删除文档失败")

# 验证删除
print("\n验证删除...")
deleted_doc = meta_store.get_document_by_uuid(db, test_uuid)
if not deleted_doc:
    print(f"文档已成功删除: {test_uuid}")
else:
    print("文档删除失败")

# 清理测试数据
meta_store.delete_document(db, another_uuid)

# 关闭数据库会话
db.close()

print("\nMetaStore 测试完成")