# scripts/strategy.py
"""
scripts/strategy.py

主程序，运行选股策略流程。
"""

import pandas as pd

import scripts.strategy.magic_nine as magic_nine
import scripts.strategy.deep_down as deep_down  # Import the deep_down strategy
import scripts.strategy.data_reader as data_reader
import scripts.strategy.output as output


def run_magic_nine_strategy(data, output_instance):
    """
    运行 Magic Nine 选股策略。
    """
    magic_nine_strategy = magic_nine.MagicNineStrategy()
    data = magic_nine_strategy.calculate_nine_reversal(data)
    buy_signals, sell_signals = magic_nine_strategy.find_signals(data)
    output_instance.print_signals(buy_signals, sell_signals, "Magic Nine")


def run_deep_down_strategy(stock_data, index_data, output_instance):
    """
    运行 Deep Down 选股策略。
    """
    deep_down_strategy = deep_down.DeepDownStrategy()
    data = deep_down_strategy.calculate_signals(stock_data, index_data)
    buy_signals = deep_down_strategy.find_signals(data)
    output_instance.print_signals(buy_signals, pd.DataFrame(), "Deep Down")  # 这个策略只有买入信号


def main():
    """
    主函数，运行选股策略。
    """
    # 示例任务
    tasks = [
        ('temp', ['sh600522', 'sh600523'], '20200101', '20250101'),  # 股票数据
        ('index', 'sh000001')  # 上证指数数据
    ]

    # 初始化模块
    data_reader_instance = data_reader.DataReader()
    output_instance = output.Output()

    # 读取数据
    stock_data = data_reader_instance.get_data(tasks[0][0], tasks[0][1], tasks[0][2], tasks[0][3])
    index_data = data_reader_instance.get_data(tasks[1][0], tasks[1][1], tasks[0][2], tasks[0][3])

    if stock_data.empty:
        print(f"{tasks[0][0]} 数据为空，跳过")
        return

    if index_data.empty:
        print(f"{tasks[1][0]} 数据为空，跳过")
        return

    # 运行魔术九转策略
    # run_magic_nine_strategy(stock_data.copy(), output_instance)

    # 运行深度下跌策略
    run_deep_down_strategy(stock_data.copy(), index_data.copy(), output_instance)


if __name__ == "__main__":
    main()

