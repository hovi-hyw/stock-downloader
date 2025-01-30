from db.db_manager import DatabaseManager
from services.save_service import DataSaver
from services.batch_service import BatchProcessor
from services.update_service import UpdateService
import pandas as pd
import os

# 配置
DATABASE_URL = "postgresql://user:password@localhost:5432/stock_db"
STOCK_LIST_FILE = "./data/stock_list.csv"

# 初始化数据库管理器
db_manager = DatabaseManager(DATABASE_URL)
data_saver = DataSaver(db_manager)
batch_processor = BatchProcessor(data_saver)
update_service = UpdateService(STOCK_LIST_FILE)

if __name__ == "__main__":
    # 更新股票列表
    update_service.update_stock_list()

    # 加载股票列表
    stock_list = pd.read_csv(STOCK_LIST_FILE)
    stock_symbols = stock_list['代码'].tolist()

    # 批量下载和保存股票数据
    batch_processor.process_in_batches(symbols=stock_symbols, data_type="stock", batch_size=10, max_workers=3)

    print("所有数据处理完成！")