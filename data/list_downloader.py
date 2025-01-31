import akshare as ak
from utils.retry_utils import retry_config

class ListDownloader:
    @staticmethod
    @retry_config
    def get_stock_list():
        """
        获取所有 A 股股票列表。

        Returns:
            pandas.DataFrame: 包含股票代码和名称的 DataFrame。
        """
        try:
            stock_list = ak.stock_info_a_code_name()
            if stock_list is None or stock_list.empty:
                raise ValueError("获取的股票列表为空")
            return stock_list
        except Exception as e:
            raise RuntimeError(f"获取股票列表失败: {str(e)}")

    @staticmethod
    @retry_config
    def get_index_list():
        """
        获取所有指数列表。

        Returns:
            pandas.DataFrame: 包含指数代码和名称的 DataFrame。
        """
        try:
            index_list = ak.index_stock_info()
            if index_list is None or index_list.empty:
                raise ValueError("获取的指数列表为空")
            return index_list
        except Exception as e:
            raise RuntimeError(f"获取指数列表失败: {str(e)}")