from typing import Dict, List, Optional, Tuple

class FileTypeService:
    """文件类型识别服务"""
    
    # 文件类型映射表
    FILE_TYPE_MAPPING = {
        # 文档类型
        'excel': {
            'extensions': ['xlsx', 'xls', 'csv'],
            'name': 'Excel',
            'category': 'document',
            'icon': 'file-excel'
        },
        'word': {
            'extensions': ['docx', 'doc'],
            'name': 'Word',
            'category': 'document',
            'icon': 'file-word'
        },
        'pdf': {
            'extensions': ['pdf'],
            'name': 'PDF',
            'category': 'document',
            'icon': 'file-pdf'
        },
        'txt': {
            'extensions': ['txt', 'md', 'markdown'],
            'name': '文本',
            'category': 'document',
            'icon': 'file-text'
        },
        'ppt': {
            'extensions': ['pptx', 'ppt'],
            'name': 'PowerPoint',
            'category': 'document',
            'icon': 'file-ppt'
        },
        # 图片类型
        'image': {
            'extensions': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'],
            'name': '图片',
            'category': 'image',
            'icon': 'file-image'
        },
        # 视频类型
        'video': {
            'extensions': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
            'name': '视频',
            'category': 'video',
            'icon': 'file-video'
        },
        # 音频类型
        'audio': {
            'extensions': ['mp3', 'wav', 'ogg', 'flac', 'aac'],
            'name': '音频',
            'category': 'audio',
            'icon': 'file-audio'
        },
        # 压缩文件
        'archive': {
            'extensions': ['zip', 'rar', '7z', 'tar', 'gz'],
            'name': '压缩文件',
            'category': 'archive',
            'icon': 'file-archive'
        },
        # 代码文件
        'code': {
            'extensions': ['py', 'js', 'ts', 'html', 'css', 'java', 'c', 'cpp', 'go', 'php'],
            'name': '代码',
            'category': 'code',
            'icon': 'file-code'
        }
    }
    
    @classmethod
    def get_file_type(cls, filename: str) -> Tuple[str, Dict]:
        """获取文件类型信息
        
        Args:
            filename: 文件名
            
        Returns:
            Tuple[str, Dict]: (文件类型标识, 文件类型信息)
        """
        if not filename:
            return 'unknown', {'name': '未知', 'category': 'unknown', 'icon': 'file-unknown'}
        
        # 获取文件扩展名
        file_ext = filename.split('.')[-1].lower() if '.' in filename else ''
        
        # 查找文件类型
        for file_type, info in cls.FILE_TYPE_MAPPING.items():
            if file_ext in info['extensions']:
                return file_type, info
        
        # 未知文件类型
        return 'unknown', {'name': '未知', 'category': 'unknown', 'icon': 'file-unknown'}
    
    @classmethod
    def is_supported(cls, filename: str) -> bool:
        """判断文件类型是否支持
        
        Args:
            filename: 文件名
            
        Returns:
            bool: 是否支持
        """
        file_type, _ = cls.get_file_type(filename)
        return file_type in ['excel', 'word', 'txt']  # 目前只支持这三种文件的解析
    
    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """获取支持的文件扩展名列表
        
        Returns:
            List[str]: 支持的文件扩展名列表
        """
        extensions = []
        for info in cls.FILE_TYPE_MAPPING.values():
            extensions.extend(info['extensions'])
        return extensions
    
    @classmethod
    def get_extension_by_file_type(cls, file_type: str) -> List[str]:
        """根据文件类型获取扩展名列表
        
        Args:
            file_type: 文件类型标识
            
        Returns:
            List[str]: 扩展名列表
        """
        info = cls.FILE_TYPE_MAPPING.get(file_type, {})
        return info.get('extensions', [])
    
    @classmethod
    def get_category_by_file_type(cls, file_type: str) -> str:
        """根据文件类型获取分类
        
        Args:
            file_type: 文件类型标识
            
        Returns:
            str: 分类名称
        """
        info = cls.FILE_TYPE_MAPPING.get(file_type, {})
        return info.get('category', 'unknown')
    
    @classmethod
    def get_icon_by_file_type(cls, file_type: str) -> str:
        """根据文件类型获取图标
        
        Args:
            file_type: 文件类型标识
            
        Returns:
            str: 图标名称
        """
        info = cls.FILE_TYPE_MAPPING.get(file_type, {})
        return info.get('icon', 'file-unknown')
