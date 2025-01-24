from concurrent.futures import ThreadPoolExecutor, as_completed

from GetData import get_stock_data
from sava_stock_data_to_db import write_stock_data_to_db, read_stock_list
import os
from Config.config import DATABASE_URL
import psycopg2
from psycopg2 import sql

def write_stock_data_to_db_parallel():
    """
    并行调用 write_stock_data_to_db 方法，加速数据下载和写入。
    """
    stock_list = read_stock_list()
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # 使用线程池并行处理每只股票的数据
        with ThreadPoolExecutor(max_workers=10) as executor:  # 可以根据需要调整线程数
            futures = []
            for stock_code, stock_name in stock_list:
                # 提交任务到线程池
                future = executor.submit(write_stock_data_for_single_stock, stock_code, stock_name, conn)
                futures.append(future)

            # 等待所有任务完成
            for future in as_completed(futures):
                try:
                    future.result()  # 获取任务结果，确保任务完成
                except Exception as e:
                    print(f"任务执行出错: {e}")

    except Exception as e:
        print(f"数据库操作出错: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def write_stock_data_for_single_stock(stock_code, stock_name, conn):
    """
    处理单只股票的数据下载和写入。
    """
    cursor = None
    try:
        cursor = conn.cursor()

        # 获取股票历史数据
        stock_data = get_stock_data(stock_code)

        # 获取数据库中该股票最新的日期
        cursor.execute(
            "SELECT MAX(date) FROM stock_daily WHERE code = %s",
            (stock_code,)
        )
        last_date = cursor.fetchone()[0]

        # 过滤出需要更新的数据
        if last_date:
            stock_data = stock_data[stock_data['date'] > last_date]

        if not stock_data.empty:
            # 准备插入数据
            insert_query = sql.SQL("""
                INSERT INTO stock_daily 
                (code, date, open, high, low, close, volume, amount, outstanding_share, turnover)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (code, date) 
                DO NOTHING
            """)

            # 执行插入
            data_to_insert = [
                (stock_code,) + tuple(row) for row in stock_data.itertuples(index=False)
            ]
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
            print(f"更新了 {stock_code} ({stock_name}) 的 {len(data_to_insert)} 条记录")
        else:
            print(f"{stock_code} ({stock_name}) 没有新数据需要更新")

    except Exception as e:
        print(f"处理 {stock_code} ({stock_name}) 时出错: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    # 并行写入股票数据
    write_stock_data_to_db_parallel()