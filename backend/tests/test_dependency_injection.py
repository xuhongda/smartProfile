import sys
import os

# 添加backend目录到Python搜索路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.services import container

def test_dependency_injection():
    """测试依赖注入机制"""
    print("=== 测试依赖注入机制 ===")
    
    # 测试服务注册
    assert container.has('database_service'), "数据库服务未注册"
    assert container.has('tokenizer_service'), "分词服务未注册"
    assert container.has('file_parser_service'), "文件解析服务未注册"
    assert container.has('document_manager_service'), "文档管理服务未注册"
    assert container.has('search_service'), "搜索服务未注册"
    print("✓ 所有服务注册成功")
    
    # 测试服务解析
    database_service = container.resolve('database_service')
    assert database_service is not None, "数据库服务解析失败"
    print("✓ 数据库服务解析成功")
    
    tokenizer_service = container.resolve('tokenizer_service')
    assert tokenizer_service is not None, "分词服务解析失败"
    print("✓ 分词服务解析成功")
    
    file_parser_service = container.resolve('file_parser_service')
    assert file_parser_service is not None, "文件解析服务解析失败"
    print("✓ 文件解析服务解析成功")
    
    document_manager_service = container.resolve('document_manager_service')
    assert document_manager_service is not None, "文档管理服务解析失败"
    print("✓ 文档管理服务解析成功")
    
    search_service = container.resolve('search_service')
    assert search_service is not None, "搜索服务解析失败"
    print("✓ 搜索服务解析成功")
    
    # 测试服务功能
    test_text = "这是一个测试文本，用于测试分词服务"
    tokenized_text = tokenizer_service.tokenize_text(test_text)
    assert isinstance(tokenized_text, str), "分词服务功能测试失败"
    print("✓ 分词服务功能测试成功")
    
    print("=== 依赖注入机制测试通过 ===")

if __name__ == "__main__":
    test_dependency_injection()
