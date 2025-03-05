from sqlalchemy import Column, String, Float, Date, Integer, PrimaryKeyConstraint

from ..base import Base


class ConceptBoardData(Base):
    __tablename__ = "concept_board"

    concept_name = Column(String, nullable=False)  # 板块名称
    concept_code = Column(String, nullable=False)  # 板块代码
    date = Column(Date, nullable=False)  # 日期
    open = Column(Float)  # 开盘
    close = Column(Float)  # 收盘
    high = Column(Float)  # 最高
    low = Column(Float)  # 最低
    change_rate = Column(Float)  # 涨跌幅
    change_amount = Column(Float)  # 涨跌额
    volume = Column(Float)  # 成交量
    amount = Column(Float)  # 成交额
    amplitude = Column(Float)  # 振幅
    turnover_rate = Column(Float)  # 换手率
    total_market_value = Column(Float)  # 总市值
    up_count = Column(Integer)  # 上涨家数
    down_count = Column(Integer)  # 下跌家数

    __table_args__ = (
        PrimaryKeyConstraint('concept_code', 'date'),
    )

    def __repr__(self):
        return f"<ConceptBoardData(concept_name={self.concept_name}, date={self.date})>"
