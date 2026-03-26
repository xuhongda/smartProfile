import sqlite3

def check_triggers():
    """检查触发器的具体定义"""
    conn = sqlite3.connect('data/unstructured_data.db')
    cursor = conn.cursor()
    
    # 检查每个触发器的定义
    triggers = ['documents_ai', 'documents_ad', 'documents_au']
    for trigger in triggers:
        print(f"=== {trigger} 触发器定义 ===")
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='trigger' AND name='{trigger}'")
        result = cursor.fetchone()
        if result:
            print(result[0])
        else:
            print("未找到触发器定义")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_triggers()