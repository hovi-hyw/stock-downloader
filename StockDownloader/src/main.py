# src/main.py
"""
此模块是应用程序的主入口点。
它负责初始化数据库、启动 FastAPI 应用，并定期执行数据下载任务。
Authors: hovi.hyw & AI
Date: 2024-07-03
"""

import threading
import time

import uvicorn

from .api.app import app
from .core.logger import logger
from .tasks.download_index_task import download_all_index_data
from .tasks.download_stock_task import download_all_stock_data
from .tasks.scheduled_tasks import start_scheduled_tasks
from .utils.db_utils import initialize_database_if_needed


def run_scheduled_tasks():
    """
    定期运行数据下载任务。
    """
    while True:
        logger.info("开始执行定时数据下载任务...")
        download_all_stock_data()
        download_all_index_data()
        logger.info("定时数据下载任务执行完成，等待下次执行...")
        time.sleep(86400)  # 每天执行一次，86400秒 = 1天


def ensure_directories():
    """
    确保必要的目录存在。
    """
    import os
    from .core.config import config
    
    # 确保缓存目录存在
    if not os.path.exists(config.CACHE_PATH):
        logger.info(f"缓存目录 '{config.CACHE_PATH}' 不存在，正在创建...")
        os.makedirs(config.CACHE_PATH, exist_ok=True)
        logger.info(f"缓存目录 '{config.CACHE_PATH}' 创建成功")
    
    # 确保日志目录存在
    log_dir = os.path.dirname(config.LOG_FILE)
    if not os.path.exists(log_dir):
        logger.info(f"日志目录 '{log_dir}' 不存在，正在创建...")
        os.makedirs(log_dir, exist_ok=True)
        logger.info(f"日志目录 '{log_dir}' 创建成功")


def main():
    """
    主函数。
    初始化数据库、启动 FastAPI 应用，并启动定时任务。
    """
    # 确保必要的目录存在
    ensure_directories()
    
    initialize_database_if_needed()

    # 启动每日数据下载定时任务
    task_thread = threading.Thread(target=run_scheduled_tasks)
    task_thread.daemon = True  # 设置为守护线程，主线程退出时自动结束
    task_thread.start()
    
    # 启动交易日特定时间任务（股票列表下载）
    # start_scheduled_tasks()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
