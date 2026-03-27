import os
import subprocess
import json
from typing import Dict, List, Optional

class ModelManagerService:
    """模型管理服务"""
    
    def __init__(self, config):
        self.config = config
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models')
        # 确保模型目录存在
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
        
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
                            model_files = [f for f in files if f in ["config.json", "model.safetensors", "pytorch_model.bin", "model.onnx"]]
                            if model_files:
                                # 直接使用文件夹名作为模型名称
                                model_name = model_dir
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
            model_dir = os.path.join(self.models_dir, model_name)
            
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
