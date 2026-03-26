import sqlite3

def test_fts_direct():
    """直接测试FTS5表的搜索功能"""
    conn = sqlite3.connect('data/unstructured_data.db')
    cursor = conn.cursor()
    
    # 测试FTS5搜索
    keywords = ['物理', '成绩', '教学', '声音', '压强', '浮力']
    
    for keyword in keywords:
        print(f"\n=== 直接搜索关键词: {keyword} ===")
        try:
            cursor.execute("SELECT rowid, filename FROM documents_fts WHERE documents_fts MATCH ?", (keyword,))
            results = cursor.fetchall()
            print(f"找到 {len(results)} 个结果")
            for result in results:
                print(f"  - RowID: {result[0]}, Filename: {result[1]}")
        except Exception as e:
            print(f"搜索失败: {str(e)}")
    
    conn.close()

def main():
    """主测试函数"""
    print("开始直接测试FTS5表的搜索功能...")
    print("=" * 70)
    test_fts_direct()
    print("=" * 70)
    print("测试完成")

if __name__ == "__main__":
    main()