"""
strategy/magic_nine.py

魔术九转选股策略的实现。
"""

import pandas as pd
from tqdm import tqdm


class MagicNineStrategy:
    """
    魔术九转策略实现，用于计算买入和卖出信号。
    """

    @staticmethod
    def calculate_nine_reversal(df: pd.DataFrame) -> pd.DataFrame:
        """
        计算九转买入和卖出信号。

        :param df: 包含股票数据的 DataFrame，必须包含 'close' 列。
        :return: 添加了 'buy_count' 和 'sell_count' 列的 DataFrame。
        """
        df['close_4_days_ago'] = df['close'].shift(4)
        df['buy_count'] = 0
        df['sell_count'] = 0
        buy_count = 0
        sell_count = 0

        with tqdm(range(len(df)), desc="计算九转信号", leave=False, ncols=100) as pbar:
            for i in pbar:
                if pd.notna(df['close_4_days_ago'].iloc[i]):
                    # 买入计数
                    if df['close'].iloc[i] < df['close_4_days_ago'].iloc[i]:
                        buy_count += 1
                    else:
                        buy_count = 0
                    df.loc[df.index[i], 'buy_count'] = buy_count

                    # 卖出计数
                    if df['close'].iloc[i] > df['close_4_days_ago'].iloc[i]:
                        sell_count += 1
                    else:
                        sell_count = 0
                    df.loc[df.index[i], 'sell_count'] = sell_count

        return df

    @staticmethod
    def find_signals(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        找出九转买入和卖出信号。

        :param df: 包含 'buy_count' 和 'sell_count' 列的 DataFrame。
        :return: 两个 DataFrame，分别包含买入信号和卖出信号。
        """
        buy_signals = df[df['buy_count'] == 9][['date', 'symbol', 'close']]
        sell_signals = df[df['sell_count'] == 9][['date', 'symbol', 'close']]
        return buy_signals, sell_signals