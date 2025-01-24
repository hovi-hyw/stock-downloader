# config/settings.py

import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置（从环境变量读取敏感信息）
DATABASE = {
    'dbname': os.getenv('DB_NAME', 'stock_daily'),
    'user': os.getenv('DB_USER', ''),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432))
}

# 构建 SQLAlchemy 数据库 URL
DATABASE_URL = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['dbname']}"

#
STOCK_LIST_CACHE = f"Config/stock_list.csv"
LOG_DIR = "logs"

MAX_WORKERS = int(os.getenv('MAX_WORKERS', 4))
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))
API_RETRY_COUNT = int(os.getenv('API_RETRY_COUNT', 3))
API_RETRY_DELAY = int(os.getenv('API_RETRY_DELAY', 1))
API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 1))

DEFAULT_START_DATE = "19900101"
DEFAULT_END_DATE = datetime.now().strftime('%Y%m%d')
