from sqlalchemy import inspect
from src.database.session import engine
from src.core.logger import logger
from scripts.init.init_db import init_database

def check_database_initialized():
    """检查数据库是否已经初始化"""
    inspector = inspect(engine)
    # 检查必要的表是否存在
    required_tables = {'concept_board', 'index_daily_data', 'stock_daily_data'}  # 根据实际表名调整
    existing_tables = set(inspector.get_table_names())
    return required_tables.issubset(existing_tables)

def initialize_database_if_needed():
    """检查数据库是否初始化，未初始化则进行初始化"""
    if not check_database_initialized():
        logger.info("数据库未初始化，开始初始化...")
        init_database()
    else:
        logger.info("数据库已初始化，跳过初始化步骤")

if __name__ == '__main__':
    # 示例用法
    initialize_database_if_needed()
    if check_database_initialized():
        print("数据库已初始化或初始化成功。")
    else:
        print("数据库初始化检查失败。")