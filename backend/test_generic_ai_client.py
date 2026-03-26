from core.services.generic_ai_client import generic_ai_client
from core.utils.config import config

# 测试通用AI连接器
def test_generic_ai_client():
    """测试通用AI连接器"""
    print("开始测试通用AI连接器...")
    
    # 测试配置检查
    print("\n1. 测试配置检查...")
    is_configured = generic_ai_client.is_configured()
    print(f"AI服务是否配置: {is_configured}")
    
    # 测试更新配置
    print("\n2. 测试更新配置...")
    generic_ai_client.update_config()
    print("配置更新成功")
    
    # 测试创建嵌入
    print("\n3. 测试创建嵌入...")
    test_text = "这是一个测试文本"
    embedding = generic_ai_client.create_embedding(test_text)
    if embedding:
        print(f"成功创建嵌入，向量长度: {len(embedding)}")
    else:
        print("创建嵌入失败，可能是因为AI服务未配置")
    
    # 测试聊天完成
    print("\n4. 测试聊天完成...")
    test_messages = [
        {"role": "user", "content": "你好，你是谁？"}
    ]
    response = generic_ai_client.chat_completion(test_messages)
    if response:
        print(f"成功获取聊天响应: {response}")
    else:
        print("获取聊天响应失败，可能是因为AI服务未配置")
    
    print("\n通用AI连接器测试完成！")

# 执行测试
if __name__ == "__main__":
    test_generic_ai_client()