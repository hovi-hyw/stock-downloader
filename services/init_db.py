import os
import sys
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from Config.config import DATABASE_URL
from models import Base
# 获取项目根目录的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 确保可以导入项目模块
sys.path.append(BASE_DIR)

def init_database():
    """
    自动初始化数据库表结构
    """
    print(f"当前工作目录: {os.getcwd()}")
    print(f"项目根目录: {BASE_DIR}")

    # 显式导入模型
    print("开始导入模型...")
    from models.index_model import IndexDaily
    print("模型导入完成")

    # 验证模型是否正确注册
    print(f"注册的表: {Base.metadata.tables.keys()}")

    # 创建数据库引擎
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True 将显示SQL语句

    print("开始创建所有表...")
    try:
        Base.metadata.create_all(engine)
        print("所有表创建完成")
    except Exception as e:
        print(f"创建表失败: {str(e)}")
        raise


if __name__ == "__main__":
    init_database()