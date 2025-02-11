"""
strategy/data_reader.py

通用数据读取模块，用于从数据库加载股票、指数或概念板块数据。
"""

from sqlalchemy import select
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from src.database.models.stock import StockDailyData
from src.database.models.index import IndexDailyData
from src.database.models.concept import ConceptBoardData
from src.database.session import get_db
from src.core.logger import logger


class DataReader:
    """
    通用数据读取器，用于从数据库加载数据。
    """

    def __init__(self):
        self.db = next(get_db())

    def get_data(self, data_type: str, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        从数据库获取指定类型的数据。

        :param data_type: 数据类型 ('stock', 'index', 'concept')。
        :param symbol: 股票代码 ('all' 或具体代码)。
        :param start_date: 开始日期 (格式: YYYYMMDD)。
        :param end_date: 结束日期 (格式: YYYYMMDD)。
        :return: 包含数据的 DataFrame。如果未找到数据，则返回空 DataFrame。
        """
        try:
            model_map = {
                'stock': (StockDailyData, {'close': 'close', 'date': 'date'}),
                'index': (IndexDailyData, {'close': 'close', 'date': 'date'}),
                'concept': (ConceptBoardData, {'close': 'close', 'date': 'date'}),
            }
            if data_type not in model_map:
                raise ValueError(f"不支持的数据类型: {data_type}")
            model, field_map = model_map[data_type]

            query = select(model)
            if symbol.lower() != 'all':
                query = query.where(model.symbol == symbol)
            query = query.where(
                model.date >= datetime.strptime(start_date, '%Y%m%d').date(),
                model.date <= datetime.strptime(end_date, '%Y%m%d').date(),
            ).order_by(model.date)

            result = self.db.execute(query)
            data = result.all()
            if not data:
                logger.warning(f"未找到数据: {data_type} {symbol}")
                return pd.DataFrame()

            df = pd.DataFrame(
                [
                    {
                        'date': getattr(row[0], field_map['date']),
                        'close': getattr(row[0], field_map['close']),
                        'symbol': getattr(row[0], 'symbol'),
                    }
                    for row in tqdm(data, desc=f"加载 {data_type} 数据", leave=False, ncols=100)
                ]
            )
            return df

        except Exception as e:
            logger.error(f"获取数据时发生错误: {str(e)}")
            return pd.DataFrame()