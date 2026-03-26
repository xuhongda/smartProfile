from typing import List
from datetime import datetime

class Document:
    """文档模型"""
    
    def __init__(self, id: int, filename: str, file_type: str, content: str, 
                 content_length: int, created_at: datetime, updated_at: datetime):
        self.id = id
        self.filename = filename
        self.file_type = file_type
        self.content = content
        self.content_length = content_length
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "filename": self.filename,
            "file_type": self.file_type,
            "content_length": self.content_length,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class DocumentList:
    """文档列表模型"""
    
    def __init__(self, total: int, page: int, page_size: int, 
                 total_pages: int, documents: List[Document]):
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = total_pages
        self.documents = documents
    
    def to_dict(self):
        """转换为字典"""
        return {
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "documents": [doc.to_dict() for doc in self.documents]
        }
