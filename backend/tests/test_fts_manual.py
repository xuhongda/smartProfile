import sqlite3

def test_fts_manual():
    """手动测试FTS5功能"""
    conn = sqlite3.connect('data/unstructured_data.db')
    cursor = conn.cursor()

    # 先检查是否已存在id为1的记录
    cursor.execute("SELECT rowid FROM documents_fts WHERE rowid = 1")
    if not cursor.fetchone():
        # 手动向FTS5表中插入数据
        print("=== 手动向FTS5表插入数据 ===")
        cursor.execute("""
            INSERT INTO documents_fts(rowid, content, filename, file_type)      
            VALUES(1, '这是一个测试文件，用于测试文件上传功能。包含一些关键词：测试、上传、文件、功能。希望能够成功上传并被搜索到。', 'test_upload.txt', 'txt')        
        """)
        conn.commit()
    print("数据插入成功")
    
    # 检查FTS5表的内容
    print("\n=== documents_fts表内容 ===")
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
    test_fts_manual()