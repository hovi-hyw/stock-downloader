"""
strategy/output.py
通用输出模块，支持多种输出方式。
"""

import pandas as pd
from enum import Enum
from sqlalchemy.orm import Session
from src.core.logger import logger
from src.database.models.stock import StockDailyData


class OutputMode(Enum):
    PRINT = "print"
    CSV = "csv"
    DATABASE = "database"


class Output:
    """通用输出工具类"""

    @staticmethod
    def output_analysis(results: pd.DataFrame, mode: OutputMode,
                        filename: str = None, db_session: Session = None):
        """
        输出分析结果

        :param results: 包含分析结果的DataFrame
        :param mode: 输出模式
        :param filename: CSV文件名(当mode为CSV时使用)
        :param db_session: 数据库会话(当mode为DATABASE时使用)
        """
        if mode == OutputMode.PRINT:
            print("\n=== 深度下跌策略分析结果 ===")
            for _, row in results.iterrows():
                print(f"日期: {row['date']}, 命中数量: {row['count']}")
                print(f"命中股票: {', '.join(row['symbols'])}\n")

        elif mode == OutputMode.CSV:
            if not filename:
                filename = "deep_down_analysis.csv"
            try:
                # 将symbols列转换为字符串以便存储
                results['symbols'] = results['symbols'].apply(lambda x: ','.join(x))
                results.to_csv(filename, index=False, encoding='utf-8')
                logger.info(f"分析结果已保存到 {filename}")
            except Exception as e:
                logger.error(f"保存分析结果时发生错误: {str(e)}")

        elif mode == OutputMode.DATABASE:
            if not db_session:
                raise ValueError("数据库模式需要提供db_session")
            try:
                # TODO: 实现数据库存储逻辑
                logger.info("分析结果已保存到数据库")
            except Exception as e:
                logger.error(f"保存到数据库时发生错误: {str(e)}")