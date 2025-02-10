import pandas as pd
from sqlalchemy import select
from datetime import datetime
from src.database.models.stock import StockDailyData
from src.database.models.index import IndexDailyData
from src.database.models.concept import ConceptBoardData
from src.database.session import get_db
from src.core.logger import logger


class MagicNineSelector:
    def __init__(self):
        self.db = next(get_db())

    def calculate_nine_reversal(self, df):
        """计算九转买入和卖出信号"""
        df['close_4_days_ago'] = df['close'].shift(4)
        df['buy_count'] = 0
        df['sell_count'] = 0

        buy_count = 0
        sell_count = 0

        for i in range(len(df)):
            if pd.notna(df['close_4_days_ago'].iloc[i]):
                # 买入计数（价格低于4天前）
                if df['close'].iloc[i] < df['close_4_days_ago'].iloc[i]:
                    buy_count += 1
                else:
                    buy_count = 0
                df.loc[df.index[i], 'buy_count'] = buy_count

                # 卖出计数（价格高于4天前）
                if df['close'].iloc[i] > df['close_4_days_ago'].iloc[i]:
                    sell_count += 1
                else:
                    sell_count = 0
                df.loc[df.index[i], 'sell_count'] = sell_count

        return df

    def find_signals(self, df):
        """找出九转买入和卖出信号"""
        buy_signals = df[df['buy_count'] == 9][['date', 'symbol', 'close']]
        sell_signals = df[df['sell_count'] == 9][['date', 'symbol', 'close']]
        return buy_signals, sell_signals

    def get_data_from_db(self, data_type, symbol, start_date, end_date):
        """从数据库获取数据"""
        try:
            # 根据数据类型选择对应的模型和字段映射
            model_map = {
                'stock': (StockDailyData, {'close': 'close', 'date': 'date'}),
                'index': (IndexDailyData, {'close': 'close', 'date': 'date'}),
                'concept': (ConceptBoardData, {'close': 'close', 'date': 'date'})
            }

            if data_type not in model_map:
                raise ValueError(f"不支持的数据类型: {data_type}")

            model, field_map = model_map[data_type]

            # 构建查询
            query = select(model)
            if symbol.lower() != 'all':
                query = query.where(model.symbol == symbol)
            query = query.where(
                model.date >= start_date,
                model.date <= end_date
            ).order_by(model.date)

            # 执行查询
            result = self.db.execute(query)
            data = result.all()

            if not data:
                logger.warning(f"未找到数据: {data_type} {symbol}")
                return pd.DataFrame()

            # 转换为DataFrame
            df = pd.DataFrame([{
                'date': getattr(row[0], field_map['date']),
                'close': getattr(row[0], field_map['close']),
                'symbol': getattr(row[0], 'symbol')
            } for row in data])

            return df

        except Exception as e:
            logger.error(f"获取数据时发生错误: {str(e)}")
            return pd.DataFrame()

    def scan_signals(self, data_type, symbol, start_date, end_date):
        """
        扫描信号
        :param data_type: 数据类型 ('stock', 'index', 'concept')
        :param symbol: 代码 ('all' 或具体代码)
        :param start_date: 开始日期 (YYYYMMDD)
        :param end_date: 结束日期 (YYYYMMDD)
        """
        try:
            # 转换日期格式
            start_date = datetime.strptime(start_date, '%Y%m%d').date()
            end_date = datetime.strptime(end_date, '%Y%m%d').date()

            # 获取数据
            df = self.get_data_from_db(data_type, symbol, start_date, end_date)

            if df.empty:
                return pd.DataFrame(), pd.DataFrame()

            # 计算信号
            df = self.calculate_nine_reversal(df)
            buy_signals, sell_signals = self.find_signals(df)

            return buy_signals, sell_signals

        except Exception as e:
            logger.error(f"扫描信号时发生错误: {str(e)}")
            return pd.DataFrame(), pd.DataFrame()


def print_signals(buy_signals, sell_signals, data_type):
    """打印信号"""
    print(f"\n=== {data_type} 九转买入信号 ===")
    if not buy_signals.empty:
        for _, signal in buy_signals.iterrows():
            print(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
    else:
        print("没有发现买入信号")

    print(f"\n=== {data_type} 九转卖出信号 ===")
    if not sell_signals.empty:
        for _, signal in sell_signals.iterrows():
            print(f"代码: {signal['symbol']}, 日期: {signal['date']}, 收盘价: {signal['close']:.2f}")
    else:
        print("没有发现卖出信号")


def main():
    selector = MagicNineSelector()

    # 示例用法
    data_types = [
        ('stock', '600552', '19900101', '20240101'),  # 单个股票
        # ('index', 'all', '20200101', '20240101'),   # 所有指数
        # ('concept', 'all', '20200101', '20240101'), # 所有概念板块
    ]

    for data_type, symbol, start_date, end_date in data_types:
        buy_signals, sell_signals = selector.scan_signals(data_type, symbol, start_date, end_date)
        print_signals(buy_signals, sell_signals, f"{data_type.upper()} {symbol}")


if __name__ == "__main__":
    main()