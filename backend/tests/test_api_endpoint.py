import http.client

# 测试健康检查接口
try:
    conn = http.client.HTTPConnection("localhost", 8000)
    conn.request("GET", "/health")
    response = conn.getresponse()
    print(f"健康检查接口响应状态: {response.status}")
    data = response.read()
    print(f"响应内容: {data.decode()}")
    conn.close()
    print("✓ 健康检查接口测试通过！")
except Exception as e:
    print(f"✗ 健康检查接口测试失败: {str(e)}")

# 测试数据库检查接口
try:
    conn = http.client.HTTPConnection("localhost", 8000)
    conn.request("GET", "/db-check")
    response = conn.getresponse()
    print(f"\n数据库检查接口响应状态: {response.status}")
    data = response.read()
    print(f"响应内容: {data.decode()}")
    conn.close()
    print("✓ 数据库检查接口测试通过！")
except Exception as e:
    print(f"\n✗ 数据库检查接口测试失败: {str(e)}")
