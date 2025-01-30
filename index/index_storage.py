"""
File: index/index_storage.py
功能：实现指数数据的数据库存储功能
"""

from typing import Union, Dict
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Config.config import DATABASE_URL
from models import Base, IndexDaily


def save_to_database(data: Union[pd.DataFrame, Dict[str, pd.DataFrame]]) -> None:
    """将指数数据保存到数据库

    支持保存单个指数数据或多个指数数据。如果数据已存在，则进行更新操作。

    Args:
        data: 可以是单个指数的DataFrame，或者包含多个指数数据的字典(键为指数代码)

    Raises:
        ValueError: 当输入数据格式不正确或数据为空时抛出
        RuntimeError: 当数据库操作失败时抛出
    """
    # 创建数据库引擎和会话
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 处理单个DataFrame的情况
        if isinstance(data, pd.DataFrame):
            data_dict = {data['code'].iloc[0]: data}
        else:
            data_dict = data

        # 批量保存数据
        for code, df in data_dict.items():
            for _, row in df.iterrows():
                # 创建IndexDaily实例
                index_daily = IndexDaily(
                    code=row['code'],
                    trade_date=row['trade_date'],
                    name=row['name'],
                    open=row['open'],
                    close=row['close'],
                    high=row['high'],
                    low=row['low'],
                    volume=row['volume'],
                    amount=row['amount'],
                    amplitude=row['amplitude'],
                    pct_change=row['pct_change'],
                    price_change=row['price_change'],
                    turnover_rate=row['turnover_rate']
                )

                # 尝试更新已存在的记录，如果不存在则插入
                session.merge(index_daily)

        # 提交事务
        session.commit()

    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Failed to save data to database: {str(e)}")

    finally:
        session.close()