from core.services.vector_store import vector_store
import uuid

# 测试初始化
print("测试 VectorStore 初始化...")
stats = vector_store.get_collection_stats()
print(f"集合统计信息: {stats}")

# 测试生成向量
print("\n测试生成向量...")
test_text = "这是一个测试文本，用于验证向量生成功能"
embedding = vector_store.generate_embedding(test_text)
if embedding is not None:
    print(f"成功生成向量，维度: {len(embedding)}")
else:
    print("生成向量失败")

# 测试添加文档
print("\n测试添加文档...")
doc_id = str(uuid.uuid4())
metadata = {"filename": "test_document.txt", "file_type": "txt"}
success = vector_store.add_document(doc_id, test_text, metadata)
if success:
    print(f"成功添加文档: {doc_id}")
else:
    print("添加文档失败")

# 测试查询
print("\n测试查询...")
query_text = "测试文本"
results = vector_store.query(query_text, top_k=3)
print(f"查询结果: {results}")

# 测试删除文档
print("\n测试删除文档...")
delete_success = vector_store.delete_document(doc_id)
if delete_success:
    print(f"成功删除文档: {doc_id}")
else:
    print("删除文档失败")

# 再次查询验证删除
print("\n验证删除...")
results_after_delete = vector_store.query(query_text, top_k=3)
print(f"删除后的查询结果: {results_after_delete}")

print("\nVectorStore 测试完成")