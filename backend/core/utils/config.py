import os
import json
from typing import Dict, Any

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = None):
        self.config = {
            # 数据库配置
            "database": {
                "url": os.getenv("DATABASE_URL", "sqlite:///data/unstructured_data.db"),
                "echo": os.getenv("DATABASE_ECHO", "true").lower() == "true"
            },
            # 向量搜索配置
            "vector_search": {
                "chroma_path": os.getenv("CHROMA_PATH", "data/chroma_db"),
                "top_k": int(os.getenv("TOP_K", "10")),
                "chunk_size": int(os.getenv("CHUNK_SIZE", "1000"))
            },
            # AI服务配置
            "ai_service": {
                "api_base_url": os.getenv("AI_API_BASE_URL", ""),
                "api_key": os.getenv("AI_API_KEY", ""),
                "embedding_model": os.getenv("AI_EMBEDDING_MODEL", "text-embedding-3-small"),
                "chat_model": os.getenv("AI_CHAT_MODEL", "gpt-3.5-turbo"),
                "timeout": int(os.getenv("AI_TIMEOUT", "5"))
            },
            # 上传配置
            "upload": {
                "directory": os.getenv("UPLOAD_DIR", "uploads"),
                "max_size": int(os.getenv("MAX_UPLOAD_SIZE", "20971520"))  # 20MB
            },
            # API配置
            "api": {
                "title": os.getenv("API_TITLE", "Unstructured Data Search API"),
                "description": os.getenv("API_DESCRIPTION", "非结构化数据检索系统的后端 API 服务"),
                "version": os.getenv("API_VERSION", "1.0.0")
            },
            # CORS配置
            "cors": {
                "allow_origins": os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
            }
        }
        
        # 加载配置文件
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
    
    def _load_config_file(self, config_file: str):
        """加载配置文件
        
        Args:
            config_file: 配置文件路径
        """
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                # 深度合并配置
                self._deep_update(self.config, file_config)
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}")
    
    def _deep_update(self, target: Dict[str, Any], source: Dict[str, Any]):
        """深度更新配置
        
        Args:
            target: 目标配置
            source: 源配置
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，支持点分隔，如 "database.url"
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值
        
        Args:
            key: 配置键，支持点分隔，如 "database.url"
            value: 配置值
        """
        keys = key.split(".")
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        Returns:
            配置字典
        """
        return self.config

# 创建全局配置实例
config = Config()
