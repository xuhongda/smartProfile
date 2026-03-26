from sqlalchemy.orm import Session
from core.services.meta_store import meta_store
from core.services.vector_store import vector_store
from core.utils.config import config
import os
import uuid
import asyncio
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor

class IngestionService:
    """数据写入服务"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(IngestionService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化数据写入服务"""
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.chunk_size = config.get("vector_search.chunk_size")
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._initialized = True
    
    def _chunk_text(self, text: str, chunk_size: int = None) -> List[str]:
        """将文本切分为多个块
        
        Args:
            text: 要切分的文本
            chunk_size: 块大小，默认使用配置中的值
            
        Returns:
            文本块列表
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
        
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)
        return chunks
    
    def ingest_document(self, db: Session, file_path: str, content_text: str) -> List[Dict[str, Any]]:
        """写入文档到存储系统
        
        Args:
            db: 数据库会话
            file_path: 文件路径
            content_text: 文件内容
            
        Returns:
            包含每个文档块信息的列表
        """
        results = []
        
        try:
            # 获取文件名和文件类型
            filename = os.path.basename(file_path)
            file_type = os.path.splitext(filename)[1].lstrip('.').lower()
            if not file_type:
                file_type = "txt"
            
            # 切分文本
            chunks = self._chunk_text(content_text)
            
            for i, chunk in enumerate(chunks):
                # 生成唯一的文档 ID
                doc_id = str(uuid.uuid4())
                
                # 先写 SQLite
                try:
                    document = meta_store.create_document(
                        db=db,
                        filename=filename,
                        file_type=file_type,
                        content=chunk,
                        doc_uuid=doc_id,
                        indexed=False  # 初始标记为未索引
                    )
                except Exception as e:
                    print(f"写入 SQLite 失败: {str(e)}")
                    continue
                
                # 异步写入 ChromaDB
                metadata = {
                    "filename": filename,
                    "file_type": file_type,
                    "file_path": file_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                
                # 提交到线程池执行
                self.executor.submit(
                    self._async_add_to_vector_store,
                    doc_id, chunk, metadata, db
                )
                
                # 记录结果
                results.append({
                    "id": doc_id,
                    "filename": filename,
                    "file_type": file_type,
                    "file_path": file_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "status": "pending"
                })
            
            return results
        except Exception as e:
            print(f"写入文档失败: {str(e)}")
            return []
    
    def _async_add_to_vector_store(self, doc_id: str, text: str, metadata: dict, db: Session):
        """异步添加到向量存储
        
        Args:
            doc_id: 文档ID
            text: 文本内容
            metadata: 元数据
            db: 数据库会话
        """
        try:
            # 尝试添加到向量存储
            success = vector_store.add_document(doc_id, text, metadata)
            
            if success:
                # 更新数据库中的索引状态
                meta_store.update_document_indexed(db, doc_id, True)
                print(f"文档 {doc_id} 向量索引成功")
            else:
                print(f"文档 {doc_id} 向量索引失败")
        except Exception as e:
            print(f"异步添加到向量存储失败: {str(e)}")
    
    def retry_indexing(self, db: Session, doc_id: str) -> bool:
        """手动重试索引
        
        Args:
            db: 数据库会话
            doc_id: 文档ID
            
        Returns:
            是否重试成功
        """
        try:
            # 获取文档信息
            document = meta_store.get_document_by_uuid(db, doc_id)
            if not document:
                print(f"文档 {doc_id} 不存在")
                return False
            
            # 重新尝试向量索引
            metadata = {
                "filename": document.filename,
                "file_type": document.file_type,
                "file_path": f"/uploads/{document.filename}",
                "chunk_index": 0,
                "total_chunks": 1
            }
            
            success = vector_store.add_document(doc_id, document.content, metadata)
            
            if success:
                meta_store.update_document_indexed(db, doc_id, True)
                print(f"文档 {doc_id} 重试索引成功")
                return True
            else:
                print(f"文档 {doc_id} 重试索引失败")
                return False
        except Exception as e:
            print(f"重试索引失败: {str(e)}")
            return False
    
    def ingest_batch(self, db: Session, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量写入文档
        
        Args:
            db: 数据库会话
            documents: 文档列表，每个文档包含 file_path 和 content_text
            
        Returns:
            批量写入结果
        """
        results = []
        
        for doc in documents:
            file_path = doc.get("file_path")
            content_text = doc.get("content_text")
            
            if file_path and content_text:
                doc_results = self.ingest_document(db, file_path, content_text)
                results.extend(doc_results)
        
        return results

# 创建全局数据写入服务实例
ingestion_service = IngestionService()