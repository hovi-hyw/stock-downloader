from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import config
from .base import Base

# 创建数据库引擎
engine = create_engine(config.DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建数据库表
def create_tables():
    Base.metadata.create_all(bind=engine)


# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
