#!/usr/bin/env python3
"""
测试脚本：测试文件上传、普通搜索和 AI 搜索功能
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查接口"""
    print("=" * 50)
    print("测试1: 健康检查")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✓ 健康检查通过: {response.json()}")
            return True
        else:
            print(f"✗ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 健康检查异常: {str(e)}")
        return False

def test_file_upload():
    """测试文件上传功能"""
    print("\n" + "=" * 50)
    print("测试2: 文件上传")
    print("=" * 50)
    try:
        # 创建一个测试文件
        test_content = """
这是一个测试文件，用于测试文件上传和搜索功能。

人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个分支，
它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

机器学习是人工智能的一个子集，它使用算法和统计模型来让计算机系统能够从数据中
学习并做出预测或决策，而无需明确编程。

深度学习是机器学习的一个分支，它使用多层神经网络来模拟人脑的工作方式，
能够处理更复杂的任务，如图像识别、语音识别和自然语言处理。

这个文件还包含一些关于数据科学和大数据分析的内容。
数据科学是一门跨学科的领域，它使用科学方法、流程、算法和系统来从结构化和非结构化数据中提取知识和见解。
        """
        
        # 保存测试文件
        test_file_path = "test_upload_ai.txt"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        # 上传文件
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f, "text/plain")}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✓ 文件上传成功: {result.get('filename')}")
                print(f"  - 文件UUID: {result.get('file_uuid')}")
                print(f"  - 文件类型: {result.get('file_type')}")
                return True
            else:
                print(f"✗ 文件上传失败: {result.get('message')}")
                return False
        else:
            print(f"✗ 文件上传失败: {response.status_code}")
            print(f"  响应: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 文件上传异常: {str(e)}")
        return False

def test_normal_search():
    """测试普通搜索功能"""
    print("\n" + "=" * 50)
    print("测试3: 普通搜索（关键词搜索）")
    print("=" * 50)
    try:
        # 等待一下，确保文件已经被索引
        time.sleep(1)
        
        query = "人工智能"
        response = requests.get(f"{BASE_URL}/search?q={query}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                results = result.get("results", [])
                print(f"✓ 普通搜索成功")
                print(f"  - 查询: {query}")
                print(f"  - 找到 {len(results)} 个结果")
                if results:
                    print(f"  - 第一个结果: {results[0].get('filename')}")
                return True
            else:
                print(f"✗ 普通搜索失败: {result.get('message')}")
                return False
        else:
            print(f"✗ 普通搜索失败: {response.status_code}")
            print(f"  响应: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 普通搜索异常: {str(e)}")
        return False

def test_ai_search():
    """测试 AI 搜索功能（使用 @AI 前缀）"""
    print("\n" + "=" * 50)
    print("测试4: AI 搜索（使用 @AI 前缀）")
    print("=" * 50)
    try:
        query = "@AI 什么是机器学习"
        response = requests.get(f"{BASE_URL}/search?q={requests.utils.quote(query)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                results = result.get("results", [])
                ai_response = result.get("ai_response")
                print(f"✓ AI 搜索成功")
                print(f"  - 查询: {query}")
                print(f"  - 找到 {len(results)} 个结果")
                if ai_response:
                    print(f"  - AI 回答: {ai_response[:100]}...")
                else:
                    print(f"  - AI 回答: 无（可能 AI 服务未配置）")
                return True
            else:
                print(f"✗ AI 搜索失败: {result.get('message')}")
                return False
        else:
            print(f"✗ AI 搜索失败: {response.status_code}")
            print(f"  响应: {response.text}")
            return False
    except Exception as e:
        print(f"✗ AI 搜索异常: {str(e)}")
        return False

def test_ai_search_with_enable_ai():
    """测试 AI 搜索功能（使用 enable_ai 参数）"""
    print("\n" + "=" * 50)
    print("测试5: AI 搜索（使用 enable_ai 参数）")
    print("=" * 50)
    try:
        query = "深度学习"
        response = requests.get(f"{BASE_URL}/search?q={requests.utils.quote(query)}&enable_ai=true")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                results = result.get("results", [])
                ai_response = result.get("ai_response")
                print(f"✓ AI 搜索成功")
                print(f"  - 查询: {query}")
                print(f"  - 找到 {len(results)} 个结果")
                if ai_response:
                    print(f"  - AI 回答: {ai_response[:100]}...")
                else:
                    print(f"  - AI 回答: 无（可能 AI 服务未配置）")
                return True
            else:
                print(f"✗ AI 搜索失败: {result.get('message')}")
                return False
        else:
            print(f"✗ AI 搜索失败: {response.status_code}")
            print(f"  响应: {response.text}")
            return False
    except Exception as e:
        print(f"✗ AI 搜索异常: {str(e)}")
        return False

def test_ai_connection():
    """测试 AI 服务连接"""
    print("\n" + "=" * 50)
    print("测试6: AI 服务连接测试")
    print("=" * 50)
    try:
        # 使用用户配置的 API 地址和密钥
        config_data = {
            "api_base_url": "https://api.deepseek.com",
            "api_key": "sk-e8db40ecc0dd4b44a16e4b1b182ba19d"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/ai/test-connection",
            json=config_data
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✓ AI 服务连接成功")
                print(f"  - 消息: {result.get('message')}")
                return True
            else:
                print(f"✗ AI 服务连接失败: {result.get('message')}")
                return False
        else:
            print(f"✗ AI 服务连接测试失败: {response.status_code}")
            print(f"  响应: {response.text}")
            return False
    except Exception as e:
        print(f"✗ AI 服务连接测试异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("开始测试所有功能")
    print("=" * 50)
    
    results = []
    
    # 测试健康检查
    results.append(("健康检查", test_health()))
    
    # 测试文件上传
    results.append(("文件上传", test_file_upload()))
    
    # 测试普通搜索
    results.append(("普通搜索", test_normal_search()))
    
    # 测试 AI 搜索（使用 @AI 前缀）
    results.append(("AI 搜索（@AI）", test_ai_search()))
    
    # 测试 AI 搜索（使用 enable_ai 参数）
    results.append(("AI 搜索（enable_ai）", test_ai_search_with_enable_ai()))
    
    # 测试 AI 服务连接
    results.append(("AI 服务连接", test_ai_connection()))
    
    # 打印测试总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {name}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 所有测试都通过了！")
    else:
        print(f"\n⚠️ 有 {total - passed} 个测试失败，请检查相关功能。")

if __name__ == "__main__":
    main()
