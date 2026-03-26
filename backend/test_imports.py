#!/usr/bin/env python3
"""测试导入所有必要的模块"""

print("测试导入模块...")

# 测试核心模块
try:
    from core.services import container
    from core.services.generic_ai_client import GenericAIClient
    from core.services.vector_store import VectorStore
    from core.services.hybrid_search_service import HybridSearchService
    from core.services.ingestion_service import IngestionService
    print("✓ 核心服务模块导入成功")
except Exception as e:
    print(f"✗ 核心服务模块导入失败: {e}")

# 测试配置模块
try:
    from core.utils.config import config
    print("✓ 配置模块导入成功")
except Exception as e:
    print(f"✗ 配置模块导入失败: {e}")

# 测试数据库模块
try:
    from database import get_db, Document
    print("✓ 数据库模块导入成功")
except Exception as e:
    print(f"✗ 数据库模块导入失败: {e}")

# 测试FastAPI模块
try:
    from fastapi import FastAPI
    print("✓ FastAPI模块导入成功")
except Exception as e:
    print(f"✗ FastAPI模块导入失败: {e}")

# 测试HTTP客户端模块
try:
    import httpx
    print("✓ httpx模块导入成功")
except Exception as e:
    print(f"✗ httpx模块导入失败: {e}")

print("测试完成!")
