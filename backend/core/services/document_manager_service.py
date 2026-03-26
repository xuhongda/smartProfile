from datetime import datetime
from typing import List, Optional
from database import Document as DocumentModel
from core.models.document import Document, DocumentList

class DocumentManagerService:
    """文档管理服务"""
    
    def __init__(self, database_service):
        self.database_service = database_service
    
    def create_document(self, db, filename: str, file_type: str, content: str):
        """创建文档
        
        Args:
            db: 数据库会话
            filename: 文件名
            file_type: 文件类型
            content: 文件内容
            
        Returns:
            tuple: (Document, str) - (创建的文档, 消息)
        """
        # 检查是否已存在同名文件
        existing_doc = db.query(DocumentModel).filter(DocumentModel.filename == filename).first()
        
        if existing_doc:
            # 更新现有文件
            existing_doc.content = content
            existing_doc.file_type = file_type
            existing_doc.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing_doc)
            doc_id = existing_doc.id
            message = f"文件 '{filename}' 已更新"
        else:
            # 创建新文件记录
            new_doc = DocumentModel(
                filename=filename,
                file_type=file_type,
                content=content
            )
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)
            doc_id = new_doc.id
            message = f"文件 '{filename}' 上传成功"
        
        # 构建返回的文档对象
        doc = Document(
            id=doc_id,
            filename=filename,
            file_type=file_type,
            content=content,
            content_length=len(content),
            created_at=existing_doc.created_at if existing_doc else new_doc.created_at,
            updated_at=existing_doc.updated_at if existing_doc else new_doc.updated_at
        )
        
        return doc, message
    
    def update_document(self, db, doc_id: int, content: str, file_type: str) -> Document:
        """更新文档
        
        Args:
            db: 数据库会话
            doc_id: 文档ID
            content: 新的内容
            file_type: 新的文件类型
            
        Returns:
            Document: 更新后的文档
        """
        doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if not doc:
            raise ValueError(f"文档不存在: {doc_id}")
        
        doc.content = content
        doc.file_type = file_type
        doc.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(doc)
        
        return Document(
            id=doc.id,
            filename=doc.filename,
            file_type=doc.file_type,
            content=doc.content,
            content_length=len(doc.content),
            created_at=doc.created_at,
            updated_at=doc.updated_at
        )
    
    def delete_document(self, db, doc_id: int) -> bool:
        """删除文档
        
        Args:
            db: 数据库会话
            doc_id: 文档ID
            
        Returns:
            bool: 是否删除成功
        """
        doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if not doc:
            raise ValueError(f"文档不存在: {doc_id}")
        
        db.delete(doc)
        db.commit()
        return True
    
    def get_document(self, db, doc_id: int) -> Document:
        """获取文档
        
        Args:
            db: 数据库会话
            doc_id: 文档ID
            
        Returns:
            Document: 文档对象
        """
        doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
        if not doc:
            raise ValueError(f"文档不存在: {doc_id}")
        
        return Document(
            id=doc.id,
            filename=doc.filename,
            file_type=doc.file_type,
            content=doc.content,
            content_length=len(doc.content),
            created_at=doc.created_at,
            updated_at=doc.updated_at
        )
    
    def get_documents(self, db, page: int = 1, page_size: int = 10) -> DocumentList:
        """获取文档列表
        
        Args:
            db: 数据库会话
            page: 页码
            page_size: 每页大小
            
        Returns:
            DocumentList: 文档列表
        """
        from sqlalchemy import func
        
        # 计算总数
        total = db.query(func.count(DocumentModel.id)).scalar()
        
        # 查询文档
        offset = (page - 1) * page_size
        documents = db.query(DocumentModel).offset(offset).limit(page_size).all()
        
        # 构建文档列表
        doc_list = []
        for doc in documents:
            doc_list.append(Document(
                id=doc.id,
                filename=doc.filename,
                file_type=doc.file_type,
                content=doc.content,
                content_length=len(doc.content),
                created_at=doc.created_at,
                updated_at=doc.updated_at
            ))
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return DocumentList(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            documents=doc_list
        )
