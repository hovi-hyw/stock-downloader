"""
scripts/strategy.py

主程序，运行选股策略流程。
"""

import pandas as pd

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


def run_deep_down_strategy(stock_data, index_data, output_instance):
    """
    运行 Deep Down 选股策略。
    """
    deep_down_strategy = deep_down.DeepDownStrategy()
    buy_signals = deep_down_strategy.calculate_signals(stock_data, index_data)
    sell_signals = pd.DataFrame()  # Deep Down策略只有买入信号
    output_instance.print_signals(buy_signals, sell_signals, "Deep Down")


def main():
    """
    主函数，运行选股策略。
    """
    # 初始化模块
    data_reader_instance = data_reader.DataReader()
    output_instance = output.Output()

    # 示例任务
    tasks = [
        ('temp', 'all', '20200101', '20250101'),  # 股票数据
        ('index', 'sh000001')  # 上证指数数据
        # 可扩展更多任务
    ]

    # 读取数据
    stock_data = data_reader_instance.get_data(tasks[0][0], tasks[0][1], tasks[0][2], tasks[0][3])
    index_data = data_reader_instance.get_data(tasks[1][0], tasks[1][1], tasks[0][2], tasks[0][3])
    print("读取的数据总量:", len(stock_data))
    print("读取的数据总量:", len(index_data))
    # # 测试一下
    # df = stock_data.copy()
    # # 计算DXJP
    # low_63 = df['low'].rolling(window=63).min()
    # high_44 = df['high'].rolling(window=44).max()
    # df['DXJP'] = (df['close'] - low_63) / (high_44 - low_63) * 100
    #
    # # 计算FS
    # df['FS'] = df['DXJP'].ewm(span=3, adjust=False).mean()
    #
    # # 计算DXJP上穿FS
    # df['CROSS'] = (df['DXJP'] > df['FS']) & (df['DXJP'].shift(1) <= df['FS'].shift(1))
    #
    # # 计算COND1
    # df['COND1'] = (df['CROSS']) & (df['FS'] < 5) & (df['close'].shift(63) != 0)
    #
    # # print("=-==========COND1=======\n\n")
    # # print(df[df['COND1']==True][['CROSS', 'FS', 'close', 'drop_count', 'TJ1', 'COND4']])
    # # print("=-==========COND1=======\n\n")
    #
    # index_df=index_data.copy()
    # # 计算大盘跌幅超过2%的天数
    # index_df['index_drop_98'] = index_df['close'] < index_df['close'].shift(1) * 0.98
    # tj1 = index_df['index_drop_98'].rolling(window=25).sum()
    # df['TJ1'] = tj1
    #
    # # 计算个股跌幅超过4%的天数
    # df['price_drop_96'] = df['close'] < df['close'].shift(1) * 0.96
    # df['drop_count'] = df['price_drop_96'].rolling(window=25).sum()
    #
    # # 计算COND4
    # df['COND4'] = (df['drop_count'] > (df['TJ1'] + 0.5)) & (df['drop_count'] < (df['TJ1'] + 3.5))
    #
    # df['LSXG2'] = (df['close'] > 2) & (df['close'] < df['close'].shift(1) * 1.09)
    #
    # # 最终信号LSMD
    # df['buy_signal'] = df['COND1'] & df['COND4'] & df['LSXG2']
    #
    # print("=-==========COND4=======\n\n")
    # print(df[df['buy_signal']][['date', 'symbol', 'close']])
    # print("=-==========COND4=======\n\n")

    if stock_data.empty:
        print(f"{tasks[0][0]} 数据为空，跳过")
        return

    if index_data.empty:
        print(f"{tasks[1][0]} 数据为空，跳过")
        return

    # 运行策略
    # run_magic_nine_strategy(stock_data.copy(), output_instance)
    run_deep_down_strategy(stock_data.copy(), index_data.copy(), output_instance)

if __name__ == "__main__":
    main()