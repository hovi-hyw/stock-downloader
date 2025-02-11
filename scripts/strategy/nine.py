import pandas as pd
from sqlalchemy import select
from datetime import datetime
from tqdm import tqdm
from src.database.models.stock import StockDailyData
from src.database.models.index import IndexDailyData
from src.database.models.concept import ConceptBoardData
from src.database.session import get_db
from src.core.logger import logger


class MagicNineSelector:
    """
    魔术九转选股器，用于计算股票、指数或概念板块的买入和卖出信号。
    """

    def __init__(self):
        """
        初始化数据库连接。
        """
        self.db = next(get_db())

    def calculate_nine_reversal(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算九转买入和卖出信号。

        :param df: 包含股票数据的 DataFrame，必须包含 'close' 列。
        :return: 添加了 'buy_count' 和 'sell_count' 列的 DataFrame。
        """
        df['close_4_days_ago'] = df['close'].shift(4)
        df['buy_count'] = 0
        df['sell_count'] = 0
        buy_count = 0
        sell_count = 0
        found_buy_signals = 0
        found_sell_signals = 0

        with tqdm(
            range(len(df)),
            desc="计算九转信号",
            leave=False,
            position=0,
            ncols=100
        ) as pbar:
            for i in pbar:
                if pd.notna(df['close_4_days_ago'].iloc[i]):
                    # 买入计数（价格低于4天前）
                    if df['close'].iloc[i] < df['close_4_days_ago'].iloc[i]:
                        buy_count += 1
                    else:
                        buy_count = 0
                    df.loc[df.index[i], 'buy_count'] = buy_count
                    if buy_count == 9:
                        found_buy_signals += 1

                    # 卖出计数（价格高于4天前）
                    if df['close'].iloc[i] > df['close_4_days_ago'].iloc[i]:
                        sell_count += 1
                    else:
                        sell_count = 0
                    df.loc[df.index[i], 'sell_count'] = sell_count
                    if sell_count == 9:
                        found_sell_signals += 1

                # 更新进度条的附加信息
                pbar.set_postfix({
                    "买入信号": found_buy_signals,
                    "卖出信号": found_sell_signals
                })
                pbar.update()

        return df

    def find_signals(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        找出九转买入和卖出信号。

        :param df: 包含 'buy_count' 和 'sell_count' 列的 DataFrame。
        :return: 两个 DataFrame，分别包含买入信号和卖出信号。
        """
        buy_signals = df[df['buy_count'] == 9][['date', 'symbol', 'close']]
        sell_signals = df[df['sell_count'] == 9][['date', 'symbol', 'close']]
        return buy_signals, sell_signals

    def get_data_from_db(
        self,
        data_type: str,
        symbol: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        从数据库获取指定类型的数据。

        :param data_type: 数据类型 ('stock', 'index', 'concept')。
        :param symbol: 股票代码 ('all' 或具体代码)。
        :param start_date: 开始日期 (格式: YYYYMMDD)。
        :param end_date: 结束日期 (格式: YYYYMMDD)。
        :return: 包含数据的 DataFrame。如果未找到数据，则返回空 DataFrame。
        """
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

            # 转换为 DataFrame，并显示进度条
            df = pd.DataFrame([{
                'date': getattr(row[0], field_map['date']),
                'close': getattr(row[0], field_map['close']),
                'symbol': getattr(row[0], 'symbol')
            } for row in tqdm(
                data,
                desc=f"加载 {data_type} 数据",
                leave=False,
                position=0,
                ncols=100
            )])
            return df
        except Exception as e:
            logger.error(f"获取数据时发生错误: {str(e)}")
            return pd.DataFrame()

    def scan_signals(
        self,
        data_type: str,
        symbol: str,
        start_date: str,
        end_date: str
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        扫描指定数据类型的买入和卖出信号。

        :param data_type: 数据类型 ('stock', 'index', 'concept')。
        :param symbol: 股票代码 ('all' 或具体代码)。
        :param start_date: 开始日期 (格式: YYYYMMDD)。
        :param end_date: 结束日期 (格式: YYYYMMDD)。
        :return: 两个 DataFrame，分别包含买入信号和卖出信号。
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


def print_signals(buy_signals: pd.DataFrame, sell_signals: pd.DataFrame, data_type: str):
    """
    打印买入和卖出信号。

    :param buy_signals: 包含买入信号的 DataFrame。
    :param sell_signals: 包含卖出信号的 DataFrame。
    :param data_type: 数据类型描述字符串，用于打印标题。
    """
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
    """
    主函数，用于运行魔术九转选股器。
    """
    selector = MagicNineSelector()
    # 示例用法
    data_types = [
        ('stock', 'all', '20250110', '20990101'),  # 单个股票
        # ('index', 'all', '20200101', '20240101'),   # 所有指数
        # ('concept', 'all', '20200101', '20240101'), # 所有概念板块
    ]
    for data_type, symbol, start_date, end_date in tqdm(
        data_types,
        desc="扫描不同类型数据",
        leave=False,
        position=0,
        ncols=100
    ):
        buy_signals, sell_signals = selector.scan_signals(data_type, symbol, start_date, end_date)
        print_signals(buy_signals, sell_signals, f"{data_type.upper()} {symbol}")


if __name__ == "__main__":
    main()