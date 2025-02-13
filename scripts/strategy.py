"""
scripts/strategy.py

主程序，运行选股策略流程。
"""

import pandas as pd

import scripts.strategy.magic_nine as magic_nine
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
    pass


def main():
    """
    主函数，运行选股策略。
    """

    # 示例任务
    tasks = [
        ('temp', ['sh600522','sh600523'], '20200101', '20250101'),  # 股票数据
        # ('temp', 'all', '20200101', '20250101'),  # 股票数据
        ('index', 'sh000001')  # 上证指数数据
        # 可扩展更多任务
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

    # 运行策略
    run_magic_nine_strategy(stock_data.copy(), output_instance)

if __name__ == "__main__":
    main()