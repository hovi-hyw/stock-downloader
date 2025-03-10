# src/tasks/download_stock_task.py
"""
此模块定义了下载股票数据的后台任务。
使用Celery或其他任务队列，定期从AKShare获取股票日线数据，并保存到数据库。
Authors: hovi.hyw & AI
Date: 2024-07-03
"""

from datetime import datetime

import pandas as pd

from ..core.config import config
from ..core.logger import logger
from ..services.data_fetcher import DataFetcher
from ..services.data_saver import DataSaver


def download_stock_task(symbol: str):
    """
    下载指定股票的日线数据，并保存到数据库。

    Args:
        symbol (str): 股票代码。
    """
    fetcher = DataFetcher()
    saver = DataSaver()

    try:
        stock_data = fetcher.fetch_stock_daily_data(symbol, config.START_DATE, datetime.today().strftime("%Y%m%d"), 'hfq')
        if stock_data is not None and not stock_data.empty:
            saver.save_stock_daily_data_to_db(stock_data, symbol)
            logger.info(f"股票 {symbol} 日数据下载并保存完成")
        else:
            logger.warning(f"未能获取到股票 {symbol} 的数据")
    except Exception as e:
        logger.error(f"下载股票 {symbol} 数据时出错: {e}")


def download_all_stock_data():
    """
    下载所有股票的日线数据，并保存到数据库。
    """
    fetcher = DataFetcher()
    saver = DataSaver()
    # 获取股票列表
    stock_list_file = config.CACHE_PATH + "/stock_list.csv"
    max_age = config.MAX_CSV_AGE_DAYS
    from ..utils.file_utils import check_file_validity
    if check_file_validity(stock_list_file, max_age):
        logger.info("从缓存读取股票列表")
        stock_list = pd.read_csv(stock_list_file)
    else:
        logger.info("从API获取股票列表")
        stock_list = fetcher.fetch_stock_list()
        saver.save_stock_list_to_csv(stock_list, stock_list_file)

    # 下载股票日数据并保存到数据库
    for symbol in stock_list["代码"]:
        download_stock_task(symbol)
    logger.info("所有股票数据下载任务完成")