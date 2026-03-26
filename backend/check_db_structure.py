#!/usr/bin/env python3
"""检查数据库表结构"""

import sqlite3

# 连接到数据库
conn = sqlite3.connect('data/unstructured_data.db')
cursor = conn.cursor()

# 检查documents表结构
print("检查documents表结构:")
cursor.execute("PRAGMA table_info(documents)")
columns = cursor.fetchall()
for column in columns:
    print(f"ID: {column[0]}, 名称: {column[1]}, 类型: {column[2]}, 不为空: {column[3]}, 默认值: {column[4]}, 主键: {column[5]}")

# 检查documents_fts表结构
print("\n检查documents_fts表结构:")
try:
    cursor.execute("PRAGMA table_info(documents_fts)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"ID: {column[0]}, 名称: {column[1]}, 类型: {column[2]}, 不为空: {column[3]}, 默认值: {column[4]}, 主键: {column[5]}")
except sqlite3.OperationalError as e:
    print(f"documents_fts表不存在: {e}")

# 关闭连接
conn.close()
