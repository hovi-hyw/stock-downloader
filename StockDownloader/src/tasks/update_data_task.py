# src/tasks/update_data_task.py

import os
from datetime import date, datetime

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
from StockDownloader.src.utils.index_utils import get_index_trading_dates, get_stock_trading_dates


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
    today = date.today()
    end_date = today.strftime("%Y%m%d")
    
    # 创建数据库会话
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 如果是更新指数数据，使用常规方式更新
        if table_model == IndexDailyData:
            latest_date = get_latest_date_from_db(engine, table_model)
            
            if latest_date is None:
                start_date = "20040101"  # 如果数据库为空，从最早的时间开始
            else:
                start_date = latest_date.strftime("%Y%m%d")
                
            if start_date == end_date:
                logger.info(f"指数数据库已是最新，无需更新")
                return
                
            for _, row in symbol_list.iterrows():
                # 确保指数代码始终以字符串形式处理，并且保留前导零
                symbol = str(row[symbol_key]).strip()
                # 对于纯数字的指数代码，确保格式正确（如：000001而不是1）
                if symbol.isdigit() and len(symbol) < 6:
                    symbol = symbol.zfill(6)  # 补齐6位
                    
                try:
                    data = fetch_function(symbol, start_date, end_date)
                    # 检查返回的数据是否为None或空
                    if data is None or data.empty:
                        logger.warning(f"获取指数 {symbol} 的数据为空，跳过保存")
                        continue
                        
                    # 传递index_name参数
                    if '名称' in row:
                        save_function(data, symbol, row['名称'])
                    else:
                        save_function(data, symbol)
                    logger.info(f"指数 {symbol} 数据更新完成")
                except Exception as e:
                    logger.error(f"更新指数 {symbol} 数据出错: {e}")
        
        # 如果是更新股票数据，基于指数000001的交易日期进行全量比较
        else:
            # 获取指数000001的所有交易日期作为基准
            index_trading_dates = get_index_trading_dates(db, "000001")
            if not index_trading_dates:
                logger.error("无法获取指数000001的交易日期，请先更新指数数据")
                return
                
            logger.info(f"获取到指数000001的交易日期共 {len(index_trading_dates)} 个")
            
            # 遍历所有股票
            for _, row in symbol_list.iterrows():
                # 确保股票代码始终以字符串形式处理
                symbol = str(row[symbol_key]).strip()
                
                try:
                    # 获取该股票在数据库中已有的交易日期
                    stock_trading_dates = get_stock_trading_dates(db, symbol)
                    
                    # 计算缺失的交易日期
                    missing_dates = index_trading_dates - stock_trading_dates
                    
                    if not missing_dates:
                        logger.info(f"股票 {symbol} 数据已完整，无需更新")
                        continue
                        
                    logger.info(f"股票 {symbol} 缺失 {len(missing_dates)} 个交易日期的数据")
                    
                    # 按时间顺序排序缺失的日期
                    sorted_missing_dates = sorted(missing_dates)
                    
                    # 将缺失日期分组为连续的时间段，减少API调用次数
                    date_ranges = []
                    if sorted_missing_dates:
                        start = sorted_missing_dates[0]
                        end = start
                        
                        for i in range(1, len(sorted_missing_dates)):
                            current = sorted_missing_dates[i]
                            prev = sorted_missing_dates[i-1]
                            
                            # 如果日期连续（相差一天），则扩展当前范围
                            if (current - prev).days <= 7:  # 允许最多相差7天，减少API调用
                                end = current
                            else:
                                # 添加当前范围并开始新范围
                                date_ranges.append((start, end))
                                start = current
                                end = current
                        
                        # 添加最后一个范围
                        date_ranges.append((start, end))
                    
                    # 对每个日期范围获取数据
                    for start_date, end_date in date_ranges:
                        start_str = start_date.strftime("%Y%m%d")
                        end_str = end_date.strftime("%Y%m%d")
                        
                        logger.info(f"获取股票 {symbol} 从 {start_str} 到 {end_str} 的数据")
                        
                        try:
                            data = fetch_function(symbol, start_str, end_str)
                            
                            # 检查返回的数据是否为None或空
                            if data is None or data.empty:
                                logger.warning(f"获取股票 {symbol} 从 {start_str} 到 {end_str} 的数据为空，跳过保存")
                                continue
                                
                            save_function(data, symbol)
                            logger.info(f"股票 {symbol} 从 {start_str} 到 {end_str} 的数据更新完成")
                        except Exception as e:
                            logger.error(f"更新股票 {symbol} 从 {start_str} 到 {end_str} 的数据出错: {e}")
                            continue  # 继续处理下一个日期范围
                    
                    logger.info(f"股票 {symbol} 所有缺失数据更新完成")
                except Exception as e:
                    logger.error(f"更新股票 {symbol} 数据出错: {e}")
    finally:
        db.close()


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
    cache_dir = os.path.join(os.getcwd(), "cache")
    # 确保缓存目录存在
    from ..utils.file_utils import ensure_directory_exists
    ensure_directory_exists(cache_dir)
    stock_list_file = os.path.join(cache_dir, "stock_list.csv")
    
    # 直接检查文件是否存在，不再检查文件的有效期
    if os.path.exists(stock_list_file):
        logger.info("从缓存读取股票列表")
        stock_list = pd.read_csv(stock_list_file)
    else:
        logger.info("从API获取股票列表")
        stock_list = fetcher.fetch_stock_list()
        saver.save_stock_list_to_csv(stock_list, stock_list_file)
        
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
    cache_dir = os.path.join(os.getcwd(), "cache")
    # 确保缓存目录存在
    from ..utils.file_utils import ensure_directory_exists
    ensure_directory_exists(cache_dir)
    index_list_file = os.path.join(cache_dir, "index_list.csv")
    
    # 直接检查文件是否存在，不再检查文件的有效期
    if os.path.exists(index_list_file):
        logger.info("从缓存读取指数列表")
        index_list = pd.read_csv(index_list_file)
    else:
        logger.info("从东方财富获取指数列表")
        index_list = fetcher.fetch_index_list()
        saver.save_index_list_to_csv(index_list, index_list_file)
    
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
    cache_dir = os.path.join(os.getcwd(), "cache")
    # 确保缓存目录存在
    from ..utils.file_utils import ensure_directory_exists
    ensure_directory_exists(cache_dir)
    stock_list_file = os.path.join(cache_dir, "stock_list.csv")
    
    # 直接检查文件是否存在，不再检查文件的有效期
    if os.path.exists(stock_list_file):
        logger.info("从缓存读取股票列表")
        stock_list = pd.read_csv(stock_list_file)
    else:
        logger.info("从API获取股票列表")
        stock_list = fetcher.fetch_stock_list()
        saver.save_stock_list_to_csv(stock_list, stock_list_file)
        
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
    cache_dir = os.path.join(os.getcwd(), "cache")
    # 确保缓存目录存在
    from ..utils.file_utils import ensure_directory_exists
    ensure_directory_exists(cache_dir)
    index_list_file = os.path.join(cache_dir, "index_list.csv")
    
    # 直接检查文件是否存在，不再检查文件的有效期
    if os.path.exists(index_list_file):
        logger.info("从缓存读取指数列表")
        index_list = pd.read_csv(index_list_file)
    else:
        logger.info("从东方财富获取指数列表")
        index_list = fetcher.fetch_index_list()
        saver.save_index_list_to_csv(index_list, index_list_file)
        
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
    update_stock_data()