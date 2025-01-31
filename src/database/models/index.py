from sqlalchemy import Column, String, Float, Date, Integer
from ..base import Base

class IndexDailyData(Base):
    __tablename__ = "index_daily_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False)  # 指数代码
    date = Column(Date, nullable=False)      # 日期
    open = Column(Float)                     # 开盘价
    close = Column(Float)                    # 收盘价
    high = Column(Float)                     # 最高价
    low = Column(Float)                      # 最低价
    volume = Column(Float)                   # 成交量
    amount = Column(Float)                   # 成交额
    amplitude = Column(Float)                # 振幅
    change_rate = Column(Float)              # 涨跌幅
    change_amount = Column(Float)            # 涨跌额
    turnover_rate = Column(Float)            # 换手率

    def __repr__(self):
        return f"<IndexDailyData(symbol={self.symbol}, date={self.date})>"