# -- 创建 deep_down 表
# CREATE TABLE IF NOT EXISTS public.deep_down (
#     date DATE NOT NULL,
#     bullseye INTEGER NOT NULL
# );
#
# -- 插入数据到 deep_down 表
# WITH base_data AS (
#     -- 获取股票和大盘的基础数据
#     SELECT
#         s.symbol AS stock_symbol,
#         s.date,
#         s.close AS stock_close,
#         s.low AS stock_low,
#         s.high AS stock_high,
#         i.close AS index_close
#     FROM
#         public.stock_daily_data s
#     LEFT JOIN
#         public.index_daily_data i
#     ON
#         s.date = i.date AND i.symbol = 'sh000001'
#     WHERE
#         s.date BETWEEN '2021-01-01' AND '2022-12-31'
# ),
# dxjp_calc AS (
#     -- 计算 DXJP 指标
#     SELECT
#         stock_symbol,
#         date,
#         stock_close,
#         (stock_close - MIN(stock_low) OVER (PARTITION BY stock_symbol ORDER BY date ROWS BETWEEN 62 PRECEDING AND CURRENT ROW)) /
#         NULLIF(MAX(stock_high) OVER (PARTITION BY stock_symbol ORDER BY date ROWS BETWEEN 43 PRECEDING AND CURRENT ROW) -
#                MIN(stock_low) OVER (PARTITION BY stock_symbol ORDER BY date ROWS BETWEEN 62 PRECEDING AND CURRENT ROW), 0) * 100 AS dxjp
#     FROM
#         base_data
# ),
# fs_calc AS (
#     -- 计算 FS 指标（DXJP 的 3 日指数移动平均）
#     SELECT
#         stock_symbol,
#         date,
#         stock_close,
#         dxjp,
#         AVG(dxjp) OVER (PARTITION BY stock_symbol ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS fs
#     FROM
#         dxjp_calc
# ),
# cond1_calc AS (
#     -- 计算 COND1 条件
#     SELECT
#         stock_symbol,
#         date,
#         stock_close,
#         dxjp,
#         fs,
#         CASE
#             WHEN dxjp > fs AND fs < 5 AND LAG(stock_close, 63) OVER (PARTITION BY stock_symbol ORDER BY date) != 0 THEN TRUE
#             ELSE FALSE
#         END AS cond1
#     FROM
#         fs_calc
# ),
# tj1_base AS (
#     -- 计算 TJ1 基础条件
#     SELECT
#         stock_symbol,
#         date,
#         CASE
#             WHEN index_close < LAG(index_close, 1) OVER (PARTITION BY stock_symbol ORDER BY date) * 0.98 THEN 1
#             ELSE 0
#         END AS tj1_flag
#     FROM
#         base_data
# ),
# tj1_calc AS (
#     -- 统计 25 日内满足条件的天数
#     SELECT
#         stock_symbol,
#         date,
#         SUM(tj1_flag) OVER (PARTITION BY stock_symbol ORDER BY date ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS tj1
#     FROM
#         tj1_base
# ),
# cond4_base AS (
#     -- 计算 COND4 基础条件
#     SELECT
#         stock_symbol,
#         date,
#         CASE
#             WHEN stock_close < LAG(stock_close, 1) OVER (PARTITION BY stock_symbol ORDER BY date) * 0.96 THEN 1
#             ELSE 0
#         END AS cond4_flag
#     FROM
#         base_data
# ),
# cond4_calc AS (
#     -- 统计 25 日内满足条件的天数，并判断是否位于 TJ1+0.5 和 TJ1+3.5 之间
#     SELECT
#         b.stock_symbol,
#         b.date,
#         t.tj1,
#         SUM(b.cond4_flag) OVER (PARTITION BY b.stock_symbol ORDER BY b.date ROWS BETWEEN 24 PRECEDING AND CURRENT ROW) AS cond4_count,
#         CASE
#             WHEN SUM(b.cond4_flag) OVER (PARTITION BY b.stock_symbol ORDER BY b.date ROWS BETWEEN 24 PRECEDING AND CURRENT ROW)
#                  BETWEEN t.tj1 + 0.5 AND t.tj1 + 3.5 THEN TRUE
#             ELSE FALSE
#         END AS cond4
#     FROM
#         cond4_base b
#     INNER JOIN
#         tj1_calc t
#     ON
#         b.stock_symbol = t.stock_symbol AND b.date = t.date
# ),
# lsxg2_calc AS (
#     -- 计算 LSXG2 条件
#     SELECT
#         stock_symbol,
#         date,
#         CASE
#             WHEN stock_close > 2 AND stock_close < LAG(stock_close, 1) OVER (PARTITION BY stock_symbol ORDER BY date) * 1.09 THEN TRUE
#             ELSE FALSE
#         END AS lsxg2
#     FROM
#         base_data
# ),
# final_selection AS (
#     -- 合并所有条件
#     SELECT
#         c1.date,
#         COUNT(DISTINCT c1.stock_symbol) AS bullseye
#     FROM
#         cond1_calc c1
#     INNER JOIN
#         cond4_calc c4
#     ON
#         c1.stock_symbol = c4.stock_symbol AND c1.date = c4.date
#     INNER JOIN
#         lsxg2_calc l
#     ON
#         c1.stock_symbol = l.stock_symbol AND c1.date = l.date
#     WHERE
#         c1.cond1 = TRUE AND c4.cond4 = TRUE AND l.lsxg2 = TRUE
#     GROUP BY
#         c1.date
# )
# -- 插入结果到 deep_down 表
# INSERT INTO public.deep_down (date, bullseye)
# SELECT
#     date,
#     bullseye
# FROM
#     final_selection;