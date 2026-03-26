import sys
import os

# 添加backend目录到Python搜索路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.services import container
from database import SessionLocal

def test_search_service():
    """测试搜索服务"""
    print("=== 测试搜索服务 ===")
    
    # 获取服务
    search_service = container.resolve('search_service')
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 测试搜索（使用已存在的文档）
        test_query = "测试"
        search_result = search_service.search(db, test_query)
        print(f"✓ 搜索测试通过，找到 {search_result.total} 个结果")
        
        # 测试搜索计数
        count = search_service.get_search_count(db, test_query)
        print(f"✓ 搜索计数测试通过，共 {count} 个结果")
        
        # 测试不存在的关键词
        no_result_query = "不存在的关键词"
        no_result = search_service.search(db, no_result_query)
        assert no_result.total == 0, "不存在的关键词应该返回0个结果"
        assert len(no_result.results) == 0, "不存在的关键词结果列表应该为空"
        print("✓ 不存在关键词搜索测试通过")
        
        # 测试分页
        page_size = 1
        page_result = search_service.search(db, test_query, page=1, page_size=page_size)
        assert len(page_result.results) <= page_size, "分页大小错误"
        print("✓ 分页测试通过")
        
    finally:
        db.close()
    
    print("=== 搜索服务测试通过 ===")

if __name__ == "__main__":
    test_search_service()
