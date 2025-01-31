import pandas as pd
from datetime import datetime, timedelta
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.core.config import config
from src.core.logger import logger
from services.data_fetcher import DataFetcher

def main():
    fetcher = DataFetcher()
    saver = DataSaver()

    # 获取股票和指数列表
    stock_list = fetcher.fetch_stock_list()
    index_list = fetcher.fetch_index_list()

    # 保存股票和指数列表到 CSV
    saver.save_stock_list_to_csv(stock_list, config.STOCK_LIST_CSV)
    saver.save_index_list_to_csv(index_list, config.INDEX_LIST_CSV)

    # 获取过去 100 天的日期
    start_date = fetcher.get_last_n_days(config.DATA_UPDATE_INTERVAL)

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