import sys
import os

# 添加backend目录到Python搜索路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from core.utils.config import config

def test_config_management():
    """测试配置管理系统"""
    print("=== 测试配置管理系统 ===")
    
    # 测试默认配置
    assert config.get('database.url') == 'sqlite:///data/unstructured_data.db', "数据库URL配置错误"
    assert config.get('upload.directory') == 'uploads', "上传目录配置错误"
    assert config.get('upload.max_size') == 20971520, "上传大小限制配置错误"
    assert config.get('api.title') == 'Unstructured Data Search API', "API标题配置错误"
    print("✓ 默认配置测试通过")
    
    # 测试配置获取
    db_url = config.get('database.url')
    assert isinstance(db_url, str), "配置获取失败"
    print("✓ 配置获取测试通过")
    
    # 测试嵌套配置获取
    cors_origins = config.get('cors.allow_origins')
    assert isinstance(cors_origins, list), "嵌套配置获取失败"
    print("✓ 嵌套配置获取测试通过")
    
    # 测试默认值
    non_existent = config.get('non.existent.key', 'default')
    assert non_existent == 'default', "默认值测试失败"
    print("✓ 默认值测试通过")
    
    # 测试配置设置
    config.set('test.key', 'test.value')
    assert config.get('test.key') == 'test.value', "配置设置失败"
    print("✓ 配置设置测试通过")
    
    # 测试配置转换为字典
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict), "配置转换为字典失败"
    print("✓ 配置转换为字典测试通过")
    
    print("=== 配置管理系统测试通过 ===")

if __name__ == "__main__":
    test_config_management()
