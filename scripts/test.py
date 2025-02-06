import akshare as ak
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Date, Integer
import pandas as pd
import time
from src.core.config import config

# 创建数据库连接
engine = create_engine(config.DATABASE_URL)


# 元数据
metadata = MetaData()

# 定义概念板块历史数据表
concept_board_table = Table(
    "concept_board",  # 表名，你可以自定义
    metadata,
    Column("concept_name", String, comment="板块名称"),
    Column("concept_code", String, primary_key=True, comment="板块代码"), # 板块代码作为主键之一
    Column("date", Date, primary_key=True, comment="日期"), # 日期作为主键之一，和板块代码一起构成联合主键
    Column("涨跌幅", Float, comment="涨跌幅"),
    Column("总市值", Float, comment="总市值"),
    Column("换手率", Float, comment="换手率"),
    Column("上涨家数", Integer, comment="上涨家数"),
    Column("下跌家数", Integer, comment="下跌家数"),
    Column("上涨比例", Float, comment="上涨比例"),
)

# 创建表 (如果表不存在)
metadata.create_all(engine)


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
    print(f"Debug: 尝试获取板块代码为 {symbol} ({board_name}) 的历史数据...")  # 调试信息

    try:
        hist_df = ak.stock_board_concept_hist_em(symbol=board_name)
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
        hist_df_selected = hist_df[[ '板块名称', '板块代码', '日期', '涨跌幅', '总市值', '换手率', '上涨家数', '下跌家数', '上涨比例']]
        return hist_df_selected
    else:
        print(f"获取板块 {board_name} ({symbol}) 历史数据失败或无数据 (DataFrame 为空).")
        return None


def store_concept_board_data(df):
    """将概念板块历史数据写入数据库"""
    if df is not None and not df.empty:
        try:
            # 将 DataFrame 转换为字典列表，准备批量插入
            data_to_insert = df.to_dict(orient='records')

            # 使用 SQLAlchemy Core 的方式进行批量插入
            with engine.connect() as connection:
                insert_stmt = concept_board_table.insert()
                connection.execute(insert_stmt, data_to_insert)
                connection.commit() # 提交事务

            print(f"成功写入 {len(df)} 条数据到数据库.")
        except Exception as e:
            print(f"写入数据库失败: {e}")
            print(df) # 打印未能成功写入的数据，方便排查问题
    else:
        print("没有数据需要写入数据库。")


def main():
    """主程序入口"""
    start_time = time.time()
    print("开始获取概念板块数据并写入数据库...")

    concept_names_df = get_concept_board_names()
    if concept_names_df is not None and not concept_names_df.empty:
        print(f"获取到 {len(concept_names_df)} 个概念板块.")
        for index, row in concept_names_df.iterrows():
            board_name = row['板块名称']
            board_code = row['板块代码']
            print(f"开始处理概念板块: {board_name} ({board_code})")

            hist_data_df = get_concept_board_data(symbol=board_code, board_name=board_name)
            if hist_data_df is not None and not hist_data_df.empty:
                store_concept_board_data(hist_data_df)
            time.sleep(1) # 建议添加延时，避免请求过快被限制
            print(f"概念板块: {board_name} ({board_code}) 处理完成.")
    else:
        print("获取概念板块名称失败或无数据。")

    end_time = time.time()
    print(f"数据处理完成，总耗时: {end_time - start_time:.2f} 秒.")


if __name__ == "__main__":
    main()