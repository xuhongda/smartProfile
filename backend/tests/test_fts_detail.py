import sqlite3

# 连接到数据库
conn = sqlite3.connect('data/unstructured_data.db')
cursor = conn.cursor()

print("=== 检查 documents_fts 表内容 ===")
# 查看 documents_fts 表的前几行
cursor.execute("SELECT rowid, filename, content FROM documents_fts LIMIT 3")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Filename: {row[1]}")
    print(f"Content preview: {row[2][:100]}...")
    print()

print("=== 测试 FTS5 搜索 ===")
# 测试不同的搜索语法
keywords = ['物理', '成绩', '教学', '声音', '压强', '浮力']

for keyword in keywords:
    print(f"\n搜索关键词: '{keyword}'")
    
    # 测试基本搜索
    cursor.execute(
        "SELECT rowid, filename FROM documents_fts WHERE documents_fts MATCH ?",
        (keyword,)
    )
    results = cursor.fetchall()
    print(f"基本搜索结果: {len(results)} 个")
    for result in results:
        print(f"  - {result[1]}")
    
    # 测试内容字段搜索
    cursor.execute(
        "SELECT rowid, filename FROM documents_fts WHERE content MATCH ?",
        (keyword,)
    )
    results = cursor.fetchall()
    print(f"内容字段搜索结果: {len(results)} 个")
    for result in results:
        print(f"  - {result[1]}")
    
    # 测试通配符搜索
    cursor.execute(
        "SELECT rowid, filename FROM documents_fts WHERE documents_fts MATCH ?",
        (f"{keyword}*",)
    )
    results = cursor.fetchall()
    print(f"通配符搜索结果: {len(results)} 个")
    for result in results:
        print(f"  - {result[1]}")

print("\n=== 测试 SQL 直接搜索 ===")
# 测试直接SQL搜索
cursor.execute("SELECT id, filename FROM documents WHERE content LIKE '%物理%'")
results = cursor.fetchall()
print(f"LIKE搜索 '物理' 结果: {len(results)} 个")
for result in results:
    print(f"  - {result[1]}")

# 关闭连接
conn.close()
print("\n测试完成")
