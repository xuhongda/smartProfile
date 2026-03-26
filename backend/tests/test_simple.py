import http.client
import json

# 测试健康检查接口
try:
    conn = http.client.HTTPConnection("localhost", 8000)
    conn.request("GET", "/health")
    response = conn.getresponse()
    print(f"健康检查接口响应: {response.status}")
    data = response.read()
    print(f"响应内容: {data.decode()}")
    conn.close()
except Exception as e:
    print(f"健康检查接口测试失败: {str(e)}")

# 测试数据库检查接口
try:
    conn = http.client.HTTPConnection("localhost", 8000)
    conn.request("GET", "/db-check")
    response = conn.getresponse()
    print(f"数据库检查接口响应: {response.status}")
    data = response.read()
    print(f"响应内容: {data.decode()}")
    conn.close()
except Exception as e:
    print(f"数据库检查接口测试失败: {str(e)}")
