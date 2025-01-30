"""
File: models/index_model.py
"""
from sqlalchemy import Column, String, Float, Date
from .base import Base


class IndexDaily(Base):
    __tablename__ = 'index_daily'

    code = Column(String(10), primary_key=True)
    trade_date = Column(Date, primary_key=True)
    name = Column(String(50))
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