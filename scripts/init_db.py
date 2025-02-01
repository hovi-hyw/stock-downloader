# scripts/init_db.py
from src.database.base import Base
from src.database.session import engine
from src.database.models import stock, index
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """初始化数据库，创建所有表"""
    try:
        logger.info("开始创建数据库表...")
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功！")
    except Exception as e:
        logger.error(f"创建数据库表时发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    init_database()