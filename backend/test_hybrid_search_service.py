from core.services.hybrid_search_service import hybrid_search_service
from core.services.ingestion_service import ingestion_service
from database import get_db

# 测试初始化
print("测试 HybridSearchService 初始化...")

# 获取数据库会话
db = next(get_db())

# 先写入一些测试数据
print("\n写入测试数据...")
test_docs = [
    {
        "file_path": "physics_notes.txt",
        "content_text": "物理学是研究物质运动最一般规律和物质基本结构的学科。它包括力学、热学、电磁学、光学、原子物理学等分支。"
    },
    {
        "file_path": "math_notes.txt",
        "content_text": "数学是研究数量、结构、变化以及空间等概念的学科。它包括代数、几何、微积分、概率论等分支。"
    },
    {
        "file_path": "history_notes.txt",
        "content_text": "历史是研究人类社会过去发生的事件和活动的学科。它包括古代史、近代史、现代史等时期的研究。"
    }
]

ingestion_results = []
for doc in test_docs:
    result = ingestion_service.ingest_document(db, doc["file_path"], doc["content_text"])
    ingestion_results.extend(result)

print(f"成功写入 {len(ingestion_results)} 个测试文档")

# 测试搜索
print("\n测试搜索...")
queries = [
    "物理学科",
    "数学知识",
    "历史事件"
]

for query in queries:
    print(f"\n搜索: {query}")
    results = hybrid_search_service.search_knowledge_base(db, query, top_k=3)
    print(f"搜索结果数量: {len(results)}")
    for i, result in enumerate(results):
        print(f"  {i+1}. 分数: {result['score']:.4f}, 文件名: {result['filename']}")
        print(f"     内容: {result['text'][:100]}...")

# 测试带过滤条件的搜索
print("\n测试带过滤条件的搜索...")
filtered_results = hybrid_search_service.search_with_filter(db, "学科", file_type="txt", top_k=3)
print(f"过滤后的搜索结果数量: {len(filtered_results)}")
for i, result in enumerate(filtered_results):
    print(f"  {i+1}. 分数: {result['score']:.4f}, 文件名: {result['filename']}")

# 清理测试数据
print("\n清理测试数据...")
for result in ingestion_results:
    doc_id = result["id"]
    # 这里应该同时删除 ChromaDB 中的数据，但由于模型加载失败，我们只删除 SQLite 中的数据
    # vector_store.delete_document(doc_id)

# 关闭数据库会话
db.close()

print("\nHybridSearchService 测试完成")