import concurrent.futures
from tqdm import tqdm
from data.stock_downloader import StockDownloader
from data.index_downloader import IndexDownloader
from services.save_service import DataSaver

class BatchProcessor:
    def __init__(self, data_saver: DataSaver):
        self.data_saver = data_saver

    def process_in_batches(self, symbols: list, data_type: str, batch_size: int = 5, max_workers: int = 2):
        """
        批量处理数据下载和存储。

        Args:
            symbols (list): 股票或指数代码列表。
            data_type (str): 数据类型，"stock" 或 "index"。
            batch_size (int): 每批处理数量。
            max_workers (int): 最大线程数。
        """
        total_symbols = len(symbols)
        total_batches = (total_symbols + batch_size - 1) // batch_size

        with tqdm(total=total_symbols, desc="总体进度") as pbar:
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min(start_idx + batch_size, total_symbols)
                current_batch = symbols[start_idx:end_idx]

                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {
                        executor.submit(self._process_single, symbol, data_type): symbol
                        for symbol in current_batch
                    }

                    for future in concurrent.futures.as_completed(futures):
                        symbol = futures[future]
                        try:
                            future.result()
                        except Exception as e:
                            print(f"处理 {symbol} 时出错: {str(e)}")
                        finally:
                            pbar.update(1)

    def _process_single(self, symbol: str, data_type: str):
        """
        处理单个股票或指数的下载和保存。

        Args:
            symbol (str): 股票或指数代码。
            data_type (str): 数据类型，"stock" 或 "index"。
        """
        if data_type == "stock":
            stock_data = StockDownloader.get_stock_data(
                symbol=symbol,
                start_date="19900101",
                end_date="20900101",
                adjust="qfq"
            )
            self.data_saver.save_stock_data(stock_data)
        elif data_type == "index":
            index_data = IndexDownloader.get_index_data(
                symbol=symbol,
                period="daily",
                start_date="19900101",
                end_date="20900101"
            )
            self.data_saver.save_index_data(index_data)
        else:
            raise ValueError(f"不支持的数据类型: {data_type}")