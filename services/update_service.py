import os
from datetime import datetime, timedelta
from data.list_downloader import ListDownloader

class UpdateService:
    def __init__(self, file_path: str, max_days: int = 100):
        self.file_path = file_path
        self.max_days = max_days

    def is_update_needed(self) -> bool:
        """
        检查文件是否需要更新。

        Returns:
            bool: 如果需要更新，返回 True；否则返回 False。
        """
        if not os.path.exists(self.file_path):
            return True

        last_modified_time = os.path.getmtime(self.file_path)
        last_modified_date = datetime.fromtimestamp(last_modified_time)

        if datetime.now() - last_modified_date > timedelta(days=self.max_days):
            return True

        return False

    def update_stock_list(self):
        """
        更新股票列表文件。
        """
        if self.is_update_needed():
            print("更新股票列表文件...")
            stock_list = ListDownloader.get_stock_list()
            stock_list.to_csv(self.file_path, index=False, encoding="utf_8_sig")
            print(f"股票列表已保存到 {self.file_path}")
        else:
            print(f"股票列表文件未过期，无需更新")