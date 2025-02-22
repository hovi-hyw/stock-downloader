import pandas as pd
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..database.models.stock import StockDailyData
from ..database.models.index import IndexDailyData
from ..database.models.concept import ConceptBoardData
from ..core.logger import logger
from ..core.exceptions import DataSaveError


class DataSaver:
    def save_stock_list_to_csv(self, stock_list, file_path):
        """保存股票列表到 CSV 文件"""
        try:
            logger.info(f"Saving stock list to {file_path}...")
            stock_list.to_csv(file_path, index=False)
        except Exception as e:
            logger.error(f"Failed to save stock list to CSV: {e}")
            raise DataSaveError(f"Failed to save stock list to CSV: {e}")

    def save_index_list_to_csv(self, index_list, file_path):
        """保存指数列表到 CSV 文件"""
        try:
            logger.info(f"Saving index list to {file_path}...")
            index_list.to_csv(file_path, index=False)
        except Exception as e:
            logger.error(f"Failed to save index list to CSV: {e}")
            raise DataSaveError(f"Failed to save index list to CSV: {e}")


    def save_stock_daily_data_to_db(self, stock_data, symbol):
        """保存股票日数据到数据库，仅更新日期较新的数据"""
        try:
            logger.info(f"Saving daily data for stock {symbol} to database...")
            db: Session = next(get_db())
            updated_count = 0
            inserted_count = 0
            for _, row in stock_data.iterrows():
                row_date_str = row["date"]
                row_date = pd.to_datetime(row_date_str, errors='coerce').date()
                if pd.isna(row_date):
                    logger.warning(f"Invalid date format: {row_date_str}")
                    continue

                existing_record = db.query(StockDailyData).filter_by(symbol=symbol, date=row_date).first()
                if existing_record:
                    if row_date > existing_record.date:
                        existing_record.open = row["open"]
                        existing_record.close = row["close"]
                        existing_record.high = row["high"]
                        existing_record.low = row["low"]
                        existing_record.volume = row["volume"]
                        existing_record.amount = row["amount"]
                        existing_record.outstanding_share = row["outstanding_share"]
                        existing_record.turnover = row["turnover"]
                        updated_count += 1
                else:
                    db.add(StockDailyData(
                        symbol=symbol,
                        date=row_date,
                        open=row["open"],
                        close=row["close"],
                        high=row["high"],
                        low=row["low"],
                        volume=row["volume"],
                        amount=row["amount"],
                        outstanding_share=row["outstanding_share"],
                        turnover=row["turnover"]
                    ))
                    inserted_count += 1
            db.commit()
            logger.info(f"Updated {updated_count} records and inserted {inserted_count} new records for stock {symbol}.")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save daily data for stock {symbol} to database: {e}")
            raise DataSaveError(f"Failed to save daily data for stock {symbol} to database: {e}")

    def save_index_daily_data_to_db(self, index_data, symbol, index_name):  # 添加 index_name 参数
        """保存指数日数据到数据库"""
        try:
            logger.info(f"Saving daily data for index {symbol}({index_name}) to database...")
            db: Session = next(get_db())
            updated_count = 0
            inserted_count = 0
            for _, row in index_data.iterrows():
                row_date_str = row["日期"]
                row_date = pd.to_datetime(row_date_str, errors='coerce').date()
                if pd.isna(row_date):
                    logger.warning(f"Invalid date format: {row_date_str}")
                    continue

                existing_record = db.query(IndexDailyData).filter_by(symbol=symbol, date=row_date).first()
                if existing_record:
                    if row_date > existing_record.date:
                        existing_record.open = row["开盘"]
                        existing_record.name = index_name
                        existing_record.close = row["收盘"]
                        existing_record.high = row["最高"]
                        existing_record.low = row["最低"]
                        existing_record.volume = row["成交量"]
                        existing_record.amount = row["成交额"] / 10000.0
                        existing_record.amplitude = row["振幅"]
                        existing_record.change_rate = row["涨跌幅"]
                        existing_record.change_amount = row["涨跌额"]
                        existing_record.turnover_rate = row["换手率"]
                        updated_count += 1
                else:
                    db.add(IndexDailyData(
                        symbol=symbol,
                        name=index_name,
                        date=row_date,
                        open=row["开盘"],
                        close=row["收盘"],
                        high=row["最高"],
                        low=row["最低"],
                        volume=row["成交量"],
                        amount=row["成交额"] / 10000.0,
                        amplitude=row["振幅"],
                        change_rate=row["涨跌幅"],
                        change_amount=row["涨跌额"],
                        turnover_rate=row["换手率"]
                    ))
                    inserted_count += 1
            db.commit()
            logger.info(f"Updated {updated_count} records and inserted {inserted_count} new records for index {symbol}.")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save daily data for index {symbol} to database: {e}")
            raise DataSaveError(f"Failed to save daily data for index {symbol} to database: {e}")


    def save_concept_board_list_to_csv(self, concept_list, file_path):
        """保存概念板块列表到CSV文件"""
        try:
            logger.info(f"Saving concept board list to {file_path}...")
            concept_list.to_csv(file_path, index=False)
        except Exception as e:
            logger.error(f"Failed to save concept board list to CSV: {e}")
            raise DataSaveError(f"Failed to save concept board list to CSV: {e}")


    def save_concept_board_data_to_db(self, board_data, concept_name, concept_code):
        """保存概念板块历史数据到数据库"""
        try:
            logger.info(f"Saving daily data for concept board {concept_name} to database...")
            db: Session = next(get_db())

            for _, row in board_data.iterrows():
                # 转换日期格式
                row_date = pd.to_datetime(row["日期"], errors='coerce').date()
                if pd.isna(row_date):
                    logger.warning(f"Invalid date format: {row['日期']}")
                    continue

                # 检查记录是否存在
                existing_record = db.query(ConceptBoardData).filter_by(
                    concept_code=concept_code,
                    date=row_date
                ).first()

                data = {
                    'concept_name': concept_name,
                    'concept_code': concept_code,
                    'date': row_date,
                    'open': row["开盘"],
                    'close': row["收盘"],
                    'high': row["最高"],
                    'low': row["最低"],
                    'change_rate': row["涨跌幅"],
                    'change_amount': row["涨跌额"],
                    'volume': row["成交量"],
                    'amount': row["成交额"],
                    'amplitude': row["振幅"],
                    'turnover_rate': row["换手率"]
                }

                if existing_record:
                    for key, value in data.items():
                        setattr(existing_record, key, value)
                else:
                    db.add(ConceptBoardData(**data))

            db.commit()
            logger.info(f"Successfully saved data for concept board {concept_name}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save concept board data: {e}")
            raise DataSaveError(f"Failed to save concept board data: {e}")