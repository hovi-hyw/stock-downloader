# models/stock_model.py
from sqlalchemy import Column, String, Float, Date
from models import Base


class StockDaily(Base):
    """股票日线数据模型类

    用于存储股票的日线交易数据，包括开高低收、成交量、成交额等信息。

    Attributes:
        code (str): 股票代码
        date (Date): 交易日期
        open (float): 开盘价
        high (float): 最高价
        low (float): 最低价
        close (float): 收盘价
        volume (float): 成交量
        amount (float): 成交额
        outstanding_share (float): 流通股本
        turnover (float): 换手率
    """

    __tablename__ = 'stock_daily'

    code = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    amount = Column(Float)
    outstanding_share = Column(Float)
    turnover = Column(Float)