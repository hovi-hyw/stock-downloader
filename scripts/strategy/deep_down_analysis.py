# strategy/deep_down_analysis.py

"""
strategy/deep_down_analysis.py
Deep Down策略分析模块，用于分析每日符合策略的股票。
"""

import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from scripts.strategy.deep_down import DeepDownStrategy


class DeepDownAnalyzer:
    """Deep Down策略分析器"""

    def __init__(self):
        """初始化分析器"""
        self.strategy = DeepDownStrategy()
        self.batch_size = 100  # 每批处理的日期数
        self.worker_count = 4  # 并行工作进程数

    def _process_single_date(self, date, stock_data, index_data):
        """
        处理单个日期的数据

        :param date: 日期
        :param stock_data: 该日期之前的所有股票数据
        :param index_data: 该日期之前的所有指数数据
        :return: 分析结果字典
        """
        try:
            # 按股票分组分析
            day_signals = []

            # 获取当天的所有股票
            current_symbols = stock_data[stock_data['date'] == date]['symbol'].unique()

            for symbol in current_symbols:
                # 获取单个股票的历史数据直到当天
                symbol_data = stock_data[
                    (stock_data['symbol'] == symbol) &
                    (stock_data['date'] <= date)
                    ].copy()

                # 如果数据不足63天，跳过
                if len(symbol_data) < 63:
                    continue

                # 获取对应的指数数据
                current_index_data = index_data[index_data['date'] <= date].copy()

                # 如果指数数据不足25天，跳过
                if len(current_index_data) < 25:
                    continue

                # 计算信号
                data = self.strategy.calculate_signals(symbol_data, current_index_data)

                # 只看当天是否有信号
                if data[data['date'] == date]['buy_signal'].any():
                    day_signals.append(symbol)

            if day_signals:
                return {
                    'date': date,
                    'symbols': ','.join(day_signals),
                    'count': len(day_signals)
                }

        except Exception as e:
            print(f"处理日期 {date} 时发生错误: {str(e)}")

        return None

    def _process_date_batch(self, dates, stock_data, index_data):
        """
        处理一批日期
        """
        results = []
        for date in dates:
            result = self._process_single_date(date, stock_data, index_data)
            if result:
                results.append(result)
        return results

    def analyze(self, stock_data: pd.DataFrame, index_data: pd.DataFrame) -> pd.DataFrame:
        """
        分析每个交易日符合Deep Down策略的股票

        :param stock_data: 股票数据DataFrame
        :param index_data: 指数数据DataFrame
        :return: 包含每日分析结果的DataFrame
        """
        # 确保日期格式统一
        stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date
        index_data['date'] = pd.to_datetime(index_data['date']).dt.date

        # 获取所有唯一日期
        dates = sorted(stock_data['date'].unique())

        # 将日期分批
        date_batches = [dates[i:i + self.batch_size] for i in range(0, len(dates), self.batch_size)]

        all_results = []

        # 使用tqdm显示总体进度
        with tqdm(total=len(dates), desc="分析进度") as pbar:
            # 使用线程池处理每批数据
            with ThreadPoolExecutor(max_workers=self.worker_count) as executor:
                # 提交所有批次的任务
                future_to_batch = {
                    executor.submit(
                        self._process_date_batch,
                        batch,
                        stock_data,
                        index_data
                    ): batch for batch in date_batches
                }

                # 处理完成的任务
                for future in as_completed(future_to_batch):
                    batch = future_to_batch[future]
                    try:
                        batch_results = future.result()
                        all_results.extend(batch_results)
                        pbar.update(len(batch))
                    except Exception as e:
                        print(f'处理批次时发生错误: {str(e)}')

        # 转换为DataFrame并按日期排序
        if all_results:
            results_df = pd.DataFrame(all_results)
            results_df = results_df.sort_values('date')
            return results_df
        else:
            return pd.DataFrame(columns=['date', 'symbols', 'count'])