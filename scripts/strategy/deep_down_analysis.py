"""
strategy/deep_down_analysis.py

深度下跌策略的横向分析实现，用于统计每日命中策略的股票数量。
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from .deep_down import DeepDownStrategy


class DeepDownAnalyzer:
    """
    深度下跌策略横向分析实现，用于统计每日选股结果。
    """

    def analyze(self, stock_data: pd.DataFrame, index_data: pd.DataFrame) -> pd.DataFrame:
        """
        分析每日符合深度下跌策略的股票数量。

        :param stock_data: 包含所有股票数据的 DataFrame
        :param index_data: 包含大盘指数数据的 DataFrame
        :return: DataFrame，包含每日统计结果
        """
        # 使用 DeepDownStrategy 计算信号
        strategy = DeepDownStrategy()
        df = strategy.calculate_signals(stock_data, index_data)

        # 按日期分组统计
        daily_stats = df[df['buy_signal']].groupby('date').agg({
            'symbol': lambda x: list(x),  # 记录所有命中的股票代码
            'buy_signal': 'sum'  # 统计命中数量
        }).reset_index()

        # 重命名列
        daily_stats.columns = ['date', 'symbols', 'count']

        return daily_stats