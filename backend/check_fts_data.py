import sqlite3

def check_fts_data():
    """检查FTS5表的内容"""
    conn = sqlite3.connect('data/unstructured_data.db')
    cursor = conn.cursor()
    
    # 检查documents表的内容
    print("=== documents表内容 ===")
    cursor.execute("SELECT id, filename, file_type, content FROM documents")
    documents = cursor.fetchall()
    for doc in documents:
        print(f"ID: {doc[0]}, Filename: {doc[1]}, Type: {doc[2]}")
        print(f"Content: {doc[3]}")
        print()
    
    # 检查documents_fts表的内容
    print("=== documents_fts表内容 ===")
    cursor.execute("SELECT rowid, content, filename, file_type FROM documents_fts")
    fts_docs = cursor.fetchall()
    for doc in fts_docs:
        print(f"RowID: {doc[0]}, Filename: {doc[2]}, Type: {doc[3]}")
        print(f"Content: {doc[1]}")
        print()
    
    # 测试FTS5搜索
    print("=== FTS5搜索测试 ===")
    keywords = ['测试', '上传', '文件']
    for keyword in keywords:
        print(f"搜索关键词: {keyword}")
        cursor.execute("SELECT rowid, filename FROM documents_fts WHERE documents_fts MATCH ?", (keyword,))
        results = cursor.fetchall()
        print(f"结果数量: {len(results)}")
        for result in results:
            print(f"  - RowID: {result[0]}, Filename: {result[1]}")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_fts_data()