import sqlite3

# 连接到数据库
conn = sqlite3.connect('data/unstructured_data.db')
cursor = conn.cursor()

print("开始同步 documents 表到 documents_fts 表...")

# 清空 documents_fts 表
cursor.execute("DELETE FROM documents_fts")
print("已清空 documents_fts 表")

# 从 documents 表中获取所有数据
cursor.execute("SELECT id, content, filename, file_type FROM documents")
documents = cursor.fetchall()

print(f"找到 {len(documents)} 个文档记录")

# 将数据插入到 documents_fts 表
insert_count = 0
for doc in documents:
    doc_id, content, filename, file_type = doc
    try:
        cursor.execute(
            "INSERT INTO documents_fts(rowid, content, filename, file_type) VALUES (?, ?, ?, ?)",
            (doc_id, content, filename, file_type)
        )
        insert_count += 1
        print(f"同步文档: {filename} (ID: {doc_id})")
    except Exception as e:
        print(f"同步文档 {filename} 失败: {str(e)}")

# 提交事务
conn.commit()
print(f"数据同步完成，成功插入 {insert_count} 条记录")

# 检查 documents_fts 表中的记录数
cursor.execute("SELECT COUNT(*) FROM documents_fts")
count = cursor.fetchone()[0]
print(f"documents_fts 表中共有 {count} 条记录")

# 查看 documents_fts 表的前几行
cursor.execute("SELECT rowid, filename FROM documents_fts LIMIT 3")
rows = cursor.fetchall()
print("\ndocuments_fts 表中的记录:")
for row in rows:
    print(f"  ID: {row[0]}, Filename: {row[1]}")

# 测试 FTS5 搜索
print("\n测试 FTS5 搜索功能...")
keywords = ['物理', '成绩', '教学']

for keyword in keywords:
    # 测试基本搜索
    try:
        cursor.execute(
            "SELECT rowid, filename FROM documents_fts WHERE documents_fts MATCH ?",
            (keyword,)
        )
        results = cursor.fetchall()
        print(f"搜索关键词 '{keyword}' 找到 {len(results)} 个结果")
        for result in results:
            print(f"  - {result[1]}")
    except Exception as e:
        print(f"搜索关键词 '{keyword}' 失败: {str(e)}")

# 测试直接查询FTS5表的内容
print("\n测试直接查询FTS5表内容...")
try:
    cursor.execute("SELECT rowid, filename, content FROM documents_fts LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"ID: {row[0]}, Filename: {row[1]}")
        print(f"Content: {row[2][:50]}...")
except Exception as e:
    print(f"查询FTS5表失败: {str(e)}")

# 关闭连接
conn.close()
print("\n同步和测试完成")
