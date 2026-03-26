import os
import subprocess
import json
from typing import Dict, List, Optional

import threading

class ModelManagerService:
    """模型管理服务"""
    
    def __init__(self, config):
        self.config = config
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models')
        self._current_model = None
        self._model_loading_status = {"status": "idle", "progress": 0, "message": ""}
        self._lock = threading.Lock()  # 用于线程安全
        
    def download_model(self, command: str) -> Dict:
        """下载模型
        
        Args:
            command: ModelScope 下载命令
            
        Returns:
            Dict: 下载结果，包含状态、消息、进度等
        """
        try:
            # 解析命令，提取模型名称
            model_name = self._parse_model_name(command)
            if not model_name:
                return {
                    "success": False,
                    "message": "无效的模型下载命令",
                    "error": "无法解析模型名称"
                }
            
            # 创建模型文件夹
            model_dir = os.path.join(self.models_dir, model_name.replace('/', '_'))
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            
            # 构建下载命令
            download_cmd = [
                "modelscope", "download",
                model_name,
                "--local_dir", model_dir
            ]
            
            # 执行下载命令
            process = subprocess.Popen(
                download_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 读取输出，捕获进度
            output = []
            error_output = []
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    output.append(line.strip())
                    # 这里可以解析进度信息
            
            # 读取错误输出
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                error_output.append(line.strip())
            
            # 检查执行结果
            if process.returncode == 0:
                return {
                    "success": True,
                    "message": f"模型 {model_name} 下载成功",
                    "model_name": model_name,
                    "output": output
                }
            else:
                return {
                    "success": False,
                    "message": f"模型 {model_name} 下载失败",
                    "error": '\n'.join(error_output),
                    "output": output
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": "下载模型时发生错误",
                "error": str(e)
            }
    
    async def upload_model(self, files) -> Dict:
        """上传模型
        
        Args:
            files: 上传的模型文件列表
        
        Returns:
            Dict: 上传结果，包含状态、消息等
        """
        try:
            # 检查是否有文件
            if not files or len(files) == 0:
                return {
                    "success": False,
                    "message": "请选择要上传的模型文件夹",
                    "error": "没有选择文件"
                }
            
            # 提取文件夹名称（假设第一个文件的路径格式为 "folder/file.txt"）
            import os
            first_file_name = files[0].filename
            if not first_file_name:
                return {
                    "success": False,
                    "message": "无效的模型文件",
                    "error": "无法获取模型名称"
                }
            
            folder_name = os.path.dirname(first_file_name)
            if not folder_name:
                # 如果没有文件夹路径，使用当前时间戳作为文件夹名
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                folder_name = f"model_{timestamp}"
            
            # 创建模型文件夹
            model_dir = os.path.join(self.models_dir, folder_name)
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            
            # 保存所有文件
            uploaded_files = []
            for file in files:
                # 获取文件名
                file_name = file.filename
                if not file_name:
                    continue
                
                # 保存文件
                # 提取相对路径（去掉文件夹名）
                relative_path = os.path.relpath(file_name, folder_name)
                file_path = os.path.join(model_dir, relative_path)
                # 确保目录存在
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                contents = await file.read()
                with open(file_path, "wb") as f:
                    f.write(contents)
                
                uploaded_files.append(relative_path)
            
            if not uploaded_files:
                return {
                    "success": False,
                    "message": "没有成功上传的文件",
                    "error": "文件上传失败"
                }
            
            return {
                "success": True,
                "message": f"模型 {folder_name} 上传成功，共上传 {len(uploaded_files)} 个文件",
                "model_name": folder_name,
                "uploaded_files": uploaded_files
            }
        except Exception as e:
            return {
                "success": False,
                "message": "上传模型时发生错误",
                "error": str(e)
            }
    
    def get_models(self) -> List[Dict]:
        """获取模型列表
        
        Returns:
            List[Dict]: 模型列表
        """
        models = []
        try:
            if os.path.exists(self.models_dir):
                # 查找子文件夹
                for model_dir in os.listdir(self.models_dir):
                    model_path = os.path.join(self.models_dir, model_dir)
                    if os.path.isdir(model_path) and not model_dir.startswith('.'):
                        # 递归查找模型文件
                        for root, dirs, files in os.walk(model_path):
                            # 检查是否存在模型文件
                            model_files = [f for f in files if f in ["config.json", "model.safetensors", "pytorch_model.bin"]]
                            if model_files:
                                # 还原模型名称（将 _ 替换回 /）
                                model_name = model_dir.replace('_', '/')
                                models.append({
                                    "name": model_name,
                                    "path": root,
                                    "size": self._get_dir_size(root)
                                })
                                break  # 找到一个模型就停止查找
        except Exception as e:
            print(f"获取模型列表失败: {e}")
        return models
    
    def _parse_model_name(self, command: str) -> Optional[str]:
        """解析模型名称
        
        Args:
            command: 下载命令
            
        Returns:
            Optional[str]: 模型名称
        """
        # 简单解析命令，提取 --model 参数的值
        parts = command.split()
        try:
            model_index = parts.index('--model') + 1
            return parts[model_index]
        except (ValueError, IndexError):
            return None
    
    def delete_model(self, model_name: str) -> Dict:
        """删除模型
        
        Args:
            model_name: 模型名称
        
        Returns:
            Dict: 删除结果，包含状态、消息等
        """
        try:
            # 创建模型文件夹路径
            model_dir = os.path.join(self.models_dir, model_name.replace('/', '_'))
            
            # 检查模型文件夹是否存在
            if not os.path.exists(model_dir):
                return {
                    "success": False,
                    "message": "模型不存在",
                    "error": f"模型 {model_name} 不存在"
                }
            
            # 删除模型文件夹及其内容
            import shutil
            shutil.rmtree(model_dir)
            
            return {
                "success": True,
                "message": f"模型 {model_name} 删除成功"
            }
        except Exception as e:
            return {
                "success": False,
                "message": "删除模型时发生错误",
                "error": str(e)
            }

    def load_model(self, model_name: str) -> Dict:
        """加载模型
        
        Args:
            model_name: 模型名称
        
        Returns:
            Dict: 加载结果，包含状态、消息等
        """
        try:
            # 更新加载状态
            with self._lock:
                self._model_loading_status = {
                    "status": "loading",
                    "progress": 0,
                    "message": f"开始加载模型 {model_name}"
                }
            
            # 创建模型文件夹路径
            model_dir = os.path.join(self.models_dir, model_name.replace('/', '_'))
            
            # 检查模型文件夹是否存在
            if not os.path.exists(model_dir):
                with self._lock:
                    self._model_loading_status = {
                        "status": "error",
                        "progress": 0,
                        "message": f"模型 {model_name} 不存在"
                    }
                return {
                    "success": False,
                    "message": "模型不存在",
                    "error": f"模型 {model_name} 不存在"
                }
            
            # 检查模型文件是否存在
            model_files = []
            for root, dirs, files in os.walk(model_dir):
                model_files.extend([f for f in files if f in ["config.json", "model.safetensors", "pytorch_model.bin"]])
            
            if not model_files:
                with self._lock:
                    self._model_loading_status = {
                        "status": "error",
                        "progress": 0,
                        "message": f"模型 {model_name} 缺少必要的模型文件"
                    }
                return {
                    "success": False,
                    "message": "模型文件不完整",
                    "error": f"模型 {model_name} 缺少必要的模型文件"
                }
            
            # 更新加载进度
            with self._lock:
                self._model_loading_status["progress"] = 30
                self._model_loading_status["message"] = f"正在验证模型文件..."
            
            # 这里实现模型加载逻辑
            # 由于不同模型的加载方式不同，这里只做简单的验证
            # 实际项目中，需要根据模型类型选择不同的加载方式
            
            # 模拟模型加载过程
            import time
            time.sleep(2)  # 模拟加载时间
            
            # 更新加载进度
            with self._lock:
                self._model_loading_status["progress"] = 70
                self._model_loading_status["message"] = f"正在初始化模型..."
            
            # 模拟初始化过程
            time.sleep(1)
            
            # 线程安全地更新当前模型
            with self._lock:
                # 保存旧模型引用，以便在加载失败时回滚
                old_model = self._current_model
                try:
                    # 这里应该是实际的模型加载代码
                    # 例如：self._current_model = load_model(model_dir)
                    self._current_model = model_name  # 暂时使用模型名称作为占位符
                    
                    # 更新配置，设置当前加载的模型
                    self.config.set("ai_service.embedding_model", model_name)
                    
                    # 启用 chromaDB 数据库相应功能
                    self.config.set("vector_store.enabled", True)
                    
                    # 更新加载状态
                    self._model_loading_status = {
                        "status": "success",
                        "progress": 100,
                        "message": f"模型 {model_name} 加载成功"
                    }
                    
                    return {
                        "success": True,
                        "message": f"模型 {model_name} 加载成功，已启用 chromaDB 数据库功能",
                        "model_name": model_name
                    }
                except Exception as e:
                    # 加载失败，回滚到旧模型
                    self._current_model = old_model
                    self._model_loading_status = {
                        "status": "error",
                        "progress": 0,
                        "message": f"模型加载失败: {str(e)}"
                    }
                    raise
        except Exception as e:
            # 确保在异常情况下，状态也被更新为 error
            with self._lock:
                self._model_loading_status = {
                    "status": "error",
                    "progress": 0,
                    "message": f"模型加载失败: {str(e)}"
                }
            return {
                "success": False,
                "message": "加载模型时发生错误",
                "error": str(e)
            }

    def get_model_status(self) -> Dict:
        """获取模型加载状态
        
        Returns:
            Dict: 模型加载状态，包含状态、进度和消息
        """
        with self._lock:
            return {
                "success": True,
                "status": self._model_loading_status,
                "current_model": self._current_model
            }

    def _get_dir_size(self, path: str) -> int:
        """获取目录大小
        
        Args:
            path: 目录路径
            
        Returns:
            int: 目录大小（字节）
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
        except Exception:
            pass
        return total_size
