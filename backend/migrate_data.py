from database import get_db
from core.services.meta_store import meta_store
from core.services.vector_store import vector_store
from core.services.ingestion_service import ingestion_service
import os

# 数据迁移脚本
def migrate_existing_data():
    """迁移现有数据到向量存储"""
    print("开始数据迁移...")
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 获取所有文档
        documents = meta_store.get_all_documents(db, limit=1000)
        print(f"找到 {len(documents)} 个文档需要迁移")
        
        # 迁移每个文档
        success_count = 0
        failed_count = 0
        
        for i, doc in enumerate(documents):
            print(f"迁移文档 {i+1}/{len(documents)}: {doc.filename}")
            
            try:
                # 构建文件路径
                file_path = f"/uploads/{doc.filename}"
                
                # 使用 ingestion_service 进行迁移
                # 注意：这里会重新生成 UUID，因为我们需要为每个文档生成新的向量
                # 如果需要保持原有的 UUID，可以修改 ingestion_service 的实现
                results = ingestion_service.ingest_document(db, file_path, doc.content)
                
                if results:
                    success_count += 1
                    print(f"  成功: {len(results)} 个文档块")
                else:
                    failed_count += 1
                    print(f"  失败: 无法迁移")
            except Exception as e:
                failed_count += 1
                print(f"  错误: {str(e)}")
        
        print(f"\n迁移完成:")
        print(f"成功: {success_count} 个文档")
        print(f"失败: {failed_count} 个文档")
        
    except Exception as e:
        print(f"迁移过程中发生错误: {str(e)}")
    finally:
        # 关闭数据库会话
        db.close()

# 执行迁移
if __name__ == "__main__":
    migrate_existing_data()