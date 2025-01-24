from concurrent.futures import ThreadPoolExecutor, as_completed
from sava_stock_data_to_db import write_stock_data_to_db, read_stock_list

def write_stock_data_to_db_parallel():
    """
    并行调用 write_stock_data_to_db 方法，加速数据下载和写入。
    """
    stock_list = read_stock_list()

    # 使用线程池并行处理每只股票的数据
    with ThreadPoolExecutor(max_workers=4) as executor:  # 可以根据需要调整线程数
        futures = []
        for stock_code, stock_name in stock_list:
            # 提交任务到线程池，调用改造后的 write_stock_data_to_db
            future = executor.submit(write_stock_data_to_db, stock_code, stock_name)
            futures.append(future)

        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                future.result()  # 获取任务结果，确保任务完成
            except Exception as e:
                print(f"任务执行出错: {e}")

if __name__ == "__main__":
    # 并行写入股票数据
    write_stock_data_to_db_parallel()