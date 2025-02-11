"""
strategy/deep_down.py

DEEPDOWN选股策略实现。
这是一个结合个股和大盘数据的选股策略，主要用于在市场大幅下跌后寻找超跌反弹的机会。

策略逻辑:
1. 计算个股的动向极品指标(DXJP)，反映个股的超跌程度
2. 结合大盘跌幅统计，确保是在市场调整期间
3. 通过价格条件筛选，避免选中高风险股票

参数说明:
- DXJP: (收盘价-63日内最低价)/(44日内最高价-63日内最低价)*100
- FS: DXJP的3日指数移动平均
- 大盘条件: 统计25日内大盘跌幅超过2%的天数
- 个股条件: 统计25日内个股跌幅超过4%的天数，且需要在特定范围内
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from typing import List, Tuple, Optional
from datetime import datetime, timedelta


class DeepDownStrategy:
    """DEEPDOWN策略实现"""

    def __init__(self):
        """初始化策略参数"""
        self.required_history_days = 63  # 需要的历史数据天数
        self.index_code = 'sh000001'  # 默认使用上证指数

    def calculate_signals(self,
                          data_reader,
                          market_type: str = 'stock',
                          start_date: str = None,
                          end_date: str = None,
                          index_code: str = None) -> pd.DataFrame:
        """
        计算指定市场的所有股票的买入信号

        参数:
            data_reader: 数据读取器实例
            market_type: 市场类型，可选 'stock'(股票),'index'(指数),'concept'(概念板块)
            start_date: 开始日期，格式YYYYMMDD
            end_date: 结束日期，格式YYYYMMDD
            index_code: 参考大盘指数代码，默认使用上证指数

        返回:
            DataFrame: 包含买入信号的数据框
        """
        if index_code:
            self.index_code = index_code

        # 如果未指定日期，使用当前日期往前推
        if not end_date:
            end_date = datetime.now().strftime('%Y%m%d')
        if not start_date:
            start_date = (datetime.strptime(end_date, '%Y%m%d') -
                          timedelta(days=self.required_history_days)).strftime('%Y%m%d')

        # 获取指数数据
        index_data = data_reader.get_data('index', self.index_code, start_date, end_date)
        if index_data.empty:
            raise ValueError(f"无法获取指数数据: {self.index_code}")

        # 获取市场所有标的数据
        market_data = data_reader.get_data(market_type, 'all', start_date, end_date)
        if market_data.empty:
            raise ValueError(f"无法获取{market_type}市场数据")

        # 按股票代码分组处理
        signals = []
        unique_symbols = market_data['symbol'].unique()

        for symbol in tqdm(unique_symbols, desc="计算选股信号"):
            stock_data = market_data[market_data['symbol'] == symbol]
            if len(stock_data) < self.required_history_days:
                continue

            result = self._calculate_single_stock(stock_data, index_data)
            if not result.empty:
                signals.append(result)

        if not signals:
            return pd.DataFrame()

        return pd.concat(signals, ignore_index=True)

    def _calculate_single_stock(self, stock_df: pd.DataFrame,
                                index_df: pd.DataFrame) -> pd.DataFrame:
        """
        计算单个股票的DEEPDOWN策略信号
        """
        df = stock_df.copy()

        # 计算DXJP
        low_63 = df['low'].rolling(window=63).min()
        high_44 = df['high'].rolling(window=44).max()
        df['DXJP'] = (df['close'] - low_63) / (high_44 - low_63) * 100

        # 计算FS
        df['FS'] = df['DXJP'].ewm(span=3, adjust=False).mean()

        # 计算DXJP上穿FS
        df['CROSS'] = (df['DXJP'] > df['FS']) & (df['DXJP'].shift(1) <= df['FS'].shift(1))

        # 计算COND1
        df['COND1'] = (df['CROSS']) & (df['FS'] < 5) & (df['close'].shift(63) != 0)

        # 计算大盘跌幅超过2%的天数
        index_df['index_drop_98'] = index_df['close'] < index_df['close'].shift(1) * 0.98
        tj1 = index_df['index_drop_98'].rolling(window=25).sum()
        df['TJ1'] = tj1

        # 计算个股跌幅超过4%的天数
        df['price_drop_96'] = df['close'] < df['close'].shift(1) * 0.96
        df['drop_count'] = df['price_drop_96'].rolling(window=25).sum()

        # 计算COND4
        df['COND4'] = (df['drop_count'] > (df['TJ1'] + 0.5)) & (df['drop_count'] < (df['TJ1'] + 3.5))

        # 计算LSXG2
        df['LSXG2'] = (df['close'] > 2) & (df['close'] < df['close'].shift(1) * 1.09)

        # 最终信号LSMD
        df['buy_signal'] = df['COND1'] & df['COND4'] & df['LSXG2']

        # 只返回有买入信号的记录
        return df[df['buy_signal']][['date', 'symbol', 'close']]