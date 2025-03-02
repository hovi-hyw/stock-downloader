# src/tasks/download_index_task.py
"""
此模块定义了下载指数数据的后台任务。
使用Celery或其他任务队列，定期从AKShare获取指数日线数据，并保存到数据库。
Authors: hovi.hyw & AI
Date: 2024-07-03
"""

from datetime import datetime

import pandas as pd

from src.core.config import config
from src.core.logger import logger
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver


def format_index_code(symbol):
    """确保指数代码为6位数字格式"""
    return str(symbol).zfill(6)


def download_index_data(symbol: str, name: str):
    """
    下载指定指数的日线数据，并保存到数据库。

    Args:
        symbol (str): 指数代码。
        name (str): 指数名称
    """
    fetcher = DataFetcher()
    saver = DataSaver()
    formatted_symbol = format_index_code(symbol)
    try:
        index_data = fetcher.fetch_index_daily_data(
            formatted_symbol,
            "20040101",
            datetime.today().strftime("%Y%m%d")
        )
        if index_data is None:
            logger.warning(f"未能获取到指数 {formatted_symbol}({name}) 的数据")
            return
        saver.save_index_daily_data_to_db(index_data, formatted_symbol, name)
        logger.info(f"指数 {formatted_symbol}({name}) 日数据下载并保存完成")
    except Exception as e:
        logger.error(f"处理指数 {formatted_symbol}({name}) 时出错: {e}")


def download_all_index_data():
    """
    下载所有指数的日线数据，并保存到数据库。
    """
    fetcher = DataFetcher()
    saver = DataSaver()

    # 获取指数列表
    index_list_file = config.CACHE_PATH + "/index_list.csv"
    max_age = config.MAX_CSV_AGE_DAYS
    from src.utils.file_utils import check_file_validity
    if check_file_validity(index_list_file, max_age):
        logger.info("从缓存读取指数列表")
        index_list = pd.read_csv(index_list_file)
    else:
        logger.info("从东方财富获取指数列表")
        index_list = fetcher.fetch_index_list()
        saver.save_index_list_to_csv(index_list, index_list_file)

    # 下载指数日数据并保存到数据库
    for _, row in index_list.iterrows():
        symbol = row["代码"]
        name = row["名称"]
        download_index_data(symbol, name)

    logger.info("所有指数数据下载任务完成")