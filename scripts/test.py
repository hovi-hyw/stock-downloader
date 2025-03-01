import time

import akshare as ak
import pandas as pd


def get_concept_board_names():
    """获取概念板块名称和代码"""
    concept_df = ak.stock_board_concept_name_em()
    return concept_df


def get_concept_board_data(symbol, board_name):
    """
    获取概念板块历史数据并计算上涨比例
    :param symbol: 板块代码
    :param board_name: 板块名称
    :return: pandas DataFrame
    """
    print(f"尝试获取板块代码为 {symbol} ({board_name}) 的历史数据...")  # 调试信息

    try:
        hist_df = ak.stock_board_concept_hist_em(symbol=board_name, start_date='20250201', end_date='20990101')
        print("DONE!!!")
    except IndexError as e:
        print(f"Error: 获取板块 {board_name} ({symbol}) 历史数据时发生 IndexError: {e}")
        print(f"Error: 可能是板块代码 {symbol} 不正确或 akshare 无法识别。")
        return None
    except Exception as e:  # 捕获其他可能发生的异常
        print(f"Error: 获取板块 {board_name} ({symbol}) 历史数据时发生未知错误: {e}")
        return None

    if hist_df is not None and not hist_df.empty:
        # 计算上涨比例
        hist_df['上涨比例'] = hist_df['上涨家数'] / (hist_df['上涨家数'] + hist_df['下跌家数'])
        # 添加板块名称和代码列
        hist_df['板块名称'] = board_name
        hist_df['板块代码'] = symbol
        # 确保 '日期' 列是 Date 类型，并处理可能的 '日期间隔' 列
        if '日期间隔' in hist_df.columns:
            hist_df['日期'] = pd.to_datetime(hist_df['日期间隔']).dt.date  # 优先使用 '日期间隔' 列
        elif '日期' in hist_df.columns:
            hist_df['日期'] = pd.to_datetime(hist_df['日期']).dt.date
        else:
            print(f"板块 {board_name} ({symbol}) 历史数据缺少日期列，跳过.")
            return None

        # 选择需要的列并重新排序
        hist_df_selected = hist_df[
            ['板块名称', '板块代码', '日期', '涨跌幅', '总市值', '换手率', '上涨家数', '下跌家数', '上涨比例']]
        return hist_df_selected
    else:
        print(f"获取板块 {board_name} ({symbol}) 历史数据失败或无数据 (DataFrame 为空).")
        return None


def showdata():
    """主程序入口"""
    start_time = time.time()

    concept_names_df = get_concept_board_names()
    if concept_names_df is not None and not concept_names_df.empty:
        print(f"获取到 {len(concept_names_df)} 个概念板块.")
        for index, row in concept_names_df.iterrows():
            board_name = row['板块名称']
            board_code = row['板块代码']
            print(f"开始处理概念板块: {board_name} ({board_code})")

            hist_data_df = get_concept_board_data(symbol=board_code, board_name=board_name)
            if hist_data_df is not None and not hist_data_df.empty:
                print(hist_data_df)
            time.sleep(1)  # 建议添加延时，避免请求过快被限制
            print(f"概念板块: {board_name} ({board_code}) 处理完成.")
    else:
        print("获取概念板块名称失败或无数据。")

    end_time = time.time()
    print(f"数据处理完成，总耗时: {end_time - start_time:.2f} 秒.")


if __name__ == "__main__":
    showdata()
