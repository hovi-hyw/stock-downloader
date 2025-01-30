import os
from sqlalchemy import create_engine
from db.models import Base
from config.config import DATABASE_URL

def init_database():
    """
    初始化数据库表结构。如果表不存在则创建。
    """
    print("正在初始化数据库...")
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True 显示所有 SQL 语句

    try:
        # 创建所有表
        Base.metadata.create_all(engine)
        print("数据库初始化完成，表结构已创建。")
    except Exception as e:
        print(f"初始化数据库失败: {str(e)}")
        raise

if __name__ == "__main__":
    init_database()