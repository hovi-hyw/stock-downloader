import akshare as ak
import pandas as pd
from pathlib import Path
import os
from typing import Union, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Config.config import DATABASE_URL
from models import Base, IndexDaily


def save_to_database(data: Union[pd.DataFrame, Dict[str, pd.DataFrame]]) -> None:
    """将指数数据保存到数据库

    支持保存单个指数数据或多个指数数据。如果数据已存在，则进行更新操作。

    Args:
        data: 可以是单个指数的DataFrame，或者包含多个指数数据的字典(键为指数代码)

    Raises:
        ValueError: 当输入数据格式不正确或数据为空时抛出
        RuntimeError: 当数据库操作失败时抛出
    """
    # 创建数据库引擎和会话
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 处理单个DataFrame的情况
        if isinstance(data, pd.DataFrame):
            data_dict = {data['code'].iloc[0]: data}
        else:
            data_dict = data

        # 批量保存数据
        for code, df in data_dict.items():
            for _, row in df.iterrows():
                # 创建IndexDaily实例
                index_daily = IndexDaily(
                    code=row['code'],
                    trade_date=row['trade_date'],
                    name=row['name'],
                    open=row['open'],
                    close=row['close'],
                    high=row['high'],
                    low=row['low'],
                    volume=row['volume'],
                    amount=row['amount'],
                    amplitude=row['amplitude'],
                    pct_change=row['pct_change'],
                    price_change=row['price_change'],
                    turnover_rate=row['turnover_rate']
                )

                # 尝试更新已存在的记录，如果不存在则插入
                session.merge(index_daily)

        # 提交事务
        session.commit()

    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Failed to save data to database: {str(e)}")

    finally:
        session.close()


class IndexDataManager:
    def __init__(self, index_series_name="沪深重要指数"):
        """初始化数据管理器"""
        self.index_series_name = index_series_name  # 指数系列名称
        self.base_path = Path("Config")
        self.base_path.mkdir(exist_ok=True)

    def get_index_codes_and_names(self):
        """获取指数代码和名称，并保存为CSV文件"""
        csv_filename = self.base_path / f"{self.index_series_name}.csv"

        # 检查CSV文件是否存在
        if csv_filename.exists():
            print(f"CSV文件 {csv_filename} 已存在，直接读取...")
            df = pd.read_csv(csv_filename)
        else:
            print(f"CSV文件 {csv_filename} 不存在，正在下载指数代码和名称...")
            # 获取指定系列指数的代码和名称
            df = ak.stock_zh_index_spot_em(symbol=self.index_series_name)
            # 只取指数代码和名称
            df = df[['代码', '名称']]
            # 保存为CSV文件
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"指数代码和名称已保存到 {csv_filename}")
        return df

    def clean_index_code(self, code):
        """清理指数代码，确保为纯数字并补全为6位"""
        # 去除非数字字符
        code = ''.join(filter(str.isdigit, str(code)))
        # 补全为6位
        return code.zfill(6)

    def save_single_index_data(self, code, name, hist_data):
        """将单个指数的历史数据保存到数据库 using sqlalchemy"""
        try:
            # Prepare data for save_to_database function
            hist_data['code'] = code
            hist_data['name'] = name
            hist_data.rename(columns={'date': 'trade_date'}, inplace=True) # rename date to trade_date to match model
            save_to_database(hist_data)
            print(f"指数代码 {code} ({name}) 的数据已成功写入数据库表 index_daily！")
        except Exception as e:
            print(f"指数代码 {code} ({name}) 的数据写入失败: {str(e)}")

    def get_and_save_index_historical_data(self):
        """遍历CSV文件中的指数代码，获取历史数据并保存到数据库"""
        csv_filename = self.base_path / f"{self.index_series_name}.csv"

        # 读取CSV文件
        df = pd.read_csv(csv_filename)

        for index, row in df.iterrows():
            raw_code = row['代码']
            name = row['名称']
            # 清理指数代码
            cleaned_code = self.clean_index_code(raw_code)
            print(f"正在获取指数代码 {cleaned_code} ({name}) 的历史数据...")
            try:
                # 获取历史数据
                hist_data = ak.index_zh_a_hist(symbol=cleaned_code)
                # 检查是否成功获取数据
                if hist_data is None or hist_data.empty:
                    print(f"指数代码 {cleaned_code} 的历史数据为空，跳过...")
                    continue
                # 只取需要的字段 and rename to match with model and save_to_database function
                hist_data = hist_data[['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']]
                # 重命名列名为英文 and snake_case to match model and save_to_database function
                hist_data.rename(columns={
                    '日期': 'date',
                    '开盘': 'open',
                    '收盘': 'close',
                    '最高': 'high',
                    '最低': 'low',
                    '成交量': 'volume',
                    '成交额': 'amount',
                    '振幅': 'amplitude',
                    '涨跌幅': 'pct_change',
                    '涨跌额': 'price_change',
                    '换手率': 'turnover_rate'
                }, inplace=True)
                # Convert '日期' to datetime if needed. If 'save_to_database' expects datetime, convert here
                hist_data['date'] = pd.to_datetime(hist_data['date'])


                # 保存到数据库
                self.save_single_index_data(cleaned_code, name, hist_data)
            except Exception as e:
                print(f"获取指数代码 {cleaned_code} 的历史数据失败: {e}")


# 主函数
def main():
    # 设置指数系列名称
    index_series_name = "沪深重要指数"  # 可以修改为其他指数系列名称，如 "中证系列指数"

    # 初始化数据管理器
    manager = IndexDataManager(index_series_name)

    # 第一步：获取指数代码和名称
    print("第一步：获取指数代码和名称...")
    index_codes_and_names = manager.get_index_codes_and_names()

    # 第二步：获取历史数据并保存到数据库
    print("第二步：获取历史数据并保存到数据库...")
    manager.get_and_save_index_historical_data()
    print("数据保存到数据库完成！")


if __name__ == "__main__":
    main()