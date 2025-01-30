from data.downloader import DataDownloader

class IndexDownloader:
    @staticmethod
    def get_index_data(symbol: str, period: str = "daily", start_date: str = "19900101", end_date: str = "20900101"):
        """
        获取指定指数的历史数据。

        Args:
            symbol (str): 指数代码，例如 "sh000001" 表示上证指数。
            period (str): 数据周期，可选值为 "daily"（日线）, "weekly"（周线）, "monthly"（月线）。
            start_date (str): 数据开始日期，格式为 "YYYYMMDD"。
            end_date (str): 数据结束日期，格式为 "YYYYMMDD"。

        Returns:
            pandas.DataFrame: 包含历史数据的 DataFrame，包括日期、开盘价、收盘价、最高价等。
        """
        return DataDownloader.download_data(
            method="index_zh_a_hist",
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date
        )

    @staticmethod
    def get_index_list():
        """
        获取所有指数的列表。

        Returns:
            pandas.DataFrame: 包含指数代码和名称的 DataFrame。
        """
        return DataDownloader.download_data(method="index_stock_info")