from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import uuid

# 创建数据库引擎
import os
# 使用配置中的数据库路径
db_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, 'unstructured_data.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 文档表
class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), nullable=False, index=True)
    file_type = Column(String(50), nullable=False, index=True)  # excel, word, txt
    content = Column(Text, nullable=False)
    indexed = Column(Integer, default=0)  # 0: 未索引, 1: 已索引
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# 初始化数据库
def init_db():
    # 先删除现有的documents表和相关对象
    with engine.connect() as conn:
        # 删除触发器
        conn.execute(text("DROP TRIGGER IF EXISTS documents_ai"))
        conn.execute(text("DROP TRIGGER IF EXISTS documents_ad"))
        conn.execute(text("DROP TRIGGER IF EXISTS documents_au"))
        # 删除FTS表
        conn.execute(text("DROP TABLE IF EXISTS documents_fts"))
        # 删除documents表
        conn.execute(text("DROP TABLE IF EXISTS documents"))
        conn.commit()
        print("成功删除现有表结构")
    
    # 创建普通表
    with engine.connect() as conn:
        # 直接使用SQL语句创建documents表，确保包含indexed字段
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT UNIQUE,
                filename VARCHAR(255) NOT NULL,
                file_type VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                indexed INTEGER DEFAULT 0,
                created_at DATETIME,
                updated_at DATETIME
            )
        """))
        # 创建索引
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_documents_filename ON documents(filename)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_documents_file_type ON documents(file_type)"))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_uuid ON documents(uuid)"))
        conn.commit()
        print("成功重新创建表结构")
    
    # 创建FTS5虚拟表用于全文搜索
    with engine.connect() as conn:
        # 先删除旧的FTS表和触发器（如果存在）
        conn.execute(text("DROP TRIGGER IF EXISTS documents_ai"))
        conn.execute(text("DROP TRIGGER IF EXISTS documents_ad"))
        conn.execute(text("DROP TRIGGER IF EXISTS documents_au"))
        conn.execute(text("DROP TABLE IF EXISTS documents_fts"))
        
        # 创建FTS5虚拟表
        conn.execute(text("""
            CREATE VIRTUAL TABLE documents_fts USING fts5(
                content,
                filename,
                file_type
            )
        """))
        
        # 创建触发器，当documents表发生变化时自动更新FTS表
        conn.execute(text("""
            CREATE TRIGGER documents_ai AFTER INSERT ON documents BEGIN
                INSERT INTO documents_fts(rowid, content, filename, file_type)
                VALUES(new.id, new.content, new.filename, new.file_type);
            END;
        """))
        
        conn.execute(text("""
            CREATE TRIGGER documents_ad AFTER DELETE ON documents BEGIN
                DELETE FROM documents_fts WHERE rowid = old.id;
            END;
        """))
        
        conn.execute(text("""
            CREATE TRIGGER documents_au AFTER UPDATE ON documents BEGIN
                UPDATE documents_fts SET 
                    content = new.content, 
                    filename = new.filename, 
                    file_type = new.file_type 
                WHERE rowid = new.id;
            END;
        """))
        
        conn.commit()
        print("FTS5虚拟表和触发器创建成功")
    
    print("数据库初始化完成，表结构创建成功")

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 批量插入数据
def bulk_insert(db, model, data_list):
    """批量插入数据
    
    Args:
        db: 数据库会话
        model: 数据模型类
        data_list: 数据列表，每个元素是一个字典
    
    Returns:
        插入的记录数量
    """
    try:
        # 打印插入信息
        print(f"开始批量插入 {len(data_list)} 条记录到 {model.__tablename__} 表")
        # 使用SQLAlchemy的bulk_insert_mappings方法进行批量插入
        db.bulk_insert_mappings(model, data_list)
        db.commit()
        print(f"批量插入完成，共插入 {len(data_list)} 条记录")
        return len(data_list)
    except Exception as e:
        db.rollback()
        print(f"批量插入失败: {str(e)}")
        raise e

# 批量更新数据
def bulk_update(db, model, data_list, primary_key='id'):
    """批量更新数据
    
    Args:
        db: 数据库会话
        model: 数据模型类
        data_list: 数据列表，每个元素是一个字典，包含主键和要更新的字段
        primary_key: 主键字段名
    
    Returns:
        更新的记录数量
    """
    try:
        # 分批处理，每批1000条
        batch_size = 1000
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i+batch_size]
            db.bulk_update_mappings(model, batch)
        db.commit()
        return len(data_list)
    except Exception as e:
        db.rollback()
        raise e