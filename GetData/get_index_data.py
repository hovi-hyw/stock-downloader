import akshare as ak

def get_index_data(symbol, period="daily", start_date="19900101", end_date="20900101"):
    """
    获取指定指数的历史数据。

    Args:
        symbol (str): 指数代码，例如 "sh000001" 表示上证指数。
        period (str): 数据周期，可选值为 "daily"（日线）, "weekly"（周线）, "monthly"（月线）。
        start_date (str): 数据开始日期，格式为 "YYYYMMDD"。
        end_date (str): 数据结束日期，格式为 "YYYYMMDD"。

    Returns:
        DataFrame: 包含指定指数的历史数据，包括日期、开盘价、收盘价、最高价、最低价等。
    """
    try:
        index_data = ak.index_zh_a_hist(symbol, period, start_date, end_date)
        return index_data
    except Exception as e:
        print(f"获取指数数据时出错: {e}")
        return None

# 示例用法
if __name__ == "__main__":
    symbol = "sh000001"  # 上证指数
    index_data = get_index_data(symbol)
    if index_data is not None:
        print(index_data.head())