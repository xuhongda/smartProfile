from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base, Document

class DatabaseService:
    """数据库操作服务"""
    
    def __init__(self, database_url: str = 'sqlite:///data/unstructured_data.db'):
        self.engine = create_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        """获取数据库会话
        
        Returns:
            Session: 数据库会话
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def init_database(self):
        """初始化数据库"""
        # 先删除现有的documents表和相关对象
        with self.engine.connect() as conn:
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
        with self.engine.connect() as conn:
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
        with self.engine.connect() as conn:
            # 先删除旧的FTS表和触发器（如果存在）
            conn.execute(text("DROP TRIGGER IF EXISTS documents_ai"))
            conn.execute(text("DROP TRIGGER IF EXISTS documents_ad"))
            conn.execute(text("DROP TRIGGER IF EXISTS documents_au"))
            conn.execute(text("DROP TABLE IF EXISTS documents_fts"))
            conn.commit()
            
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
    
    def bulk_insert(self, db, model, data_list):
        """批量插入数据
        
        Args:
            db: 数据库会话
            model: 数据模型类
            data_list: 数据列表，每个元素是一个字典
            
        Returns:
            int: 插入的记录数量
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
    
    def bulk_update(self, db, model, data_list, primary_key='id'):
        """批量更新数据
        
        Args:
            db: 数据库会话
            model: 数据模型类
            data_list: 数据列表，每个元素是一个字典，包含主键和要更新的字段
            primary_key: 主键字段名
            
        Returns:
            int: 更新的记录数量
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
