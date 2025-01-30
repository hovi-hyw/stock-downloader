from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Date

Base = declarative_base()

class StockDaily(Base):
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

class IndexDaily(Base):
    __tablename__ = 'index_daily'
    code = Column(String, primary_key=True)
    trade_date = Column(Date, primary_key=True)
    name = Column(String)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    amount = Column(Float)
    amplitude = Column(Float)
    pct_change = Column(Float)
    price_change = Column(Float)
    turnover_rate = Column(Float)