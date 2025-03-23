import inspect
import logging
import os
from datetime import datetime

from .config import config


def get_caller_name():
    # 获取调用栈
    frame = inspect.stack()[2]  # 向上查找2层，跳过get_logger和get_caller_name自身
    module = inspect.getmodule(frame[0])
    if module:
        # 获取文件名（不含扩展名）
        return os.path.splitext(os.path.basename(module.__file__))[0]
    return 'unknown'


def get_logger():
    caller_name = get_caller_name()
    # 使用更详细的日期格式，确保日志文件名主要基于运行日期
    date_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 修改日志文件名格式，以日期为主要部分，模块名为次要部分
    log_filename = f"log_{date_prefix}_{caller_name}.log"
    # 使用config.LOG_FILE中的目录，但文件名使用动态生成的
    log_filepath = os.path.join(os.path.dirname(config.LOG_FILE), log_filename)

    # 确保日志目录存在
    os.makedirs(os.path.dirname(log_filepath), exist_ok=True)

    # 创建或获取logger
    logger = logging.getLogger(caller_name)

    # 如果logger已经配置过handlers，直接返回
    if logger.handlers:
        return logger

    logger.setLevel(config.LOG_LEVEL)

    # 文件处理器
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(config.LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config.LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 为了保持与现有代码兼容
logger = get_logger()
