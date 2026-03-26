import jieba

class ChineseTokenizer:
    """中文分词器，使用jieba库进行分词"""
    
    @staticmethod
    def tokenize_text(text):
        """对文本进行分词处理
        
        Args:
            text: 要分词的文本
            
        Returns:
            str: 分词后的文本，用空格连接
        """
        if not text:
            return ""
        
        # 使用jieba的搜索引擎模式进行分词
        words = jieba.cut_for_search(text)
        return " ".join(words)
    
    @staticmethod
    def tokenize_query(query):
        """对搜索查询进行分词处理
        
        Args:
            query: 搜索查询字符串
            
        Returns:
            str: 分词后的查询，用空格连接
        """
        if not query:
            return ""
        
        # 使用jieba的搜索引擎模式进行分词
        words = jieba.cut_for_search(query)
        return " ".join(words)
    
    @staticmethod
    def is_chinese(text):
        """判断文本是否包含中文字符
        
        Args:
            text: 要判断的文本
            
        Returns:
            bool: 是否包含中文字符
        """
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
