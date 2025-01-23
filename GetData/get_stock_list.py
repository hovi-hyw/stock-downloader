import akshare as ak

def get_stock_list():
    """
    获取A股市场所有股票的实时行情数据。

    Returns:
        DataFrame: 包含A股市场所有股票的实时行情数据，包括股票代码、名称、最新价、涨跌幅等。
    """
    try:
        stock_data = ak.stock_zh_a_spot()
        return stock_data
    except Exception as e:
        print(f"获取股票列表时出错: {e}")
        return None

# 示例用法
if __name__ == "__main__":
    stock_list = get_stock_list()
    if stock_list is not None:
        print(stock_list.head())