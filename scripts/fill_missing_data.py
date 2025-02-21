"""
根据index中的sh000001日期来补全stock股票集中缺失日期的数据
"""
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.core.config import config
from src.core.logger import logger

# 创建数据库引擎和会话
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_missing_dates(stock_symbol, reference_dates):
    """
    获取股票缺失的交易日期。

    :param stock_symbol: 股票代码
    :param reference_dates: 基准交易日期列表（DataFrame 格式）
    :return: 缺失日期列表
    """
    query = f"""
        SELECT date 
        FROM stock_daily_data 
        WHERE symbol = '{stock_symbol}' AND date >= '20240101';
    """
    with engine.connect() as connection:
        stock_dates = pd.read_sql(query, connection)

    # 转换为集合并找出缺失日期
    stock_date_set = set(stock_dates["date"].tolist())
    reference_date_set = set(reference_dates["date"].tolist())
    missing_dates = sorted(reference_date_set - stock_date_set)

    return missing_dates

def fill_missing_data():
    """
    检查数据库中股票的日线数据是否有缺失，并补充缺失数据。
    """
    # 初始化服务类
    fetcher = DataFetcher()
    saver = DataSaver()

    # 获取基准交易日期（symbol=sh000001，上证指数）
    logger.info("获取基准交易日期...")
    query = """
        SELECT date 
        FROM index_daily_data 
        WHERE symbol = 'sh000001' AND date >= '20240101';
    """
    with engine.connect() as connection:
        reference_dates = pd.read_sql(query, connection)

    if reference_dates.empty:
        logger.error("未找到任何基准交易日期数据，请检查数据库中的 index_daily_data 表！")
        return

    # 获取股票列表
    logger.info("获取股票列表...")
    with engine.connect() as connection:
        stock_list = pd.read_sql("SELECT DISTINCT symbol FROM stock_daily_data;", connection)

    if stock_list.empty:
        logger.error("未找到任何股票数据，请检查数据库中的 stock_daily_data 表！")
        return

    # 遍历每只股票，检查缺失日期并补充数据
    for stock_symbol in stock_list["symbol"]:
        logger.info(f"检查股票 {stock_symbol} 的缺失数据...")
        missing_dates = get_missing_dates(stock_symbol, reference_dates)

        if not missing_dates:
            logger.info(f"股票 {stock_symbol} 数据完整，无需补充。")
            continue

        logger.info(f"股票 {stock_symbol} 缺失日期: {missing_dates}")

        # 下载并补充缺失数据
        for missing_date in missing_dates:
            try:
                logger.info(f"补充 {stock_symbol} 的数据，日期: {missing_date}...")
                stock_data = fetcher.fetch_stock_daily_data(stock_symbol, missing_date, missing_date)
                if stock_data is not None and not stock_data.empty:
                    saver.save_stock_daily_data_to_db(stock_data, stock_symbol)
                    logger.info(f"成功补充 {stock_symbol} 的数据，日期: {missing_date}")
                else:
                    logger.warning(f"未找到 {stock_symbol} 在 {missing_date} 的数据，跳过。")
            except Exception as e:
                logger.error(f"补充 {stock_symbol} 的数据时发生错误，日期: {missing_date}，错误信息: {e}")
                continue

    logger.info("缺失数据补充完成！")

if __name__ == "__main__":
    fill_missing_data()