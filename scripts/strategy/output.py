# strategy/output.py

"""
strategy/output.py
通用输出模块，用于输出选股策略的结果。
"""

import pandas as pd
from src.core.logger import logger


class Output:
    """通用输出工具类"""

    @staticmethod
    def print_signals(buy_signals: pd.DataFrame, sell_signals: pd.DataFrame, strategy_name: str):
        """打印买入和卖出信号"""
        print(f"\n=== {strategy_name} 策略 - 买入信号 ===")
        logger.info(f"\n=== {strategy_name} 策略 - 买入信号 ===")
        if not buy_signals.empty:
            for _, signal in buy_signals.iterrows():
                print(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
                logger.info(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
        else:
            print("没有发现买入信号")

        if not sell_signals.empty:
            print(f"\n=== {strategy_name} 策略 - 卖出信号 ===")
            logger.info(f"\n=== {strategy_name} 策略 - 卖出信号 ===")
            for _, signal in sell_signals.iterrows():
                print(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
                logger.info(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
        else:
            print("没有发现卖出信号")

    @staticmethod
    def save_analysis_to_csv(results: pd.DataFrame, filename: str):
        """
        将分析结果保存为CSV文件

        :param results: 包含分析结果的DataFrame，需要包含date、symbols和count列
        :param filename: 输出文件名
        """
        try:
            results.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"分析结果已保存到 {filename}")
        except Exception as e:
            logger.error(f"保存分析结果时发生错误: {str(e)}")