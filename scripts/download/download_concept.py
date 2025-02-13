import time
from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.core.config import config
from src.core.logger import logger
from src.utils.db_utils import initialize_database_if_needed
from src.utils.file_utils import check_file_validity
import pandas as pd


def main():
    initialize_database_if_needed() # 初始化数据库检查

    fetcher = DataFetcher()
    saver = DataSaver()

    # 下载概念板块
    # 1. 获取并保存概念板块列表
    if check_file_validity(config.CACHE_PATH+"/2025-02-12.csv", config.MAX_CSV_AGE_DAYS):
        logger.info("从缓存读取概念板块列表")
        concept_list = pd.read_csv(config.CACHE_PATH+"/2025-02-12.csv")
    else:
        logger.info("从API获取概念板块列表")
        concept_list = fetcher.fetch_concept_board_list()
        saver.save_concept_board_list_to_csv(concept_list, config.CACHE_PATH+"/2025-02-12.csv")


    # 2. 获取并保存每个概念板块的历史数据
    for _, row in concept_list.iterrows():
        board_name = row['板块名称']
        board_code = row['板块代码']

        try:
            hist_data = fetcher.fetch_concept_board_daily_data(board_name, adjust='hfq')
            if hist_data is not None:
                saver.save_concept_board_data_to_db(hist_data, board_name, board_code)
                logger.info(f"概念板块 {board_name} 日数据下载并保存完成")
            time.sleep(0.5)  # 避免请求过快
        except Exception as e:
            logger.error(f"Error processing board {board_name}: {e}")
            continue

    logger.info("概念板块数据下载任务完成")


if __name__ == "__main__":
    main()