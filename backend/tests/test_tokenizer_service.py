import sys
import os

# 添加backend目录到Python搜索路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.services import container

def test_tokenizer_service():
    """测试分词处理服务"""
    print("=== 测试分词处理服务 ===")
    
    # 获取分词服务
    tokenizer_service = container.resolve('tokenizer_service')
    
    # 测试中文分词
    test_text = "这是一个测试文本，用于测试分词服务"
    tokenized_text = tokenizer_service.tokenize_text(test_text)
    assert isinstance(tokenized_text, str), "分词结果类型错误"
    assert len(tokenized_text) > 0, "分词结果为空"
    print(f"✓ 中文分词测试通过: {tokenized_text}")
    
    # 测试搜索查询分词
    test_query = "测试分词"
    tokenized_query = tokenizer_service.tokenize_query(test_query)
    assert isinstance(tokenized_query, str), "查询分词结果类型错误"
    assert len(tokenized_query) > 0, "查询分词结果为空"
    print(f"✓ 搜索查询分词测试通过: {tokenized_query}")
    
    # 测试中文检测
    chinese_text = "中文文本"
    english_text = "English text"
    assert tokenizer_service.is_chinese(chinese_text) == True, "中文检测失败"
    assert tokenizer_service.is_chinese(english_text) == False, "英文检测失败"
    print("✓ 中文检测测试通过")
    
    # 测试空字符串处理
    empty_text = ""
    assert tokenizer_service.tokenize_text(empty_text) == "", "空字符串处理失败"
    assert tokenizer_service.tokenize_query(empty_text) == "", "空查询处理失败"
    assert tokenizer_service.is_chinese(empty_text) == False, "空字符串中文检测失败"
    print("✓ 空字符串处理测试通过")
    
    print("=== 分词处理服务测试通过 ===")

if __name__ == "__main__":
    test_tokenizer_service()
