import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, TimeoutError

import akshare as ak

from src.core.config import config
from src.core.exceptions import DataFetchError
from src.core.logger import logger


class DataFetcher:
    def __init__(self):
        self.today = datetime.today()

    @staticmethod
    def fetch_stock_list():
        """获取股票列表"""
        try:
            logger.info("Fetching stock list...")
            stock_list = ak.stock_zh_a_spot()
            return stock_list
        except Exception as e:
            logger.error(f"Failed to fetch stock list: {e}")
            raise DataFetchError(f"Failed to fetch stock list: {e}")

    @staticmethod
    def fetch_index_list():
        """获取指数列表"""
        try:
            logger.info("Fetching index list...")
            index_list = ak.stock_zh_index_spot_sina()
            return index_list
        except Exception as e:
            logger.error(f"Failed to fetch index list: {e}")
            raise DataFetchError(f"Failed to fetch index list: {e}")

    @staticmethod
    def _fetch_with_timeout(fetch_func, *args, **kwargs):
        """带超时的数据获取"""
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(fetch_func, *args, **kwargs)
            try:
                return future.result(timeout=config.GET_TIMEOUT)
            except TimeoutError:
                raise DataFetchError(f"Operation timed out after {config.GET_TIMEOUT} seconds")

    @staticmethod
    def _fetch_with_retry(fetch_func, *args, max_retries=config.MAX_RETRIES, retry_delay=config.RETRY_DELAY, **kwargs):
        """带重试和超时的数据获取"""
        for attempt in range(max_retries):
            try:
                result = DataFetcher._fetch_with_timeout(fetch_func, *args, **kwargs)
                time.sleep(0.5)  # 成功后等待1秒
                return result
            except DataFetchError as e:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise DataFetchError(f"Failed to fetch data after {max_retries} attempts: {str(e)}")
            except Exception as e:
                logger.warning(f"Error on attempt {attempt + 1}/{max_retries}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise DataFetchError(f"Failed to fetch data after {max_retries} attempts: {e}")

    def fetch_stock_daily_data(self, symbol, start_date, end_date, adjust):
        logger.info(f"Fetching daily data in mode {adjust}: for {symbol} from {start_date} to {end_date}...")
        return self._fetch_with_retry(
            ak.stock_zh_a_daily,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )

    def fetch_index_daily_data(self, symbol, start_date, end_date):
        """获取指数日数据"""
        logger.info(f"Fetching daily data for index {symbol} from {start_date} to {end_date}...")
        symbol = symbol[2:]  # 2个API的symbol不一样
        return self._fetch_with_retry(
            ak.index_zh_a_hist,
            symbol=symbol,
            period="daily",
            start_date=start_date,
            end_date=end_date
        )

    def fetch_concept_board_list(self):
        """获取概念板块列表"""
        try:
            logger.info("Fetching concept board list...")
            return self._fetch_with_retry(ak.stock_board_concept_name_em)
        except Exception as e:
            logger.error(f"Failed to fetch concept board list: {e}")
            raise DataFetchError(f"Failed to fetch concept board list: {e}")

    def fetch_concept_board_daily_data(self, board_name, adjust, start_date='20220101', end_date='20310101'):
        """获取概念板块历史数据"""
        try:
            logger.info(f"Fetching daily data in mode {adjust} : for concept board {board_name}...")
            return self._fetch_with_retry(
                ak.stock_board_concept_hist_em,
                symbol=board_name,
                start_date=start_date,      # 这里要想办法解决一下，起始时间如何根据API来确定？
                end_date=end_date,
                adjust=adjust
            )

        except Exception as e:
            logger.error(f"Failed to fetch concept board data: {e}")
            raise DataFetchError(f"Failed to fetch concept board data: {e}")


    def get_last_n_days(self, n):
        """获取过去 n 天的日期"""
        return (self.today - timedelta(days=n)).strftime("%Y%m%d")