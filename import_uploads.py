import os
import sqlite3
from datetime import datetime

# 配置
UPLOAD_DIR = 'backend/uploads'
DB_PATH = 'backend/data/unstructured_data.db'

# 连接到数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 检查并创建必要的表结构
try:
    # 检查文档表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
    if not cursor.fetchone():
        # 创建文档表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT,
            filename VARCHAR(255) NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            indexed INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建FTS表
        cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING FTS5(
            content,
            filename,
            tokenize="porter"
        )
        ''')
        
        # 创建触发器
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents
        BEGIN
            INSERT INTO documents_fts(rowid, content, filename) VALUES (new.id, new.content, new.filename);
        END
        ''')
        
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents
        BEGIN
            DELETE FROM documents_fts WHERE rowid = old.id;
        END
        ''')
        
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents
        BEGIN
            UPDATE documents_fts SET content = new.content, filename = new.filename WHERE rowid = old.id;
        END
        ''')
        
        conn.commit()
        print("数据库表结构已创建")
except Exception as e:
    print(f"数据库操作失败: {e}")

# 处理文件类型
def get_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.xlsx', '.xls']:
        return 'excel'
    elif ext in ['.docx']:
        return 'word'
    elif ext in ['.txt']:
        return 'txt'
    else:
        return 'unknown'

# 读取文件内容
def read_file_content(file_path, file_type):
    try:
        if file_type == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif file_type == 'excel':
            try:
                import pandas as pd
                df = pd.read_excel(file_path)
                return df.to_string()
            except:
                return f"Excel文件: {os.path.basename(file_path)}"
        elif file_type == 'word':
            try:
                from docx import Document
                doc = Document(file_path)
                content = '\n'.join([para.text for para in doc.paragraphs])
                return content
            except:
                return f"Word文件: {os.path.basename(file_path)}"
        else:
            return f"文件: {os.path.basename(file_path)}"
    except Exception as e:
        return f"读取文件失败: {str(e)}"

# 处理uploads目录中的文件
print("开始处理uploads目录中的文件...")

for filename in os.listdir(UPLOAD_DIR):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.isfile(file_path):
        # 检查文件是否已存在于数据库
        cursor.execute("SELECT id FROM documents WHERE filename = ?", (filename,))
        if cursor.fetchone():
            print(f"文件 {filename} 已存在于数据库中，跳过")
            continue
        
        # 获取文件类型
        file_type = get_file_type(filename)
        
        # 读取文件内容
        content = read_file_content(file_path, file_type)
        
        # 生成UUID
        import uuid
        file_uuid = str(uuid.uuid4())
        
        # 插入数据库
        try:
            cursor.execute(
                "INSERT INTO documents (uuid, filename, file_type, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (file_uuid, filename, file_type, content, datetime.now(), datetime.now())
            )
            conn.commit()
            print(f"文件 {filename} 已成功添加到数据库")
        except Exception as e:
            print(f"添加文件 {filename} 失败: {e}")
            conn.rollback()

# 关闭连接
conn.close()
print("处理完成")