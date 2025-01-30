"""
File: index/index_downloader.py
功能：实现单个指数下载和并行批量下载的核心功能
"""

import concurrent.futures
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import logging
from GetData.get_index_list import get_index_list
from GetData.get_index_data import get_index_data
import time
import random
from retrying import retry

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def get_index_list_with_retry():
    """带重试机制的指数列表获取函数"""
    try:
        index_list = get_index_list()
        if index_list is None or index_list.empty:
            raise ValueError("获取到的指数列表为空")
        return index_list
    except Exception as e:
        logger.error(f"获取指数列表失败: {str(e)}")
        raise

@retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
def download_single_index(index_code: str) -> pd.DataFrame:

    """下载单个指数的历史数据(带重试机制)

    通过指数代码获取该指数的所有历史交易数据。首先获取指数的基本信息（代码和名称），
    然后获取其历史交易数据，最后将两部分数据合并。

    Args:
        index_code: str, 指数代码

    Returns:
        pd.DataFrame: 包含该指数所有历史数据的DataFrame

    Raises:
        ValueError: 当指数代码无效时抛出
        RuntimeError: 当数据获取失败时抛出
    """
    try:
        logger.info(f"开始下载指数 {index_code} 的数据...")

        # 获取指数基本信息
        index_list = get_index_list_with_retry()
        index_info = index_list[index_list['代码'] == index_code]

        if index_info.empty:
            raise ValueError(f"无效的指数代码: {index_code}")

        # 添加随机延时，避免频繁请求
        time.sleep(random.uniform(0.5, 1.5))

        # 获取历史数据
        symbol = index_code[2:]
        hist_data = get_index_data(symbol=symbol)

        if hist_data is None or hist_data.empty:
            raise RuntimeError(f"获取指数 {index_code} 的历史数据失败")

        hist_data['code'] = index_code
        hist_data['name'] = index_info['名称'].iloc[0]

        logger.info(f"成功下载指数 {index_code} ({index_info['名称'].iloc[0]}) 的数据")
        return hist_data

    except Exception as e:
        logger.error(f"下载指数 {index_code} 时发生错误: {str(e)}")
        raise


def download_indices_in_batches(index_codes: List[str],
                                batch_size: int = 10,
                                max_workers: int = 2) -> Dict[str, pd.DataFrame]:
    """分批并行下载指数数据

    将大量指数下载任务分成小批次，每个批次使用线程池并行处理，
    避免同时发起过多请求而导致的问题。

    Args:
        index_codes: List[str], 需要下载的指数代码列表
        batch_size: int, 每批处理的指数数量，默认为5
        max_workers: int, 每批次的最大线程数，默认为3

    Returns:
        Dict[str, pd.DataFrame]: 键为指数代码，值为对应的历史数据DataFrame
    """
    results = {}
    failed_indices = []
    total_indices = len(index_codes)

    # 计算总批次数
    total_batches = (total_indices + batch_size - 1) // batch_size

    logger.info(f"开始下载 {total_indices} 个指数的数据，分 {total_batches} 批处理")

    # 分批处理
    with tqdm(total=total_indices, desc="总体进度") as pbar:
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, total_indices)
            current_batch = index_codes[start_idx:end_idx]

            logger.info(f"\n开始处理第 {batch_idx + 1}/{total_batches} 批 "
                        f"({len(current_batch)} 个指数)")

            # 对当前批次使用线程池并行处理
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_index = {
                    executor.submit(download_single_index, code): code
                    for code in current_batch
                }

                for future in concurrent.futures.as_completed(future_to_index):
                    index_code = future_to_index[future]
                    try:
                        data = future.result()
                        results[index_code] = data
                        pbar.update(1)
                    except Exception as e:
                        failed_indices.append((index_code, str(e)))
                        pbar.update(1)
                        logger.error(f"下载指数 {index_code} 失败: {str(e)}")

    # 输出下载统计信息
    success_count = len(results)
    fail_count = len(failed_indices)
    logger.info(f"\n下载完成统计:")
    logger.info(f"- 成功: {success_count} 个")
    logger.info(f"- 失败: {fail_count} 个")

    if failed_indices:
        error_msg = "\n失败详情:\n" + "\n".join([f"- {code}: {error}" for code, error in failed_indices])
        logger.error(error_msg)
        raise RuntimeError(f"部分指数下载失败。成功 {success_count} 个，失败 {fail_count} 个。{error_msg}")

    return results