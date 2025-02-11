"""
strategy/output.py

通用输出模块，用于输出选股策略的结果。
"""

import pandas as pd


class Output:
    """
    通用输出工具类，用于打印选股结果。
    """

    @staticmethod
    def print_signals(buy_signals: pd.DataFrame, sell_signals: pd.DataFrame, strategy_name: str):
        """
        打印买入和卖出信号。

        :param buy_signals: 包含买入信号的 DataFrame。
        :param sell_signals: 包含卖出信号的 DataFrame。
        :param strategy_name: 策略名称，用于输出标题。
        """
        print(f"\n=== {strategy_name} 策略 - 买入信号 ===")
        if not buy_signals.empty:
            for _, signal in buy_signals.iterrows():
                print(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
        else:
            print("没有发现买入信号")

        print(f"\n=== {strategy_name} 策略 - 卖出信号 ===")
        if not sell_signals.empty:
            for _, signal in sell_signals.iterrows():
                print(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
        else:
            print("没有发现卖出信号")