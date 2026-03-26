from typing import Any

class APIResponse:
    """API响应模型"""
    
    def __init__(self, success: bool, message: str, data: Any = None):
        self.success = success
        self.message = message
        self.data = data
    
    def to_dict(self):
        """转换为字典"""
        response = {
            "success": self.success,
            "message": self.message
        }
        if self.data is not None:
            # 如果data是对象且有to_dict方法，调用它
            if hasattr(self.data, 'to_dict'):
                response["data"] = self.data.to_dict()
            # 如果data是列表，递归处理每个元素
            elif isinstance(self.data, list):
                response["data"] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in self.data]
            else:
                response["data"] = self.data
        return response
