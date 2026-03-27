import httpx
import json
import os
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
        self.speech_model = config.get("ai_service.speech_model")
        self.chat_model = config.get("ai_service.chat_model")
        self.timeout = config.get("ai_service.timeout")
        
        # 创建HTTP客户端
        self.client = httpx.Client(timeout=httpx.Timeout(self.timeout))
        
        # 本地模型相关
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models')
        self.local_embedding_model = None
        self.local_speech_model = None
        self._load_local_model()
        self._load_local_speech_model()
        
        self._initialized = True
    
    def is_configured(self) -> bool:
        """检查AI服务是否配置
        
        Returns:
            bool: 是否配置了AI服务
        """
        return bool(self.api_base_url) or bool(self.local_embedding_model)
    
    def update_config(self):
        """更新配置"""
        self.api_base_url = config.get("ai_service.api_base_url")
        self.api_key = config.get("ai_service.api_key")
        self.embedding_model = config.get("ai_service.embedding_model")
        self.speech_model = config.get("ai_service.speech_model")
        self.chat_model = config.get("ai_service.chat_model")
        self.timeout = config.get("ai_service.timeout")
        
        # 重新加载本地模型
        self._load_local_model()
        self._load_local_speech_model()
    
    def _load_local_model(self):
        """加载本地模型"""
        try:
            if self.embedding_model:
                model_path = os.path.join(self.models_dir, self.embedding_model)
                if os.path.exists(model_path):
                    # 尝试加载本地模型
                    from transformers import AutoTokenizer, AutoModel
                    print(f"尝试加载本地模型: {self.embedding_model}")
                    self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                    self.local_embedding_model = AutoModel.from_pretrained(model_path)
                    print(f"本地模型加载成功: {self.embedding_model}")
                else:
                    print(f"本地模型路径不存在: {model_path}")
                    self.local_embedding_model = None
            else:
                self.local_embedding_model = None
        except Exception as e:
            print(f"加载本地模型失败: {str(e)}")
            self.local_embedding_model = None
    
    def _load_local_speech_model(self):
        """加载本地语音模型"""
        try:
            if self.speech_model:
                model_path = os.path.join(self.models_dir, self.speech_model)
                if os.path.exists(model_path):
                    # 尝试加载本地语音模型
                    print(f"尝试加载本地语音模型: {self.speech_model}")
                    # 这里假设使用 FunASR 模型
                    try:
                        from funasr import AutoModel
                        self.local_speech_model = AutoModel(model=model_path)
                        print(f"本地语音模型加载成功: {self.speech_model}")
                    except ImportError:
                        print("FunASR 库未安装，请安装 funasr 包")
                        self.local_speech_model = None
                else:
                    print(f"本地语音模型路径不存在: {model_path}")
                    self.local_speech_model = None
            else:
                self.local_speech_model = None
        except Exception as e:
            print(f"加载本地语音模型失败: {str(e)}")
            self.local_speech_model = None
    
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
        # 优先使用本地模型
        if self.local_embedding_model:
            try:
                import torch
                # 使用本地模型生成嵌入
                inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
                with torch.no_grad():
                    outputs = self.local_embedding_model(**inputs)
                # 获取CLS token的嵌入
                embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
                return embedding
            except Exception as e:
                print(f"本地模型生成嵌入失败: {str(e)}")
                # 本地模型失败，尝试使用API
        
        # 使用API生成嵌入
        if self.is_configured() and self.api_base_url:
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
    
    def generate_ai_response(self, query: str, search_results: List[Dict]) -> Optional[str]:
        """生成AI响应，基于搜索结果
        
        Args:
            query: 用户查询
            search_results: 搜索结果
            
        Returns:
            str: AI响应，如果失败则返回None
        """
        if not self.is_configured():
            return None
        
        # 构建上下文
        context = "搜索结果：\n"
        for result in search_results:
            context += f"- 文件名: {result.get('filename', '未知')}\n"
            context += f"  内容: {result.get('content', '无内容')[:200]}...\n\n"
        
        # 构建消息
        messages = [
            {
                "role": "system",
                "content": "你是一个智能助手，基于搜索结果回答用户的问题。请根据搜索结果提供准确的回答，不要编造信息。"
            },
            {
                "role": "user",
                "content": f"用户问题: {query}\n\n{context}"
            }
        ]
        
        # 记录提示词到本地日志
        self._log_prompt(messages, query)
        
        return self.chat_completion(messages)
    
    def _log_prompt(self, messages: List[Dict], query: str):
        """记录提示词到本地日志
        
        Args:
            messages: 发送给AI的消息
            query: 用户查询
        """
        import os
        import json
        from datetime import datetime
        
        # 创建日志目录
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # 日志文件路径
        log_file = os.path.join(log_dir, 'ai_prompts.log')
        
        # 构建日志内容
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "messages": messages
        }
        
        # 写入日志文件
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            print(f"提示词已记录到: {log_file}")
        except Exception as e:
            print(f"记录提示词失败: {str(e)}")
    
    def speech_recognition(self, audio_data: bytes) -> Optional[str]:
        """语音识别
        
        Args:
            audio_data: 音频数据
            
        Returns:
            str: 识别结果，如果失败则返回None
        """
        # 优先使用本地模型
        if self.local_speech_model:
            try:
                # 使用本地语音模型进行识别
                import tempfile
                import os
                
                # 创建临时音频文件
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                    f.write(audio_data)
                    temp_file = f.name
                
                # 调用模型进行识别
                result = self.local_speech_model(temp_file)
                
                # 清理临时文件
                os.unlink(temp_file)
                
                # 提取识别结果
                if result and len(result) > 0:
                    return result[0]['text']
                
                return None
            except Exception as e:
                print(f"本地语音模型识别失败: {str(e)}")
                # 本地模型失败，尝试使用API
        
        # 使用API进行语音识别
        if self.is_configured() and self.api_base_url:
            try:
                url = f"{self.api_base_url.rstrip('/')}/audio/transcriptions"
                
                # 构建表单数据
                import io
                from httpx import MultipartFile
                
                files = {
                    "file": ("audio.wav", io.BytesIO(audio_data), "audio/wav")
                }
                data = {
                    "model": self.speech_model
                }
                
                response = self.client.post(
                    url,
                    headers=self._get_headers(),
                    files=files,
                    data=data
                )
                
                response.raise_for_status()
                data = response.json()
                
                if data and "text" in data:
                    return data["text"]
                
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
                print(f"语音识别失败: {str(e)}")
                return None
        
        return None
    
    def close(self):
        """关闭HTTP客户端"""
        if hasattr(self, 'client'):
            self.client.close()

# 创建全局通用AI客户端实例
generic_ai_client = GenericAIClient()