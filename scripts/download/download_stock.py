from datetime import datetime

import pandas as pd

from src.core.config import config
from src.core.logger import logger
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.utils.db_utils import initialize_database_if_needed
from src.utils.file_utils import check_file_validity


def main():
    initialize_database_if_needed()  # 初始化数据库检查

    fetcher = DataFetcher()
    saver = DataSaver()

    # 获取股票列表
    if check_file_validity(config.CACHE_PATH + "/stock_list.csv", config.MAX_CSV_AGE_DAYS):
        logger.info("从缓存读取股票列表")
        stock_list = pd.read_csv(config.CACHE_PATH + "/stock_list.csv")
    else:
        logger.info("从API获取股票列表")
        stock_list = fetcher.fetch_stock_list()
        saver.save_stock_list_to_csv(stock_list, config.CACHE_PATH + "/stock_list.csv")

    # 下载股票日数据并保存到数据库
    for symbol in stock_list["代码"]:
        stock_data = fetcher.fetch_stock_daily_data(symbol, "20040101", datetime.today().strftime("%Y%m%d"), 'hfq')
        saver.save_stock_daily_data_to_db(stock_data, symbol)
        logger.info(f"股票 {symbol} 日数据下载并保存完成")

    logger.info("股票数据下载任务完成")


if __name__ == "__main__":
    main()
