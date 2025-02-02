def save_stock_daily_data_to_db(self, stock_data, symbol):
    """保存股票日数据到数据库，仅更新日期较新的数据"""
    try:
        logger.info(f"Saving daily data for stock {symbol} to database...")
        db: Session = next(get_db())
        for _, row in stock_data.iterrows():
            existing_record = db.query(StockDailyData).filter_by(symbol=symbol, date=row["date"]).first()
            if existing_record:
                # 如果存在记录，检查日期
                if row["date"] > existing_record.date:
                    # 更新字段，只更新日期更大的记录
                    existing_record.open = row["open"]
                    existing_record.close = row["close"]
                    existing_record.high = row["high"]
                    existing_record.low = row["low"]
                    existing_record.volume = row["volume"]
                    existing_record.amount = row["amount"]
                    existing_record.outstanding_share = row["outstanding_share"]
                    existing_record.turnover = row["turnover"]
                    logger.info(f"Updated existing record for {symbol} on {row['date']}")
            else:
                # 如果不存在记录，直接插入
                db.add(StockDailyData(
                    symbol=symbol,
                    date=row["date"],
                    open=row["open"],
                    close=row["close"],
                    high=row["high"],
                    low=row["low"],
                    volume=row["volume"],
                    amount=row["amount"],
                    outstanding_share=row["outstanding_share"],
                    turnover=row["turnover"]
                ))
                logger.info(f"Inserted new record for {symbol} on {row['date']}")
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save daily data for stock {symbol} to database: {e}")
        raise DataSaveError(f"Failed to save daily data for stock {symbol} to database: {e}")