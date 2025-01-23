import akshare as ak

def get_index_list():
    """
    获取A股市场所有指数的实时行情数据。

    Returns:
        DataFrame: 包含A股市场所有指数的实时行情数据，包括指数代码、名称、最新价、涨跌幅等。
    """
    try:
        index_data = ak.stock_zh_index_spot_sina()
        return index_data
    except Exception as e:
        print(f"获取指数列表时出错: {e}")
        return None

# 示例用法
if __name__ == "__main__":
    index_list = get_index_list()
    if index_list is not None:
        print(index_list.head())