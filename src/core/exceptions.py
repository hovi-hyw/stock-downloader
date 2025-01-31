class DataFetchError(Exception):
    """数据获取异常"""
    pass

class DataSaveError(Exception):
    """数据保存异常"""
    pass

class DatabaseError(Exception):
    """数据库操作异常"""
    pass

class ConfigError(Exception):
    """配置错误异常"""
    pass