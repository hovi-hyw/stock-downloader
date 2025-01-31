# scripts/download_data.py
from services.data_fetcher import StockDataFetcher, IndexDataFetcher
from services.data_saver import StockDataSaver, IndexDataSaver
from core.logger import setup_logger
from core.config import settings
import asyncio
from datetime import datetime, timedelta

logger = setup_logger(__name__)

async def download_stock_data():
    """下载股票数据"""
    stock_fetcher = StockDataFetcher()
    stock_saver = StockDataSaver()
    
    try:
        # 获取股票列表
        stock_list = stock_fetcher.fetch_stock_list()
        logger.info(f"获取到 {len(stock_list)} 只股票")

        # 获取每只股票的日线数据
        for _, row in stock_list.iterrows():
            code = row['代码']
            name = row['名称']
            try:
                daily_data = stock_fetcher.fetch_stock_daily(code)
                stock_saver.save(daily_data)
                logger.info(f"股票 {code}({name}) 数据下载并保存成功")
            except Exception as e:
                logger.error(f"处理股票 {code}({name}) 时发生错误: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"下载股票数据时发生错误: {str(e)}")

async def download_index_data():
    """下载指数数据"""
    index_fetcher = IndexDataFetcher()
    index_saver = IndexDataSaver()
    
    try:
        # 获取指数列表
        index_list = index_fetcher.fetch_index_list()
        logger.info(f"获取到 {len(index_list)} 个指数")

        # 获取每个指数的日线数据
        for _, row in index_list.iterrows():
            code = row['代码']
            name = row['名称']
            try:
                daily_data = index_fetcher.fetch_index_daily(code)
                index_saver.save(daily_data)
                logger.info(f"指数 {code}({name}) 数据下载并保存成功")
            except Exception as e:
                logger.error(f"处理指数 {code}({name}) 时发生错误: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"下载指数数据时发生错误: {str(e)}")

async def main():
    """主函数"""
    await download_stock_data()
    await download_index_data()

if __name__ == "__main__":
    asyncio.run(main())