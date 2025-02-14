# scripts/strategy.py

"""
scripts/strategy.py
主程序，运行选股策略流程。
"""

import pandas as pd
from datetime import datetime

import scripts.strategy.magic_nine as magic_nine
import scripts.strategy.deep_down as deep_down
import scripts.strategy.deep_down_analysis as deep_down_analysis
import scripts.strategy.data_reader as data_reader
import scripts.strategy.output as output


def run_deep_down_analysis(start_date='20040101', end_date='20250101'):
    """
    运行 Deep Down 策略分析
    分析指定时间范围内每天符合策略的股票数量
    """
    tasks = [
        ('stock', 'all', start_date, end_date),  # 获取所有股票数据
        ('index', 'sh000001', start_date, end_date)
    ]

    data_reader_instance = data_reader.DataReader()
    output_instance = output.Output()

    # 读取数据
    stock_data = data_reader_instance.get_data(tasks[0][0], tasks[0][1], tasks[0][2], tasks[0][3])
    index_data = data_reader_instance.get_data(tasks[1][0], tasks[1][1], tasks[0][2], tasks[0][3])

    if stock_data.empty:
        print("股票数据为空")
        return

    if index_data.empty:
        print("指数数据为空")
        return

    # 运行分析
    analyzer = deep_down_analysis.DeepDownAnalyzer()
    results = analyzer.analyze(stock_data, index_data)

    # 保存结果到CSV
    output_instance.save_analysis_to_csv(results, "deep_down_analysis.csv")


def main():
    """主函数"""
    run_deep_down_analysis()


if __name__ == "__main__":
    main()