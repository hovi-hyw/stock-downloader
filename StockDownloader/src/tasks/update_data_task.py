# src/tasks/update_data_task.py

import os
from datetime import date

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from StockDownloader.src.core.config import config
from StockDownloader.src.core.logger import logger
from StockDownloader.src.database.models.index import IndexDailyData
from StockDownloader.src.database.models.stock import StockDailyData
from StockDownloader.src.services.data_fetcher import DataFetcher
from StockDownloader.src.services.data_saver import DataSaver
from StockDownloader.src.utils.db_utils import initialize_database_if_needed


def get_latest_date_from_db(engine, table_model):
    """从数据库中获取最新的日期"""
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        latest_record = db.query(table_model).order_by(table_model.date.desc()).first()
        if latest_record:
            return latest_record.date
        else:
            return None
    finally:
        db.close()


def update_data(engine, fetcher, saver, table_model, fetch_function, save_function, symbol_list, symbol_key):
    """更新数据"""
    latest_date = get_latest_date_from_db(engine, table_model)
    today = date.today()

    if latest_date is None:
        start_date = "20040101"  # 如果数据库为空，从最早的时间开始
    else:
        start_date = latest_date.strftime("%Y%m%d")

    end_date = today.strftime("%Y%m%d")

    if start_date == end_date:
        logger.info(f"数据库已是最新，无需更新")
        return

    for symbol in symbol_list[symbol_key]:
        try:
            data = fetch_function(symbol, start_date, end_date)
            save_function(data, symbol)
            logger.info(f"{symbol} 数据更新完成")
        except Exception as e:
            logger.error(f"更新 {symbol} 数据出错: {e}")


def update_stock_data():
    """只更新股票数据"""
    initialize_database_if_needed()
    # 确保 DATABASE_URL 不为空，否则抛出异常
    if config.DATABASE_URL is None:
        raise ValueError("数据库连接URL不能为空")
    engine = create_engine(str(config.DATABASE_URL))
    fetcher = DataFetcher()
    saver = DataSaver()

    # 更新股票数据
    stock_list_file = os.path.join(os.getcwd(), "cache", "stock_list.csv")
    stock_list = pd.read_csv(stock_list_file)
    update_data(
        engine,
        fetcher,
        saver,
        StockDailyData,
        fetcher.fetch_stock_daily_data,
        saver.save_stock_daily_data_to_db,
        stock_list,
        "代码"
    )
    
    logger.info("股票数据更新任务完成")


def update_index_data():
    """只更新指数数据"""
    initialize_database_if_needed()
    # 确保 DATABASE_URL 不为空，否则抛出异常
    if config.DATABASE_URL is None:
        raise ValueError("数据库连接URL不能为空")
    engine = create_engine(str(config.DATABASE_URL))
    fetcher = DataFetcher()
    saver = DataSaver()

    # 更新指数数据
    index_list_file = os.path.join(os.getcwd(), "cache", "index_list.csv")
    index_list = pd.read_csv(index_list_file)
    update_data(
        engine,
        fetcher,
        saver,
        IndexDailyData,
        fetcher.fetch_index_daily_data,
        saver.save_index_daily_data_to_db,
        index_list,
        "代码"
    )
    
    logger.info("指数数据更新任务完成")


def update_all_data():
    initialize_database_if_needed()
    # 确保 DATABASE_URL 不为空，否则抛出异常
    if config.DATABASE_URL is None:
        raise ValueError("数据库连接URL不能为空")
    engine = create_engine(str(config.DATABASE_URL))
    fetcher = DataFetcher()
    saver = DataSaver()

    # 更新股票数据
    stock_list_file = os.path.join(os.getcwd(), "cache", "stock_list.csv")
    stock_list = pd.read_csv(stock_list_file)
    update_data(
        engine,
        fetcher,
        saver,
        StockDailyData,
        fetcher.fetch_stock_daily_data,
        saver.save_stock_daily_data_to_db,
        stock_list,
        "代码"
    )

    # 更新指数数据
    index_list_file = os.path.join(os.getcwd(), "cache", "index_list.csv")
    index_list = pd.read_csv(index_list_file)
    update_data(
        engine,
        fetcher,
        saver,
        IndexDailyData,
        fetcher.fetch_index_daily_data,
        saver.save_index_daily_data_to_db,
        index_list,
        "代码"
    )

    logger.info("所有数据更新任务完成")


if __name__ == "__main__":
    update_all_data()