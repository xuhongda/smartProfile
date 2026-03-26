import os
import numpy as np
from chromadb import PersistentClient, Client
from core.utils.config import config
from core.services.generic_ai_client import generic_ai_client

class VectorStore:
    """向量存储类，封装 ChromaDB 操作"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化向量存储"""
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.chroma_path = config.get("vector_search.chroma_path")
        self.collection_name = "documents"
        
        # 确保 ChromaDB 存储目录存在
        os.makedirs(self.chroma_path, exist_ok=True)
        
        # 初始化 ChromaDB 客户端
        try:
            self.client = PersistentClient(path=self.chroma_path)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"成功初始化 ChromaDB 集合: {self.collection_name}")
        except Exception as e:
            print(f"初始化 ChromaDB 失败: {str(e)}")
            self.client = None
            self.collection = None
        
        self._initialized = True
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """生成文本的向量表示
        
        Args:
            text: 要向量化的文本
            
        Returns:
            文本的向量表示，如果失败则返回 None
        """
        try:
            # 使用通用AI客户端生成嵌入
            embedding = generic_ai_client.create_embedding(text)
            if embedding:
                return np.array(embedding)
            else:
                print("AI服务未配置或生成嵌入失败")
                return None
        except Exception as e:
            print(f"生成向量失败: {str(e)}")
            return None
    
    def add_document(self, doc_id: str, text: str, metadata: dict = None):
        """添加文档到向量存储
        
        Args:
            doc_id: 文档的唯一标识符
            text: 文档文本
            metadata: 文档元数据
            
        Returns:
            成功返回 True，失败返回 False
        """
        if not self.collection:
            print("向量存储未初始化，无法添加文档")
            return False
        
        try:
            # 生成向量
            embedding = self.generate_embedding(text)
            if embedding is None:
                return False
            
            # 添加到 ChromaDB
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding.tolist()],
                documents=[text],
                metadatas=[metadata] if metadata else None
            )
            return True
        except Exception as e:
            print(f"添加文档到向量存储失败: {str(e)}")
            return False
    
    def query(self, query_text: str, top_k: int = 10):
        """查询相似文档
        
        Args:
            query_text: 查询文本
            top_k: 返回的结果数量
            
        Returns:
            包含 ids, distances 和 metadatas 的字典
        """
        if not self.collection:
            print("向量存储未初始化，无法查询")
            return {"ids": [], "distances": [], "metadatas": []}
        
        try:
            # 生成查询向量
            query_embedding = self.generate_embedding(query_text)
            if query_embedding is None:
                return {"ids": [], "distances": [], "metadatas": []}
            
            # 查询相似文档
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include=["distances", "metadatas"]
            )
            
            return results
        except Exception as e:
            print(f"查询向量存储失败: {str(e)}")
            return {"ids": [], "distances": [], "metadatas": []}
    
    def delete_document(self, doc_id: str):
        """从向量存储中删除文档
        
        Args:
            doc_id: 文档的唯一标识符
            
        Returns:
            成功返回 True，失败返回 False
        """
        if not self.collection:
            print("向量存储未初始化，无法删除文档")
            return False
        
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"删除文档失败: {str(e)}")
            return False
    
    def get_collection_stats(self):
        """获取集合统计信息
        
        Returns:
            集合统计信息
        """
        if not self.collection:
            return {"status": "uninitialized"}
        
        try:
            stats = self.collection.count()
            return {"status": "initialized", "count": stats}
        except Exception as e:
            print(f"获取集合统计信息失败: {str(e)}")
            return {"status": "error", "message": str(e)}

# 创建全局向量存储实例
vector_store = VectorStore()