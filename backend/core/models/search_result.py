from typing import List
from datetime import datetime

class SearchItem:
    """搜索结果项模型"""
    
    def __init__(self, id: int, uuid: str, filename: str, file_type: str, content: str, snippet: str, 
                 file_path: str, created_at: datetime, updated_at: datetime):
        self.id = id
        self.uuid = uuid
        self.filename = filename
        self.file_type = file_type
        self.content = content
        self.snippet = snippet
        self.file_path = file_path
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.uuid,  # 使用uuid作为id返回，保持前端兼容性
            "uuid": self.uuid,
            "filename": self.filename,
            "file_type": self.file_type,
            "content": self.content,
            "snippet": self.snippet,
            "file_path": self.file_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class SearchResult:
    """搜索结果模型"""
    
    def __init__(self, query: str, total: int, page: int, page_size: int, 
                 total_pages: int, results: List[SearchItem]):
        self.query = query
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = total_pages
        self.results = results
    
    def to_dict(self):
        """转换为字典"""
        return {
            "query": self.query,
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "results": [item.to_dict() for item in self.results]
        }
