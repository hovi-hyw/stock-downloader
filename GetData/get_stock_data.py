import akshare as ak

def get_stock_data(
        symbol: str = "sz000001",
        start_date: str = "19900101",
        end_date: str = "20900101",  # 使用未来日期确保获取最新数据
        adjust: str = ""
):
    """
    获取A股历史行情数据（支持复权）

    Args:
        symbol (str): 股票代码，例如 "sz000001" 表示平安银行。
        start_date (str): 起始日期，格式为 "YYYYMMDD"，默认为 "19900101"。
        end_date (str): 结束日期，格式为 "YYYYMMDD"，默认为 "20900101"。
        adjust (str): 复权类型，可选值为：
            - "" (默认，不复权)
            - "hfq" (后复权)
            - "qfq" (前复权)

    Returns:
        pandas.DataFrame: 包含股票历史数据的DataFrame，列名包括：
            - 日期 (date)
            - 开盘价 (open)
            - 最高价 (high)
            - 最低价 (low)
            - 收盘价 (close)
            - 成交量 (volume)
            - 成交额 (amount)
            - 振幅 (amplitude)
            - 涨跌幅 (pct_change)
            - 换手率 (turnover_rate)

    Raises:
        Exception: 如果获取数据时发生错误，抛出异常并打印错误信息。
    """
    try:
        stock_data = ak.stock_zh_a_daily(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )
        return stock_data
    except Exception as e:
        print(f"获取股票数据时出错: {e}")
        return None

# 示例用法
if __name__ == "__main__":
    symbol = "sz000001"  # 平安银行
    start_date = "20200101"
    end_date = "20210101"
    adjust = "qfq"  # 前复权

    stock_data = get_stock_data(symbol, start_date, end_date, adjust)
    if stock_data is not None:
        print(stock_data.head())