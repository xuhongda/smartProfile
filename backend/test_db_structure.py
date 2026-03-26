import sqlite3

# 连接到数据库
conn = sqlite3.connect('data/unstructured_data.db')
cursor = conn.cursor()

# 检查表结构
print("检查 documents 表结构:")
cursor.execute("PRAGMA table_info(documents)")
columns = cursor.fetchall()
for col in columns:
    print(f"Column: {col[1]}, Type: {col[2]}, Nullable: {col[3]}")

# 检查是否有 uuid 字段
has_uuid = any(col[1] == 'uuid' for col in columns)
print(f"\nHas uuid column: {has_uuid}")

# 检查索引
print("\n检查索引:")
cursor.execute("PRAGMA index_list(documents)")
indexes = cursor.fetchall()
for idx in indexes:
    print(f"Index: {idx[1]}")

# 检查数据
print("\n检查数据:")
cursor.execute("SELECT id, uuid, filename FROM documents LIMIT 5")
data = cursor.fetchall()
for row in data:
    print(f"ID: {row[0]}, UUID: {row[1]}, Filename: {row[2]}")

conn.close()
print("\n数据库结构检查完成")