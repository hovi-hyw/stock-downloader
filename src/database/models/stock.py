from sqlalchemy import Column, String, Float, Date, PrimaryKeyConstraint

from src.database.base import Base


class StockDailyData(Base):
    __tablename__ = "stock_daily_data"

    symbol = Column(String, nullable=False)  # 股票代码
    date = Column(Date, nullable=False)  # 日期
    open = Column(Float)  # 开盘价
    close = Column(Float)  # 收盘价
    high = Column(Float)  # 最高价
    low = Column(Float)  # 最低价
    volume = Column(Float)  # 成交量
    amount = Column(Float)  # 成交额
    outstanding_share = Column(Float)  # 流通股本stock.py
    turnover = Column(Float)  # 换手率

    __table_args__ = (
        PrimaryKeyConstraint('symbol', 'date'),
    )

    def __repr__(self):
        return f"<StockDailyData(symbol={self.symbol}, date={self.date})>"
