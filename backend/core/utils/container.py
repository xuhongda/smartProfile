class Container:
    """依赖注入容器"""
    
    def __init__(self):
        self._services = {}
    
    def register(self, name, instance):
        """注册服务
        
        Args:
            name: 服务名称
            instance: 服务实例
        """
        self._services[name] = instance
    
    def resolve(self, name):
        """解析服务
        
        Args:
            name: 服务名称
            
        Returns:
            服务实例
        """
        if name not in self._services:
            raise ValueError(f"服务未注册: {name}")
        return self._services[name]
    
    def get_all(self):
        """获取所有服务
        
        Returns:
            dict: 所有服务
        """
        return self._services
    
    def has(self, name):
        """检查服务是否存在
        
        Args:
            name: 服务名称
            
        Returns:
            bool: 是否存在
        """
        return name in self._services
