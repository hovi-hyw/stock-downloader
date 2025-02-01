import os
import pandas as pd
from datetime import datetime
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.core.config import config
from src.core.logger import logger
import time


def check_file_validity(file_path, max_age_days):
    """检查文件是否存在且在有效期内"""
    if not os.path.exists(file_path):
        return False

    file_mtime = os.path.getmtime(file_path)
    file_age_days = (time.time() - file_mtime) / (60 * 60 * 24)
    return file_age_days <= max_age_days


def main():
    fetcher = DataFetcher()
    saver = DataSaver()

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


    # 下载股票日数据并保存到数据库
    for symbol in stock_list["代码"]:
        stock_data = fetcher.fetch_stock_daily_data(symbol, "19900101", datetime.today().strftime("%Y%m%d"))
        saver.save_stock_daily_data_to_db(stock_data, symbol)

    # 下载指数日数据并保存到数据库
    for symbol in index_list["代码"]:
        index_data = fetcher.fetch_index_daily_data(symbol, "19900101", datetime.today().strftime("%Y%m%d"))
        saver.save_index_daily_data_to_db(index_data, symbol)


if __name__ == "__main__":
    main()