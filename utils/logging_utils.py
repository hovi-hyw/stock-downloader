import logging

class LoggingUtils:
    @staticmethod
    def configure_logging(log_file: str = None, level: int = logging.INFO):
        """
        配置日志记录器。

        Args:
            log_file (str): 日志文件路径。如果为 None，则仅输出到控制台。
            level (int): 日志级别，默认是 logging.INFO。
        """
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        handlers = [logging.StreamHandler()]

        if log_file:
            # 如果指定了日志文件，则添加文件日志处理器
            handlers.append(logging.FileHandler(log_file))

        logging.basicConfig(level=level, format=log_format, handlers=handlers)
        print(f"日志系统已配置，日志级别: {logging.getLevelName(level)}")

    @staticmethod
    def get_logger(name: str):
        """
        获取指定名称的日志记录器。

        Args:
            name (str): 日志记录器的名称。

        Returns:
            logging.Logger: 配置好的日志记录器。
        """
        return logging.getLogger(name)