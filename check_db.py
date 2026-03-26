import sqlite3

# 连接到数据库
conn = sqlite3.connect('backend/data/unstructured_data.db')
cursor = conn.cursor()

# 检查文档表结构
print("文档表结构:")
cursor.execute("PRAGMA table_info(documents)")
columns = cursor.fetchall()
for column in columns:
    print(column)

# 检查文档表内容
print("\n文档表内容:")
cursor.execute("SELECT id, filename, file_type, indexed FROM documents")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(row)
else:
    print("文档表为空")

# 关闭连接
conn.close()