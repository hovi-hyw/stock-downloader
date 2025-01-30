import sys
from SavaData.save_stock_list_to_csv import save_stock_list_to_csv
import os
import pandas as pd
from Config.config import STOCK_LIST_CACHE, DATABASE_URL
import psycopg2
from psycopg2 import sql, pool
from GetData import get_stock_data

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

def check_and_create_table():
    """
    检查 PostgreSQL 数据库中的 stock 库是否存在 stock_daily 表，
    如果不存在则根据指定字段创建表。
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 检查表是否存在
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'stock_daily'
            );
        """)
        table_exists = cursor.fetchone()[0]

        # 如果表不存在，则创建表
        if not table_exists:
            create_table_query = sql.SQL("""
                CREATE TABLE stock_daily (
                    code TEXT,
                    date DATE,
                    open FLOAT,
                    high FLOAT,
                    low FLOAT,
                    close FLOAT,
                    volume FLOAT,
                    amount FLOAT,
                    outstanding_share FLOAT,
                    turnover FLOAT,
                    PRIMARY KEY (code, date)
                );
            """)
            cursor.execute(create_table_query)
            conn.commit()
            print("表 stock_daily 创建成功。")
        else:
            print("表 stock_daily 已存在，无需创建。")

    except Exception as e:
        print(f"操作数据库时出错: {e}")
    finally:
        if conn:
            release_db_connection(conn)


def read_stock_list():
    """
    读取股票列表CSV文件,返回包含股票代码和名称的列表。
    返回列是['代码', '名称']
    """
    file_path = os.path.join(r"../", STOCK_LIST_CACHE)
    try:
        df = pd.read_csv(file_path, usecols=['代码', '名称'])
        return df.values.tolist()
    except Exception as e:
        print(f"读取股票列表文件时出错: {e}")
        return []

def save_stock_data_to_db(stock_code=None, stock_name=None):
    """
    读取股票列表,获取每只股票的历史数据,并写入数据库。
    如果传入 stock_code 和 stock_name，则只处理该股票；否则处理所有股票。
    """
    if stock_code is None or stock_name is None:
        # 如果没有传入股票代码和名称，则处理所有股票
        stock_list = read_stock_list()
    else:
        # 如果传入了股票代码和名称，则只处理该股票
        stock_list = [(stock_code, stock_name)]

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        for stock_code, stock_name in stock_list:
            try:
                # 获取股票历史数据
                print(f"开始下载 {stock_code} 的数据...")
                stock_data = get_stock_data(stock_code)
                print(f"{stock_code} 的数据下载完成。")

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
                    print(f"开始插入 {stock_code} 的数据...")
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
                print("rollback成功")

    except Exception as e:
        print(f"数据库操作出错: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("==========单个线程处理股票数据下载完毕==========")


if __name__ == "__main__":
    # 1. 检查股票列表：如果股票列表超过100天没有更新，那么就更新，否则直接读取csv文件
    save_stock_list_to_csv()
    # 2. 检查数据库中表格是否存在，不存在就创建，存在就继续
    check_and_create_table()
    # 3. 读取csv文件的字段： 代码、名称
    read_stock_list()
    # 4. 根据read_stock_list的输出，读取到股票的代码和名称，调用GetData.get_stock_data方法获取股票历史数据，
    # 将 代码+获取的数据 一起写入数据库
    save_stock_data_to_db()
    print("程序运行完成，退出。")
    sys.exit(0)  # 显式退出程序