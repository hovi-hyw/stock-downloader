import time

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from src.core.logger import logger
from src.core.exceptions import DataFetchError
from src.core.config import config
import timeout_decorator


class DataFetcher:
    def __init__(self):
        self.today = datetime.today()

    @staticmethod
    def fetch_stock_list(self):
        """获取股票列表"""
        try:
            logger.info("Fetching stock list...")
            stock_list = ak.stock_zh_a_spot()
            return stock_list
        except Exception as e:
            logger.error(f"Failed to fetch stock list: {e}")
            raise DataFetchError(f"Failed to fetch stock list: {e}")

    @staticmethod
    def fetch_index_list(self):
        """获取指数列表"""
        try:
            logger.info("Fetching index list...")
            index_list = ak.stock_zh_index_spot_sina()
            return index_list
        except Exception as e:
            logger.error(f"Failed to fetch index list: {e}")
            raise DataFetchError(f"Failed to fetch index list: {e}")

    @staticmethod
    @timeout_decorator.timeout(config.GET_TIMEOUT)  # 10秒超时
    def _fetch_with_timeout(fetch_func, *args, **kwargs):
        """带超时的数据获取"""
        return fetch_func(*args, **kwargs)

    @staticmethod
    def _fetch_with_retry(fetch_func, *args, max_retries=config.MAX_RETRIES, retry_delay=config.RETRY_DELAY, **kwargs):
        """带重试和超时的数据获取"""
        for attempt in range(max_retries):
            try:
                # 使用带超时的包装函数
                result = DataFetcher._fetch_with_timeout(fetch_func, *args, **kwargs)
                time.sleep(1)  # 成功后等待1秒
                return result
            except timeout_decorator.TimeoutError:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise DataFetchError(f"Operation timed out after {max_retries} attempts")
            except Exception as e:
                logger.warning(f"Error on attempt {attempt + 1}/{max_retries}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise DataFetchError(f"Failed to fetch data after {max_retries} attempts: {e}")

    def fetch_stock_daily_data(self, symbol, start_date, end_date):
        logger.info(f"Fetching daily data for stock {symbol} from {start_date} to {end_date}...")
        return self._fetch_with_retry(
            ak.stock_zh_a_daily,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date
        )

    def fetch_index_daily_data(self, symbol, start_date, end_date):
        """获取指数日数据"""
        logger.info(f"Fetching daily data for index {symbol} from {start_date} to {end_date}...")
        symbol = symbol[2:] # 2个API的symbol不一样
        return self._fetch_with_retry(
            ak.index_zh_a_hist,
            symbol=symbol,
            period="daily",
            start_date=start_date,
            end_date=end_date
        )

    def get_last_n_days(self, n):
        """获取过去 n 天的日期"""
        return (self.today - timedelta(days=n)).strftime("%Y%m%d")