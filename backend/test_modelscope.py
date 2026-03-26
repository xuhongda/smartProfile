# 测试 ModelScope 库导入

try:
    import modelscope
    print("ModelScope 库导入成功!")
    print(f"ModelScope 版本: {modelscope.__version__}")
except ImportError as e:
    print(f"ModelScope 库导入失败: {e}")
