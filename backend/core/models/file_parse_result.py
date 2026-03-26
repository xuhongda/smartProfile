class FileParseResult:
    """文件解析结果模型"""
    
    def __init__(self, filename: str, file_type: str, content: str, content_length: int):
        self.filename = filename
        self.file_type = file_type
        self.content = content
        self.content_length = content_length
    
    def to_dict(self):
        """转换为字典"""
        return {
            "filename": self.filename,
            "file_type": self.file_type,
            "content": self.content,
            "content_length": self.content_length
        }
