import os
from datetime import datetime

from StockDownloader.src.core.config import config
from StockDownloader.src.core.logger import logger
from StockDownloader.src.services.data_fetcher import DataFetcher
from StockDownloader.src.services.data_saver import DataSaver


def is_file_from_today(file_path):
    """检查文件是否是今天生成的"""
    if not os.path.exists(file_path):
        return False

    file_timestamp = os.path.getmtime(file_path)
    file_date = datetime.fromtimestamp(file_timestamp).date()
    today = datetime.now().date()

    return file_date == today


def main():
    # 动态生成当天日期的文件名
    today_str = datetime.now().strftime("%Y-%m-%d")  # 获取当前日期并格式化为 YYYY-MM-DD
    concept_board_file = os.path.join(config.CACHE_PATH, f"{today_str}.csv")

    if not is_file_from_today(concept_board_file):
        logger.info("概念板块列表文件不是今天生成的，需要执行更新任务")
        # 获取数据并保存
        fetcher = DataFetcher()
        saver = DataSaver()
        concept_list = fetcher.fetch_concept_board_list()
        saver.save_concept_board_list_to_csv(concept_list, concept_board_file)
    else:
        logger.info("概念板块列表文件是今天生成的，无需更新")


if __name__ == "__main__":
    main()
