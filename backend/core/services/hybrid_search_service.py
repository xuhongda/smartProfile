from sqlalchemy.orm import Session
from sqlalchemy import text
from core.services.meta_store import meta_store
from core.services.vector_store import vector_store
from core.services.generic_ai_client import generic_ai_client
from core.utils.config import config
from typing import List, Dict, Any

class HybridSearchService:
    """混合检索服务"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(HybridSearchService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化混合检索服务"""
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.top_k = config.get("vector_search.top_k")
        self._initialized = True
    
    def search_knowledge_base(self, db: Session, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """搜索知识库
        
        Args:
            db: 数据库会话
            query: 查询文本
            top_k: 返回的结果数量，默认使用配置中的值
            
        Returns:
            搜索结果列表，每个结果包含 id、text、file_path 和 score
        """
        if not query:
            return []
        
        if top_k is None:
            top_k = self.top_k
        
        # 检查AI服务是否配置
        if generic_ai_client.is_configured():
            # 增强模式：使用ChromaDB向量检索
            return self._enhanced_search(db, query, top_k)
        else:
            # 基础模式：仅使用SQLite关键词检索
            return self._basic_search(db, query, top_k)
    
    def _enhanced_search(self, db: Session, query: str, top_k: int) -> List[Dict[str, Any]]:
        """增强模式搜索（使用ChromaDB向量检索）
        
        Args:
            db: 数据库会话
            query: 查询文本
            top_k: 返回的结果数量
            
        Returns:
            搜索结果列表
        """
        try:
            # 1. 在 ChromaDB 中查询相似文档
            vector_results = vector_store.query(query, top_k=top_k)
            
            # 提取文档 ID 和相似度分数
            doc_ids = vector_results.get("ids", [[]])[0]
            distances = vector_results.get("distances", [[]])[0]
            
            if not doc_ids:
                return []
            
            # 2. 在 SQLite 中获取完整文档信息
            documents = meta_store.get_documents_by_uuids(db, doc_ids)
            
            # 3. 组装搜索结果
            results = []
            for doc_id, distance, doc in zip(doc_ids, distances, documents):
                # 计算相似度分数（将距离转换为相似度）
                score = 1.0 - distance if distance else 0.0
                
                # 构建文件路径
                file_path = f"/uploads/{doc.filename}"
                
                results.append({
                    "id": doc_id,
                    "text": doc.content,
                    "file_path": file_path,
                    "score": score,
                    "filename": doc.filename,
                    "file_type": doc.file_type
                })
            
            # 按相似度分数排序
            results.sort(key=lambda x: x["score"], reverse=True)
            
            return results
        except Exception as e:
            print(f"增强模式搜索失败: {str(e)}")
            # 降级到基础模式
            return self._basic_search(db, query, top_k)
    
    def _basic_search(self, db: Session, query: str, top_k: int) -> List[Dict[str, Any]]:
        """基础模式搜索（仅使用SQLite关键词检索）
        
        Args:
            db: 数据库会话
            query: 查询文本
            top_k: 返回的结果数量
            
        Returns:
            搜索结果列表
        """
        try:
            # 使用LIKE进行关键词搜索
            search_query = text("""
                SELECT 
                    id, uuid, filename, file_type, content, created_at, updated_at
                FROM documents 
                WHERE content LIKE :query OR filename LIKE :query
                LIMIT :top_k
            """)
            
            results = db.execute(search_query, {
                "query": f"%{query}%",
                "top_k": top_k
            }).fetchall()
            
            # 组装搜索结果
            search_results = []
            for result in results:
                # 构建文件路径
                file_path = f"/uploads/{result.filename}"
                
                search_results.append({
                    "id": result.uuid,
                    "text": result.content,
                    "file_path": file_path,
                    "score": 1.0,  # 基础模式默认分数
                    "filename": result.filename,
                    "file_type": result.file_type
                })
            
            return search_results
        except Exception as e:
            print(f"基础模式搜索失败: {str(e)}")
            return []
    
    def search_with_filter(self, db: Session, query: str, file_type: str = None, top_k: int = None) -> List[Dict[str, Any]]:
        """带过滤条件的搜索
        
        Args:
            db: 数据库会话
            query: 查询文本
            file_type: 文件类型过滤
            top_k: 返回的结果数量
            
        Returns:
            搜索结果列表
        """
        # 先执行基本搜索
        results = self.search_knowledge_base(db, query, top_k)
        
        # 应用过滤条件
        if file_type:
            results = [result for result in results if result.get("file_type") == file_type]
        
        return results

# 创建全局混合检索服务实例
hybrid_search_service = HybridSearchService()