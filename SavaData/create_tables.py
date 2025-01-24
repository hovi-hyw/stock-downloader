# SaveData/create_tables.py

from Config.config import DATABASE_URL
import psycopg2
from psycopg2 import sql

def check_and_create_table():
    """
    检查 PostgreSQL 数据库中的 stock 库是否存在 stock_daily 表，
    如果不存在则根据指定字段创建表。
    """
    try:
        # 连接到 PostgreSQL 数据库
        conn = psycopg2.connect(DATABASE_URL)
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
        # 关闭数据库连接
        if conn:
            cursor.close()
            conn.close()

# 执行检查并创建表
if __name__ == "__main__":
    check_and_create_table()