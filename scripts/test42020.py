import psycopg2
import csv
import os
from src.core.config import config

def query_stock_data(input_year, min_trade_days_in1year, table_name, output_dir="."):
    """
    查询股票数据，包括平均值、最高/低前3个值、中位数，并按平均值排序。
    结果保存为 CSV 文件。

    Args:
        input_year: 查询年份。
        min_trade_days_in1year: 最少交易天数。
        table_name: 数据库表名。
        output_dir: CSV 文件输出目录，默认为当前目录。

    Returns:
        如果查询成功并保存为 CSV 文件，则返回 True；否则返回 False。
    """
    try:
        conn = psycopg2.connect(config.DATABASE_URL)  # 替换为你的数据库连接信息
        cur = conn.cursor()


        query = f"""
            WITH StockTradeDays AS (
                SELECT symbol
                FROM {table_name}
                WHERE EXTRACT(YEAR FROM date) = {input_year}
                GROUP BY symbol
                HAVING COUNT(DISTINCT date) > {min_trade_days_in1year}
            ),
            RankedRealChange AS (
                SELECT 
                    symbol,
                    real_change,
                    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY real_change DESC) as rn_desc,
                    ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY real_change) as rn_asc
                FROM {table_name}
                WHERE EXTRACT(YEAR FROM date) = {input_year}
                AND symbol IN (SELECT symbol FROM StockTradeDays)
            ),
            Top3 AS (
                SELECT symbol, array_to_string(ARRAY_AGG(real_change), ',') AS top3_real_change
                FROM RankedRealChange
                WHERE rn_desc <= 3
                GROUP BY symbol
            ),
            MedianRealChange AS (
                SELECT symbol, 
                       (
                           SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY real_change)
                           FROM {table_name}
                           WHERE EXTRACT(YEAR FROM date) = {input_year} AND symbol = a.symbol
                       ) AS median_real_change
                FROM (SELECT DISTINCT symbol FROM {table_name} WHERE EXTRACT(YEAR FROM date) = {input_year} AND symbol IN (SELECT symbol FROM StockTradeDays)) a
                GROUP BY a.symbol
            ),
            Bottom3 AS (
                SELECT symbol, array_to_string(ARRAY_AGG(real_change), ',') AS bottom3_real_change
                FROM RankedRealChange
                WHERE rn_asc <= 3
                GROUP BY symbol
            ),
            AvgRealChange AS (
                SELECT symbol, AVG(real_change) AS avg_real_change
                FROM {table_name}
                WHERE EXTRACT(YEAR FROM date) = {input_year}
                AND symbol IN (SELECT symbol FROM StockTradeDays)
                GROUP BY symbol
            )
            SELECT 
                a.symbol,
                a.avg_real_change,
                b.top3_real_change,
                m.median_real_change,
                c.bottom3_real_change
            FROM AvgRealChange a
            LEFT JOIN Top3 b ON a.symbol = b.symbol
            LEFT JOIN MedianRealChange m ON a.symbol = m.symbol
            LEFT JOIN Bottom3 c ON a.symbol = c.symbol
            ORDER BY a.avg_real_change DESC;
        """

        cur.execute(query)
        results = []
        for row in cur:
            results.append({
                "symbol": row[0],
                "avg_real_change": row[1],
                "top3_real_change": row[2],
                "median_real_change": row[3],
                "bottom3_real_change": row[4]
            })

        conn.close()

        if not results:
            # 查询结果为空
            count_query = f"SELECT COUNT(*) FROM {table_name} WHERE EXTRACT(YEAR FROM date) = {year}"
            cur = conn.cursor()
            cur.execute(count_query)
            count = cur.fetchone()[0]
            conn.close()
            if count == 0:
                print(f"表 {table_name} 在 {year} 年没有数据。")
            else:
                print(f"查询表 {table_name} 出错。")
            return False

        # 将结果保存为 CSV 文件
        filename = f"{table_name}_{year}.csv"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow(row)

        print(f"查询结果已保存到 {filepath}")
        return True

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or executing query:", error)
        return False

# 示例调用
years = range(2005,2025)
min_trade_days = 200
tables = ["derived.sh_stock", "derived.bj_stock", "derived.sz_stock"]

for table in tables:
    for year in years:
        if query_stock_data(year, min_trade_days, table, output_dir="../data/"):
            print(f"成功查询并保存 {table} 的数据。")
        else:
            print(f"查询或保存 {table} 数据时出错。")