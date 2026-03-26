import pandas as pd
import io
import docx
import chardet
from core.models.file_parse_result import FileParseResult
from core.services.file_type_service import FileTypeService

class FileParserService:
    """文件解析服务"""
    
    def parse_file(self, file_content: bytes, filename: str) -> FileParseResult:
        """解析文件内容
        
        Args:
            file_content: 文件内容字节
            filename: 文件名
            
        Returns:
            FileParseResult: 文件解析结果
        """
        # 检测文件类型
        file_type, _ = FileTypeService.get_file_type(filename)
        
        if file_type == 'excel':
            content = self._parse_excel(file_content)
        elif file_type == 'word':
            content = self._parse_word(file_content)
        elif file_type == 'txt':
            content = self._parse_text(file_content)
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")
        
        return FileParseResult(
            filename=filename,
            file_type=file_type,
            content=content,
            content_length=len(content)
        )
    
    def supports_file_type(self, filename: str) -> bool:
        """判断是否支持该文件类型
        
        Args:
            filename: 文件名
            
        Returns:
            bool: 是否支持
        """
        return FileTypeService.is_supported(filename)
    
    def _parse_excel(self, file_content: bytes) -> str:
        """解析Excel文件
        
        Args:
            file_content: 文件内容字节
            
        Returns:
            str: 解析后的文本内容
        """
        df = pd.read_excel(io.BytesIO(file_content), engine='openpyxl')
        # 将所有单元格内容转换为字符串并拼接
        content = ' '.join([' '.join(map(str, row)) for _, row in df.iterrows()])
        return content
    
    def _parse_word(self, file_content: bytes) -> str:
        """解析Word文件
        
        Args:
            file_content: 文件内容字节
            
        Returns:
            str: 解析后的文本内容
        """
        doc = docx.Document(io.BytesIO(file_content))
        content = ' '.join([para.text for para in doc.paragraphs])
        return content
    
    def _parse_text(self, file_content: bytes) -> str:
        """解析文本文件
        
        Args:
            file_content: 文件内容字节
            
        Returns:
            str: 解析后的文本内容
        """
        result = chardet.detect(file_content)
        encoding = result['encoding'] or 'utf-8'
        content = file_content.decode(encoding)
        return content
