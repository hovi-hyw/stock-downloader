import os
import pandas as pd
from datetime import datetime
from sqlalchemy import inspect
from src.services.data_fetcher import DataFetcher
from src.database.session import engine
from src.services.data_saver import DataSaver
from src.core.config import config
from src.core.logger import logger
from scripts.init.init_db import init_database
import time

def check_database_initialized():
    """检查数据库是否已经初始化"""
    inspector = inspect(engine)
    # 检查必要的表是否存在
    required_tables = {'concept_board', 'index_daily_data', 'stock_daily_data'}  # 根据实际表名调整
    existing_tables = set(inspector.get_table_names())
    return required_tables.issubset(existing_tables)


def check_file_validity(file_path, max_age_days):
    """检查文件是否存在且在有效期内"""
    if not os.path.exists(file_path):
        return False

    file_mtime = os.path.getmtime(file_path)
    file_age_days = (time.time() - file_mtime) / (60 * 60 * 24)
    return file_age_days <= max_age_days


def main():
    # 检查数据库初始化状态
    if not check_database_initialized():
        logger.info("数据库未初始化，开始初始化...")
        init_database()
    else:
        logger.info("数据库已初始化，跳过初始化步骤")

    fetcher = DataFetcher()
    saver = DataSaver()

    # # 下载概念板块
    # # 1. 获取并保存概念板块列表
    # concept_list = fetcher.fetch_concept_board_list()
    # saver.save_concept_board_list_to_csv(concept_list, config.CACHE_PATH+"/concept_board_list.csv")
    #
    # # 2. 获取并保存每个概念板块的历史数据
    # for _, row in concept_list.iterrows():
    #     board_name = row['板块名称']
    #     board_code = row['板块代码']
    #
    #     try:
    #         hist_data = fetcher.fetch_concept_board_daily_data(board_name)
    #         if hist_data is not None:
    #             saver.save_concept_board_data_to_db(hist_data, board_name, board_code)
    #         time.sleep(0.5)  # 避免请求过快
    #     except Exception as e:
    #         logger.error(f"Error processing board {board_name}: {e}")
    #         continue


    # 获取股票列表
    if check_file_validity(config.STOCK_LIST_CSV, config.MAX_CSV_AGE_DAYS):
        logger.info("从缓存读取股票列表")
        stock_list = pd.read_csv(config.STOCK_LIST_CSV)
    else:
        logger.info("从API获取股票列表")
        stock_list = fetcher.fetch_stock_list()
        saver.save_stock_list_to_csv(stock_list, config.STOCK_LIST_CSV)

    # 获取指数列表
    if check_file_validity(config.INDEX_LIST_CSV, config.MAX_CSV_AGE_DAYS):
        logger.info("从缓存读取指数列表")
        index_list = pd.read_csv(config.INDEX_LIST_CSV)
    else:
        logger.info("从API获取指数列表")
        index_list = fetcher.fetch_index_list()
        saver.save_index_list_to_csv(index_list, config.INDEX_LIST_CSV)

    # 下载指数日数据并保存到数据库
    for symbol in index_list["代码"]:
        index_data = fetcher.fetch_index_daily_data(symbol, "19900101", datetime.today().strftime("%Y%m%d"))
        saver.save_index_daily_data_to_db(index_data, symbol)


    # 下载股票日数据并保存到数据库
    for symbol in stock_list["代码"]:
        stock_data = fetcher.fetch_stock_daily_data(symbol, "19900101", datetime.today().strftime("%Y%m%d"))
        saver.save_stock_daily_data_to_db(stock_data, symbol)


if __name__ == "__main__":
    main()