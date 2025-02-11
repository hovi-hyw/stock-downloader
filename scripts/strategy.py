"""
scripts/strategy.py

主程序，运行选股策略流程。
"""

from strategy.data_reader import DataReader
from strategy.magic_nine import MagicNineStrategy
from strategy.output import Output


def main():
    """
    主函数，运行选股策略。
    """
    # 初始化模块
    reader = DataReader()
    strategy = MagicNineStrategy()
    output = Output()

    # 示例任务
    tasks = [
        ('index', 'all', '20240101', '20990110'),  # 股票数据
        # 可扩展更多任务
    ]

    for data_type, symbol, start_date, end_date in tasks:
        # 读取数据
        data = reader.get_data(data_type, symbol, start_date, end_date)
        if data.empty:
            print(f"{data_type} 数据为空，跳过")
            continue

        # 应用策略
        data = strategy.calculate_nine_reversal(data)
        buy_signals, sell_signals = strategy.find_signals(data)

        # 输出结果
        output.print_signals(buy_signals, sell_signals, "Magic Nine")


if __name__ == "__main__":
    main()