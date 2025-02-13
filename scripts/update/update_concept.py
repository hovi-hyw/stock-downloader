from datetime import datetime
import os


from src.services.data_fetcher import DataFetcher
from src.services.data_saver import DataSaver
from src.core.config import config
from src.core.logger import logger

def is_file_from_today(file_path):
    """检查文件是否是今天生成的"""
    if not os.path.exists(file_path):
        return False
    
    file_timestamp = os.path.getmtime(file_path)
    file_date = datetime.fromtimestamp(file_timestamp).date()
    today = datetime.now().date()
    
    return file_date == today


def main():
    concept_board_file = os.path.join(config.CACHE_PATH, "2025-02-12.csv")
    
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