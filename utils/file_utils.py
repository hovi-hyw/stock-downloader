import os
from datetime import datetime, timedelta

class FileUtils:
    @staticmethod
    def is_file_outdated(file_path: str, max_days: int) -> bool:
        """
        检查文件是否过期。

        Args:
            file_path (str): 文件路径。
            max_days (int): 文件的最大有效天数。

        Returns:
            bool: 如果文件不存在或已过期，返回 True；否则返回 False。
        """
        if not os.path.exists(file_path):
            return True

        last_modified_time = os.path.getmtime(file_path)
        last_modified_date = datetime.fromtimestamp(last_modified_time)

        return datetime.now() - last_modified_date > timedelta(days=max_days)

    @staticmethod
    def save_to_csv(data, file_path: str):
        """
        将数据保存为 CSV 文件。

        Args:
            data (pandas.DataFrame): 要保存的数据。
            file_path (str): 文件路径。
        """
        try:
            data.to_csv(file_path, index=False, encoding="utf_8_sig")
            print(f"文件已保存到 {file_path}")
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            raise

    @staticmethod
    def read_csv(file_path: str):
        """
        读取 CSV 文件。

        Args:
            file_path (str): 文件路径。

        Returns:
            pandas.DataFrame: 读取到的数据。
        """
        try:
            import pandas as pd
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"读取文件失败: {str(e)}")
            raise