from typing import List
from sqlalchemy import text
from core.models.search_result import SearchResult, SearchItem

class SearchService:
    """搜索服务"""
    
    def __init__(self, tokenizer_service, database_service):
        self.tokenizer_service = tokenizer_service
        self.database_service = database_service
    
    def search(self, db, query: str, page: int = 1, page_size: int = 10) -> SearchResult:
        """搜索文档
        
        Args:
            db: 数据库会话
            query: 搜索关键词
            page: 页码
            page_size: 每页大小
            
        Returns:
            SearchResult: 搜索结果
        """
        if not query:
            raise ValueError("搜索关键词不能为空")
        
        # 对搜索关键词进行分词处理
        if self.tokenizer_service.is_chinese(query):
            query = self.tokenizer_service.tokenize_query(query)
        
        # 使用FTS5全文搜索
        search_query = text("""
            SELECT 
                d.id, d.uuid, d.filename, d.file_type, d.content, d.created_at, d.updated_at
            FROM documents d
            JOIN documents_fts ON d.id = documents_fts.rowid
            WHERE documents_fts MATCH :query
            LIMIT :page_size OFFSET :offset
        """)
        
        offset = (page - 1) * page_size
        results = db.execute(search_query, {
            "query": query,
            "page_size": page_size,
            "offset": offset
        }).fetchall()
        
        # 计算总结果数
        count_query = text("""
            SELECT COUNT(*)
            FROM documents d
            JOIN documents_fts ON d.id = documents_fts.rowid
            WHERE documents_fts MATCH :query
        """)
        total = db.execute(count_query, {"query": query}).scalar() or 0
        
        # 构建搜索结果
        items = []
        for result in results:
            # 生成摘要，包含关键词上下文
            content = result.content
            # 简单的摘要生成逻辑
            if query in content:
                start = max(0, content.find(query) - 100)
                end = min(len(content), content.find(query) + len(query) + 100)
                snippet = content[start:end]
            else:
                snippet = content[:200]
            
            # 构建文件路径
            file_path = f"/uploads/{result.filename}"
            
            items.append(SearchItem(
                id=result.id,
                uuid=result.uuid,
                filename=result.filename,
                file_type=result.file_type,
                content=result.content,
                snippet=snippet,
                file_path=file_path,
                created_at=result.created_at,
                updated_at=result.updated_at
            ))
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return SearchResult(
            query=query,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            results=items
        )
    
    def get_search_count(self, db, query: str) -> int:
        """获取搜索结果数量
        
        Args:
            db: 数据库会话
            query: 搜索关键词
            
        Returns:
            int: 搜索结果数量
        """
        if not query:
            return 0
        
        # 对搜索关键词进行分词处理
        if self.tokenizer_service.is_chinese(query):
            query = self.tokenizer_service.tokenize_query(query)
        
        count_query = text("""
            SELECT COUNT(*)
            FROM documents d
            JOIN documents_fts ON d.id = documents_fts.rowid
            WHERE documents_fts MATCH :query
        """)
        total = db.execute(count_query, {"query": query}).scalar() or 0
        
        return total
