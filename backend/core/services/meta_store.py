from sqlalchemy.orm import Session
from database import Document, get_db
import uuid
from typing import List, Optional, Dict, Any

class MetaStore:
    """元数据存储类，封装 SQLite 操作"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(MetaStore, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化元数据存储"""
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._initialized = True
    
    def create_document(self, db: Session, filename: str, file_type: str, content: str, doc_uuid: Optional[str] = None, indexed: bool = False) -> Document:
        """创建文档
        
        Args:
            db: 数据库会话
            filename: 文件名
            file_type: 文件类型
            content: 文件内容
            doc_uuid: 文档 UUID，如果不提供则生成新的
            indexed: 是否已索引
            
        Returns:
            创建的文档对象
        """
        try:
            # 生成 UUID
            if not doc_uuid:
                doc_uuid = str(uuid.uuid4())
            
            # 创建文档
            document = Document(
                uuid=doc_uuid,
                filename=filename,
                file_type=file_type,
                content=content,
                indexed=indexed
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            return document
        except Exception as e:
            db.rollback()
            print(f"创建文档失败: {str(e)}")
            raise
    
    def get_document_by_uuid(self, db: Session, doc_uuid: str) -> Optional[Document]:
        """根据 UUID 获取文档
        
        Args:
            db: 数据库会话
            doc_uuid: 文档 UUID
            
        Returns:
            文档对象，如果不存在则返回 None
        """
        try:
            return db.query(Document).filter(Document.uuid == doc_uuid).first()
        except Exception as e:
            print(f"获取文档失败: {str(e)}")
            return None
    
    def get_documents_by_uuids(self, db: Session, doc_uuids: List[str]) -> List[Document]:
        """根据多个 UUID 获取文档
        
        Args:
            db: 数据库会话
            doc_uuids: 文档 UUID 列表
            
        Returns:
            文档对象列表
        """
        try:
            return db.query(Document).filter(Document.uuid.in_(doc_uuids)).all()
        except Exception as e:
            print(f"批量获取文档失败: {str(e)}")
            return []
    
    def delete_document(self, db: Session, doc_uuid: str) -> bool:
        """删除文档
        
        Args:
            db: 数据库会话
            doc_uuid: 文档 UUID
            
        Returns:
            成功返回 True，失败返回 False
        """
        try:
            document = db.query(Document).filter(Document.uuid == doc_uuid).first()
            if document:
                db.delete(document)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"删除文档失败: {str(e)}")
            return False
    
    def get_all_documents(self, db: Session, limit: int = 100) -> List[Document]:
        """获取所有文档
        
        Args:
            db: 数据库会话
            limit: 返回的文档数量限制
            
        Returns:
            文档对象列表
        """
        try:
            return db.query(Document).limit(limit).all()
        except Exception as e:
            print(f"获取所有文档失败: {str(e)}")
            return []
    
    def get_document_count(self, db: Session) -> int:
        """获取文档数量
        
        Args:
            db: 数据库会话
            
        Returns:
            文档数量
        """
        try:
            return db.query(Document).count()
        except Exception as e:
            print(f"获取文档数量失败: {str(e)}")
            return 0
    
    def update_document_indexed(self, db: Session, doc_uuid: str, indexed: bool) -> bool:
        """更新文档的索引状态
        
        Args:
            db: 数据库会话
            doc_uuid: 文档 UUID
            indexed: 索引状态
            
        Returns:
            成功返回 True，失败返回 False
        """
        try:
            document = db.query(Document).filter(Document.uuid == doc_uuid).first()
            if document:
                document.indexed = indexed
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"更新文档索引状态失败: {str(e)}")
            return False

# 创建全局元数据存储实例
meta_store = MetaStore()