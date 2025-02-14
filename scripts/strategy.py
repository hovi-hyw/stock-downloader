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
from core.logger import logger


# scripts/strategy.py

def run_deep_down_analysis(start_date='20040101', end_date='20250101',
                           output_mode=output.OutputMode.PRINT, filename=None, db_session=None):
    """
    运行 Deep Down 策略横向分析
    """
    tasks = [
        ('stock', 'all', start_date, end_date),  # 获取所有股票数据
        ('index', 'sh000001', start_date, end_date)  # 获取上证指数数据
    ]

    data_reader_instance = data_reader.DataReader()
    output_instance = output.Output()

    # 读取数据
    stock_data = data_reader_instance.get_data(tasks[0][0], tasks[0][1], tasks[0][2], tasks[0][3])
    index_data = data_reader_instance.get_data(tasks[1][0], tasks[1][1], tasks[1][2], tasks[1][3])

    if stock_data.empty or index_data.empty:
        logger.error("无法获取所需数据")
        return

    # 运行分析
    analyzer = deep_down_analysis.DeepDownAnalyzer()
    results = analyzer.analyze(stock_data, index_data)

    # 输出结果
    output_instance.output_analysis(
        results,
        mode=output_mode,
        filename=filename,
        db_session=db_session
    )

def main():
    """主函数"""
    # 示例：运行深度下跌策略分析并输出到CSV
    run_deep_down_analysis(
        start_date='20200101',
        end_date='20240214',
        output_mode=output.OutputMode.CSV,
        filename='deep_down_analysis_2024.csv'
    )

if __name__ == '__main__':
    main()