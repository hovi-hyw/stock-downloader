"""
File: download_all_indices.py
功能：下载所有指数数据并保存到数据库
"""

import logging
import random

from index.index_downloader import download_indices_in_batches, get_index_list_with_retry
from index.index_storage import save_to_database
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def download_and_save_all_indices(batch_size: int = 5, max_workers: int = 3):
    """
    下载所有指数数据并保存到数据库

    Args:
        batch_size: int, 每批处理的指数数量
        max_workers: int, 每批次的最大线程数
    """
    try:
        # 获取所有指数列表
        logger.info("获取指数列表...")
        retries = 3
        for attempt in range(retries):
            try:
                index_list = get_index_list_with_retry()
                all_index_codes = index_list['代码'].tolist()
                logger.info(f"共找到 {len(all_index_codes)} 个指数")
                break
            except Exception as e:
                if attempt == retries - 1:
                    raise
                logger.warning(f"第 {attempt + 1} 次尝试获取指数列表失败，将重试...")
                time.sleep(random.uniform(2, 5))

        # 分批下载数据
        logger.info("开始下载指数数据...")
        results = download_indices_in_batches(
            all_index_codes,
            batch_size=batch_size,
            max_workers=max_workers
        )

        # 保存成功下载的数据到数据库
        if results:
            logger.info(f"开始保存 {len(results)} 个成功下载的指数数据到数据库...")
            save_to_database(results)
            logger.info("数据保存完成")

    except Exception as e:
        logger.error(f"处理过程中发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # 减小并发数和批次大小，增加间隔时间
        download_and_save_all_indices(batch_size=5, max_workers=2)
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")