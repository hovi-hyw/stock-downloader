"""
strategy/deep_down.py

深度下跌选股策略的实现。
"""

import pandas as pd
import numpy as np
from tqdm import tqdm


class DeepDownStrategy:
    """
    深度下跌策略实现，用于计算买入信号。
    """

    @staticmethod
    def calculate_signals(stock_data: pd.DataFrame, index_data: pd.DataFrame) -> pd.DataFrame:
        """
        计算深度下跌买入信号。

        :param stock_data: 包含个股数据的 DataFrame，必须包含 'close' 列
        :param index_data: 包含大盘指数数据的 DataFrame，必须包含 'close' 列
        :return: 添加了信号相关列的 DataFrame
        """
        df = stock_data.copy()

        # 计算DXJP
        df['min_63d'] = df['close'].rolling(window=63).min()
        df['max_44d'] = df['close'].rolling(window=44).max()
        df['DXJP'] = (df['close'] - df['min_63d']) / (df['max_44d'] - df['min_63d']) * 100

        # 计算FS (3日指数移动平均)
        df['FS'] = df['DXJP'].ewm(span=3, adjust=False).mean()

        # 计算DXJP上穿FS
        df['DXJP_cross_FS'] = (df['DXJP'] > df['FS']) & (df['DXJP'].shift(1) <= df['FS'].shift(1))

        # 计算COND1
        df['close_63d_ago'] = df['close'].shift(63)
        df['COND1'] = (df['DXJP_cross_FS']) & (df['FS'] < 5) & (df['close_63d_ago'] != 0)

        # 计算TJ1 (统计25日中大盘跌幅超过2%的天数)
        index_data['index_decline'] = index_data['close'] < index_data['close'].shift(1) * 0.98
        index_data['TJ1'] = index_data['index_decline'].rolling(window=25).sum()

        # 将TJ1合并到股票数据中
        df = pd.merge(df, index_data[['date', 'TJ1']], on='date', how='left')

        # 计算COND4
        df['price_decline'] = df['close'] < df['close'].shift(1) * 0.96
        df['decline_count'] = df['price_decline'].rolling(window=25).sum()
        df['COND4'] = (df['decline_count'] > (df['TJ1'] + 0.5)) & (df['decline_count'] < (df['TJ1'] + 3.5))

        # 计算LSXG2
        df['LSXG2'] = (df['close'] > 2) & (df['close'] < df['close'].shift(1) * 1.09)

        # 最终信号
        df['buy_signal'] = df['COND1'] & df['COND4'] & df['LSXG2']

        return df

    @staticmethod
    def find_signals(df: pd.DataFrame) -> pd.DataFrame:
        """
        找出买入信号。

        :param df: 包含 'buy_signal' 列的 DataFrame
        :return: DataFrame，包含买入信号
        """
        buy_signals = df[df['buy_signal']][['date', 'symbol', 'close']]
        return buy_signals