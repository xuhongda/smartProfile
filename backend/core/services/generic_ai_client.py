import httpx
import json
from core.utils.config import config
from typing import Dict, Any, List, Optional

class GenericAIClient:
    """通用AI连接器"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(GenericAIClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化通用AI连接器"""
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.api_base_url = config.get("ai_service.api_base_url")
        self.api_key = config.get("ai_service.api_key")
        self.embedding_model = config.get("ai_service.embedding_model")
        self.chat_model = config.get("ai_service.chat_model")
        self.timeout = config.get("ai_service.timeout")
        
        # 创建HTTP客户端
        self.client = httpx.Client(timeout=httpx.Timeout(self.timeout))
        
        self._initialized = True
    
    def is_configured(self) -> bool:
        """检查AI服务是否配置
        
        Returns:
            bool: 是否配置了AI服务
        """
        return bool(self.api_base_url)
    
    def update_config(self):
        """更新配置"""
        self.api_base_url = config.get("ai_service.api_base_url")
        self.api_key = config.get("ai_service.api_key")
        self.embedding_model = config.get("ai_service.embedding_model")
        self.chat_model = config.get("ai_service.chat_model")
        self.timeout = config.get("ai_service.timeout")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头
        
        Returns:
            Dict[str, str]: 请求头
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def create_embedding(self, text: str) -> Optional[List[float]]:
        """创建文本嵌入
        
        Args:
            text: 要嵌入的文本
            
        Returns:
            List[float]: 嵌入向量，如果失败则返回None
        """
        if not self.is_configured():
            return None
        
        try:
            url = f"{self.api_base_url.rstrip('/')}/embeddings"
            payload = {
                "model": self.embedding_model,
                "input": text
            }
            
            response = self.client.post(
                url,
                headers=self._get_headers(),
                json=payload
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data and "data" in data and len(data["data"]) > 0:
                return data["data"][0]["embedding"]
            
            return None
        except httpx.ConnectError:
            print("AI服务连接拒绝，请检查服务地址是否正确")
            return None
        except httpx.TimeoutException:
            print("AI服务请求超时，请检查服务是否正常运行")
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                print("AI服务认证失败，请检查API密钥是否正确")
            else:
                print(f"AI服务返回错误: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"创建嵌入失败: {str(e)}")
            return None
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """聊天完成
        
        Args:
            messages: 消息列表
            
        Returns:
            str: 聊天响应，如果失败则返回None
        """
        if not self.is_configured():
            return None
        
        try:
            url = f"{self.api_base_url.rstrip('/')}/chat/completions"
            payload = {
                "model": self.chat_model,
                "messages": messages
            }
            
            response = self.client.post(
                url,
                headers=self._get_headers(),
                json=payload
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data and "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            
            return None
        except httpx.ConnectError:
            print("AI服务连接拒绝，请检查服务地址是否正确")
            return None
        except httpx.TimeoutException:
            print("AI服务请求超时，请检查服务是否正常运行")
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                print("AI服务认证失败，请检查API密钥是否正确")
            else:
                print(f"AI服务返回错误: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"聊天完成失败: {str(e)}")
            return None
    
    def close(self):
        """关闭HTTP客户端"""
        if hasattr(self, 'client'):
            self.client.close()

# 创建全局通用AI客户端实例
generic_ai_client = GenericAIClient()