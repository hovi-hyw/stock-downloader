# SaveData/save_stock_list_to_csv.py

import os
from datetime import datetime, timedelta
from GetData import get_stock_list
from Config.config import STOCK_LIST_CACHE

def save_stock_list_to_csv(max_days=100, file_path=STOCK_LIST_CACHE):
    """
    下载股票列表并保存为CSV文件。
    如果文件存在且未超过指定天数，则直接读取文件；否则重新下载并更新文件。

    Args:
        max_days (int): 文件的最大有效天数，默认为100天。
        file_path (str): CSV文件的保存路径，默认为相对路径： "Config/stock_list.csv"。
    """
    try:
        file_path = os.path.join(r"../",file_path)
        # 检查文件是否存在且是否超过指定天数
        if os.path.exists(file_path):
            # 获取文件的最后修改时间
            file_mod_time = os.path.getmtime(file_path)
            file_mod_date = datetime.fromtimestamp(file_mod_time)

            # 计算当前时间与文件修改时间的差值
            time_difference = datetime.now() - file_mod_date

            # 如果文件未超过指定天数，直接返回
            if time_difference <= timedelta(days=max_days):
                print(f"文件 {file_path} 存在且未超过 {max_days} 天，直接读取该文件。")
                return

        # 获取股票列表
        stock_list = get_stock_list()

        # 检查是否成功获取数据
        if stock_list is not None:
            # 保存为CSV文件
            stock_list.to_csv(file_path, index=False, encoding="utf_8_sig")
            print(f"股票列表已保存到 {file_path}")
        else:
            print("获取股票列表失败，未保存文件。")
    except Exception as e:
        print(f"保存股票列表时出错: {e}")

# 示例用法
if __name__ == "__main__":
    save_stock_list_to_csv()