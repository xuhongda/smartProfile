import sys
import os
import tempfile

# 添加backend目录到Python搜索路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.services import container

def test_file_parser_service():
    """测试文件解析服务"""
    print("=== 测试文件解析服务 ===")
    
    # 获取文件解析服务
    file_parser_service = container.resolve('file_parser_service')
    
    # 测试文本文件解析
    test_content = "这是一个测试文本文件"
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(test_content.encode('utf-8'))
        temp_txt_file = f.name
    
    try:
        with open(temp_txt_file, 'rb') as f:
            content = f.read()
        parse_result = file_parser_service.parse_file(content, 'test.txt')
        assert parse_result.filename == 'test.txt', "文本文件名错误"
        assert parse_result.file_type == 'txt', "文本文件类型错误"
        assert parse_result.content == test_content, "文本文件内容错误"
        assert parse_result.content_length == len(test_content), "文本文件长度错误"
        print("✓ 文本文件解析测试通过")
    finally:
        if os.path.exists(temp_txt_file):
            os.unlink(temp_txt_file)
    
    # 测试文件类型支持检查
    assert file_parser_service.supports_file_type('test.txt') == True, "文本文件类型支持检查失败"
    assert file_parser_service.supports_file_type('test.xlsx') == True, "Excel文件类型支持检查失败"
    assert file_parser_service.supports_file_type('test.docx') == True, "Word文件类型支持检查失败"
    assert file_parser_service.supports_file_type('test.pdf') == False, "不支持的文件类型检查失败"
    print("✓ 文件类型支持检查测试通过")
    
    print("=== 文件解析服务测试通过 ===")

if __name__ == "__main__":
    test_file_parser_service()
