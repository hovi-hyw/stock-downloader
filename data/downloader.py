import akshare as ak
import pandas as pd
from utils.retry_utils import retry


class DataDownloader:
    @staticmethod
    @retry(tries=3, delay=1, backoff=2)
    def download_data(method: str, **kwargs) -> pd.DataFrame:
        """
        通用数据下载方法，支持股票和指数数据。

        Args:
            method (str): akshare 中的下载方法名，例如 "index_zh_a_hist" 或 "stock_zh_a_daily"。
            kwargs: 传递给 akshare 方法的参数。

        Returns:
            pd.DataFrame: 下载的数据。
        """
        try:
            func = getattr(ak, method)  # 动态调用 akshare 方法
            data = func(**kwargs)
            if data is None or data.empty:
                raise ValueError(f"下载的数据为空: method={method}, params={kwargs}")
            return data
        except Exception as e:
            raise RuntimeError(f"数据下载失败: {str(e)}")