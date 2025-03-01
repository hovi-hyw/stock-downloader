from datetime import datetime

import pandas as pd

from src.core.config import config
from src.core.logger import logger
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.utils.db_utils import initialize_database_if_needed
from src.utils.file_utils import check_file_validity


def format_index_code(symbol):
    """确保指数代码为6位数字格式"""
    return str(symbol).zfill(6)


def main():
    initialize_database_if_needed()  # 初始化数据库检查

    fetcher = DataFetcher()
    saver = DataSaver()

    # 获取指数列表
    if check_file_validity(config.CACHE_PATH + "/index_list.csv", config.MAX_CSV_AGE_DAYS):
        logger.info("从缓存读取指数列表")
        index_list = pd.read_csv(config.CACHE_PATH + "/index_list.csv")
    else:
        logger.info("从东方财富获取指数列表")
        index_list = fetcher.fetch_index_list()
        saver.save_index_list_to_csv(index_list, config.CACHE_PATH + "/index_list.csv")

    # 下载指数日数据并保存到数据库
    for _, row in index_list.iterrows():
        symbol = row["代码"]
        name = row["名称"]
        formatted_symbol = format_index_code(symbol)
        try:
            index_data = fetcher.fetch_index_daily_data(
                formatted_symbol,
                "20040101",
                datetime.today().strftime("%Y%m%d")
            )
            if index_data is None:
                logger.warning(f"未能获取到指数 {formatted_symbol}({name}) 的数据")
                continue
            saver.save_index_daily_data_to_db(index_data, formatted_symbol, name)
            logger.info(f"指数 {formatted_symbol}({name}) 日数据下载并保存完成")
        except Exception as e:
            logger.error(f"处理指数 {formatted_symbol}({name}) 时出错: {e}")
            continue


if __name__ == "__main__":
    main()
