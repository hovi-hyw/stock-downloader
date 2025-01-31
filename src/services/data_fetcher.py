import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from src.core.logger import logger
from src.core.exceptions import DataFetchError

class DataFetcher:
    def __init__(self):
        self.today = datetime.today()

    def fetch_stock_list(self):
        """获取股票列表"""
        try:
            logger.info("Fetching stock list...")
            stock_list = ak.stock_zh_a_spot()
            return stock_list
        except Exception as e:
            logger.error(f"Failed to fetch stock list: {e}")
            raise DataFetchError(f"Failed to fetch stock list: {e}")

    def fetch_index_list(self):
        """获取指数列表"""
        try:
            logger.info("Fetching index list...")
            index_list = ak.stock_zh_index_spot_sina()
            return index_list
        except Exception as e:
            logger.error(f"Failed to fetch index list: {e}")
            raise DataFetchError(f"Failed to fetch index list: {e}")

    def fetch_stock_daily_data(self, symbol, start_date, end_date):
        """获取股票日数据"""
        try:
            logger.info(f"Fetching daily data for stock {symbol} from {start_date} to {end_date}...")
            stock_data = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, end_date=end_date)
            return stock_data
        except Exception as e:
            logger.error(f"Failed to fetch daily data for stock {symbol}: {e}")
            raise DataFetchError(f"Failed to fetch daily data for stock {symbol}: {e}")

    def fetch_index_daily_data(self, symbol, start_date, end_date):
        """获取指数日数据"""
        try:
            logger.info(f"Fetching daily data for index {symbol} from {start_date} to {end_date}...")
            index_data = ak.index_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date)
            return index_data
        except Exception as e:
            logger.error(f"Failed to fetch daily data for index {symbol}: {e}")
            raise DataFetchError(f"Failed to fetch daily data for index {symbol}: {e}")

    def get_last_n_days(self, n):
        """获取过去 n 天的日期"""
        return (self.today - timedelta(days=n)).strftime("%Y%m%d")