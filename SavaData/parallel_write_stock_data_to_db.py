from concurrent.futures import ThreadPoolExecutor, as_completed
from sava_stock_data_to_db import save_stock_data_to_db, read_stock_list
import psycopg2.pool
from Config.config import DATABASE_URL

# 创建数据库连接池
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)

def get_db_connection():
    """
    从连接池中获取数据库连接
    """
    return connection_pool.getconn()

def release_db_connection(conn):
    """
    释放数据库连接回连接池
    """
    connection_pool.putconn(conn)

# ... 修改 save_stock_data_to_db 函数，使用 get_db_connection 和 release_db_connection ...

def parallel_write_stock_data_to_db():
    """
    并行调用 save_stock_data_to_db 方法，加速数据下载和写入。
    """
    stock_list = read_stock_list()

    # 使用线程池并行处理每只股票的数据
    with ThreadPoolExecutor(max_workers=4) as executor:  # 可以根据需要调整线程数
        futures = []
        for stock_code, stock_name in stock_list:
            # 提交任务到线程池，调用改造后的 write_stock_data_to_db
            future = executor.submit(save_stock_data_to_db, stock_code, stock_name)
            futures.append(future)

        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                future.result()  # 获取任务结果，确保任务完成
            except Exception as e:
                print(f"任务执行出错: {e}")

        print("==========多个线程处理股票数据下载完毕==========")

if __name__ == "__main__":
    # 并行写入股票数据
    parallel_write_stock_data_to_db()
