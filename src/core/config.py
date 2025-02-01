import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = os.getenv("LOG_FILE", "stock_insight.log")

    # AkShare API 配置
    AKSHARE_API_KEY = os.getenv("AKSHARE_API_KEY", "")

    # 列表更新频率
    MAX_CSV_AGE_DAYS = int(os.getenv("MAX_CSV_AGE_DAYS", 100))

    # 数据更新频率（天）
    DATA_UPDATE_INTERVAL = int(os.getenv("DATA_UPDATE_INTERVAL", 100))

    # CSV 文件路径
    CACHE_PATH = os.getenv("CACHE_PATH", "")
    STOCK_LIST_CSV = os.getenv("STOCK_LIST_CSV", "")
    INDEX_LIST_CSV = os.getenv("INDEX_LIST_CSV", "")

# 实例化配置对象
config = Config()