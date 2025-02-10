import pandas as pd
from datetime import datetime
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.core.config import config
from src.core.logger import logger
from src.utils.db_utils import initialize_database_if_needed
from src.utils.file_utils import check_file_validity

def main():
    initialize_database_if_needed() # 初始化数据库检查

    fetcher = DataFetcher()
    saver = DataSaver()

    # 获取指数列表
    if check_file_validity(config.CACHE_PATH+"/index_list.csv", config.MAX_CSV_AGE_DAYS):
        logger.info("从缓存读取指数列表")
        index_list = pd.read_csv(config.CACHE_PATH+"/index_list.csv")
    else:
        logger.info("从API获取指数列表")
        index_list = fetcher.fetch_index_list()
        saver.save_index_list_to_csv(index_list, config.CACHE_PATH+"/index_list.csv")

    # 下载指数日数据并保存到数据库
    for symbol in index_list["代码"]:
        index_data = fetcher.fetch_index_daily_data(symbol, "20040101", datetime.today().strftime("%Y%m%d"))
        saver.save_index_daily_data_to_db(index_data, symbol)
        logger.info(f"指数 {symbol} 日数据下载并保存完成")

    logger.info("指数数据下载任务完成")


if __name__ == "__main__":
    main()