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
        # 复制数据，避免修改原始数据
        df = stock_data.copy()
        index_df = index_data.copy()

        # 数据预处理：删除包含空值的行
        df = df.dropna(subset=['close'])
        index_df = index_df.dropna(subset=['close'])

        # 1. 计算DXJP
        df['min_63d'] = df['close'].rolling(window=63).min()
        df['max_44d'] = df['close'].rolling(window=44).max()
        # 避免除以零
        df['denominator'] = df['max_44d'] - df['min_63d']
        df['DXJP'] = np.where(
            df['denominator'] != 0,
            (df['close'] - df['min_63d']) / df['denominator'] * 100,
            0
        )

        # 2. 计算FS (3日简单移动平均)
        df['FS'] = df['DXJP'].rolling(window=3).mean()

        # 3. 计算DXJP上穿FS
        df['DXJP_cross_FS'] = (df['DXJP'] > df['FS']) & (df['DXJP'].shift(1) <= df['FS'].shift(1))

        # 4. 计算COND1
        df['close_63d_ago'] = df['close'].shift(63)
        df['COND1'] = (df['DXJP_cross_FS']) & (df['FS'] < 5) & (df['close_63d_ago'] != 0)

        # 5. 计算TJ1 (统计25日中大盘跌幅超过2%的天数)
        index_df['index_decline'] = index_df['close'] < index_df['close'].shift(1) * 0.98
        index_df['TJ1'] = index_df['index_decline'].rolling(window=25).sum()

        # 将TJ1合并到股票数据中
        df = pd.merge(df, index_df[['date', 'TJ1']], on='date', how='left')

        # 6. 计算COND4
        df['price_decline'] = df['close'] < df['close'].shift(1) * 0.96
        df['decline_count'] = df['price_decline'].rolling(window=25).sum()
        df['COND4'] = (df['decline_count'] >= (df['TJ1'] + 0.5)) & (df['decline_count'] <= (df['TJ1'] + 3.5))

        # 7. 计算LSXG2
        df['LSXG2'] = (df['close'] > 2) & (df['close'] < df['close'].shift(1) * 1.09)

        # 8. 添加交易量过滤
        df['volume_valid'] = df['volume'] > 0

        # 最终信号
        df['buy_signal'] = (df['COND1'] &
                           df['COND4'] &
                           df['LSXG2'] &
                           df['volume_valid'])

        # 添加调试信息
        df['debug_info'] = ''
        df.loc[df['COND1'], 'debug_info'] += 'COND1 '
        df.loc[df['COND4'], 'debug_info'] += 'COND4 '
        df.loc[df['LSXG2'], 'debug_info'] += 'LSXG2 '
        df.loc[df['volume_valid'], 'debug_info'] += 'VOL_VALID'

        return df

    @staticmethod
    def find_signals(df: pd.DataFrame) -> pd.DataFrame:
        """
        找出买入信号。

        :param df: 包含 'buy_signal' 列的 DataFrame
        :return: DataFrame，包含买入信号和调试信息
        """
        # 筛选出买入信号，并包含更多信息用于分析
        buy_signals = df[df['buy_signal']].copy()

        # 只保留需要的列
        columns_to_keep = [
            'date', 'symbol', 'close', 'DXJP', 'FS',
            'decline_count', 'TJ1', 'debug_info'
        ]

        buy_signals = buy_signals[columns_to_keep]

        # 打印统计信息
        print(f"\n找到 {len(buy_signals)} 个买入信号")
        if not buy_signals.empty:
            print("\n买入信号统计信息:")
            print(f"日期范围: {buy_signals['date'].min()} 到 {buy_signals['date'].max()}")
            print(f"平均DXJP值: {buy_signals['DXJP'].mean():.2f}")
            print(f"平均FS值: {buy_signals['FS'].mean():.2f}")

        return buy_signals