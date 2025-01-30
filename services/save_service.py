from sqlalchemy.exc import IntegrityError
from db.db_manager import DatabaseManager
from db.models import StockDaily, IndexDaily
import pandas as pd
from sqlalchemy.orm import Session

class DataSaver:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def save_data(self, data: pd.DataFrame, model, unique_keys: list):
        """
        通用数据保存方法，将 Pandas DataFrame 写入数据库。

        Args:
            data (pd.DataFrame): 要保存的数据。
            model: SQLAlchemy 模型类。
            unique_keys (list): 唯一键字段列表，用于避免重复插入。

        Returns:
            int: 成功插入的记录数。
        """
        session: Session = self.db_manager.get_session()
        records_inserted = 0

        try:
            for row in data.itertuples(index=False):
                key_filters = {key: getattr(row, key) for key in unique_keys}
                record = session.query(model).filter_by(**key_filters).first()

                # 如果记录不存在，则插入
                if not record:
                    new_record = model(**row._asdict())
                    session.add(new_record)
                    records_inserted += 1

            session.commit()
            print(f"成功插入 {records_inserted} 条记录")
        except IntegrityError as e:
            session.rollback()
            print(f"数据库完整性错误: {str(e)}")
        except Exception as e:
            session.rollback()
            print(f"保存数据时出错: {str(e)}")
        finally:
            session.close()

        return records_inserted

    def save_stock_data(self, stock_data: pd.DataFrame):
        """
        专门保存股票数据。

        Args:
            stock_data (pd.DataFrame): 股票数据。
        """
        self.save_data(
            data=stock_data,
            model=StockDaily,
            unique_keys=["code", "date"]
        )

    def save_index_data(self, index_data: pd.DataFrame):
        """
        专门保存指数数据。

        Args:
            index_data (pd.DataFrame): 指数数据。
        """
        self.save_data(
            data=index_data,
            model=IndexDaily,
            unique_keys=["code", "trade_date"]
        )