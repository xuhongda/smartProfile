import sqlite3

# 连接数据库
conn = sqlite3.connect('backend/data/unstructured_data.db')
cursor = conn.cursor()

# 查询所有文档
print('数据库中的文档:')
cursor.execute("SELECT id, filename, file_type, content FROM documents")
documents = cursor.fetchall()

for doc in documents:
    doc_id, filename, file_type, content = doc
    print(f'--- 文件: {filename} ---')
    print(f'文件类型: {file_type}')
    print(f'内容前100字符: {content[:100]}...')
    # 检查是否包含"物理"
    if '物理' in content:
        print('✓ 内容中包含"物理"')
        # 显示包含"物理"的上下文
        start = max(0, content.find('物理') - 20)
        end = min(len(content), content.find('物理') + 20)
        print(f'上下文: {content[start:end]}')
    else:
        print('✗ 内容中不包含"物理"')
    print()

# 检查 FTS 表
print('FTS 表内容:')
cursor.execute("SELECT rowid, content FROM documents_fts")
fts_rows = cursor.fetchall()
for row in fts_rows:
    rowid, content = row
    print(f'Row ID: {rowid}')
    print(f'FTS 内容前100字符: {content[:100]}...')
    if '物理' in content:
        print('✓ FTS 内容中包含"物理"')
    else:
        print('✗ FTS 内容中不包含"物理"')
    print()

# 测试 FTS 搜索
print('测试 FTS 搜索:')
cursor.execute("SELECT rowid FROM documents_fts WHERE documents_fts MATCH ?", ('物理',))
results = cursor.fetchall()
print(f'FTS 搜索 "物理" 结果数量: {len(results)}')
for row in results:
    print(f'匹配的 Row ID: {row[0]}')

conn.close()
