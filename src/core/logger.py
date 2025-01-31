import logging
import os
from .config import config

# 创建日志目录
os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)

# 配置日志
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

# 获取日志对象
logger = logging.getLogger("stock_insight")