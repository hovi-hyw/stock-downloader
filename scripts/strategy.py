# filepath: /d:/codes/Pycharm/stock-insight/scripts/strategy.py
"""
scripts/strategy.py

主程序，运行选股策略流程。
"""
import scripts.strategy.magic_nine as magic_nine
import scripts.strategy.deep_down as deep_down
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

def run_deep_down_strategy(data, output_instance):
    """
    运行 Deep Down 选股策略。
    """


def main():
    """
    主函数，运行选股策略。
    """
    # 初始化模块
    data_reader_instance = data_reader.DataReader()
    output_instance = output.Output()

    # 示例任务
    tasks = [
        ('index', 'all', '20240101', '20990110'),  # 股票数据
        # 可扩展更多任务
    ]

    for data_type, symbol, start_date, end_date in tasks:
        # 读取数据
        data = data_reader_instance.get_data(data_type, symbol, start_date, end_date)
        if data.empty:
            print(f"{data_type} 数据为空，跳过")
            continue

        # 运行策略
        run_magic_nine_strategy(data.copy(), output_instance)  # 传入数据副本，避免修改原始数据
        run_deep_down_strategy(data.copy(), output_instance)

if __name__ == "__main__":
    main()