from data.downloader import DataDownloader

class StockDownloader:
    @staticmethod
    def get_stock_data(symbol: str, start_date: str, end_date: str, adjust: str = ""):
        """
        获取股票数据。
        """
        return DataDownloader.download_data(
            method="stock_zh_a_daily",
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )