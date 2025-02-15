"""
strategy/output.py
通用输出模块，支持多种输出方式。
"""

import pandas as pd
from enum import Enum
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Float, Date, Table
from src.core.logger import logger
from src.database.base import Base
from src.database.session import create_tables, get_db

class OutputMode(Enum):
    PRINT = "print"
    CSV = "csv"
    DATABASE = "database"

class Output:
    """通用输出工具类"""

    @staticmethod
    def _create_dynamic_model(table_name: str, df: pd.DataFrame):
        """
        根据DataFrame动态创建SQLAlchemy模型类

        :param table_name: 表名
        :param df: 数据框
        :return: SQLAlchemy模型类
        """
        # 动态创建模型类属性
        attrs = {
            '__tablename__': table_name,
            '__table_args__': {'extend_existing': True}
        }

        # 处理DataFrame中的每一列，映射到对应的SQLAlchemy类型
        for col_name, dtype in df.dtypes.items():
            if 'datetime' in str(dtype) or 'date' in str(dtype):
                attrs[col_name] = Column(col_name, Date)
            elif 'float' in str(dtype):
                attrs[col_name] = Column(col_name, Float)
            else:
                attrs[col_name] = Column(col_name, String)

        # 动态创建模型类
        model = type(f'Dynamic{table_name.title()}', (Base,), attrs)
        return model

    @staticmethod
    def output_analysis(results: pd.DataFrame, mode: OutputMode,
                       filename: str = None, db_session: Session = None,
                       table_name: str = "analysis_results"):
        """
        输出分析结果

        :param results: 包含分析结果的DataFrame
        :param mode: 输出模式
        :param filename: CSV文件名(当mode为CSV时使用)
        :param db_session: 数据库会话(当mode为DATABASE时使用)
        :param table_name: 数据库表名(当mode为DATABASE时使用)
        """
        if mode == OutputMode.PRINT:
            print("\n=== 深度下跌策略分析结果 ===")
            for _, row in results.iterrows():
                print(f"日期: {row['date']}, 命中数量: {row['count']}")
                print(f"命中股票: {', '.join(row['symbols'])}\n")

        elif mode == OutputMode.CSV:
            if not filename:
                filename = "deep_down_analysis.csv"
            try:
                # 将symbols列转换为字符串以便存储
                results['symbols'] = results['symbols'].apply(lambda x: ','.join(x) if isinstance(x, (list, tuple)) else x)
                results.to_csv(filename, index=False, encoding='utf-8')
                logger.info(f"分析结果已保存到 {filename}")
            except Exception as e:
                logger.error(f"保存分析结果时发生错误: {str(e)}")

        elif mode == OutputMode.DATABASE:
            try:
                if db_session is None:
                    db_session = next(get_db())

                # 创建动态模型类
                DynamicModel = Output._create_dynamic_model(table_name, results)

                # 使用项目现有的create_tables函数创建表
                create_tables()

                # 将DataFrame数据转换为模型实例
                for _, row in results.iterrows():
                    # 处理可能的列表类型数据
                    row_dict = row.to_dict()
                    for key, value in row_dict.items():
                        if isinstance(value, (list, tuple)):
                            row_dict[key] = ','.join(map(str, value))

                    # 创建模型实例并添加到会话
                    model_instance = DynamicModel(**row_dict)
                    db_session.add(model_instance)

                # 提交事务
                db_session.commit()
                logger.info(f"分析结果已成功保存到数据库表 {table_name}")

            except Exception as e:
                if db_session:
                    db_session.rollback()
                logger.error(f"保存到数据库时发生错误: {str(e)}")
                raise
            finally:
                if db_session:
                    db_session.close()