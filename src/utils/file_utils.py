# src/utils/file_utils.py
"""
此模块包含文件相关的实用工具函数。
包括检查文件是否存在且在有效期内的函数。
Authors: hovi.hyw & AI
Date: 2024-07-03
"""

import os
import time


def check_file_validity(file_path, max_age_days):
    """
    检查文件是否存在且在有效期内。

    Args:
        file_path (str): 文件路径。
        max_age_days (int): 文件最大有效天数。

    Returns:
        bool: 如果文件存在且在有效期内，则返回 True，否则返回 False。
    """
    if not os.path.exists(file_path):
        return False

    file_mtime = os.path.getmtime(file_path)
    file_age_days = (time.time() - file_mtime) / (60 * 60 * 24)
    return file_age_days <= max_age_days


if __name__ == '__main__':
    # 示例用法
    test_file_path = "test_file.txt"
    max_age = 7  # 天

    # 创建一个测试文件
    if not os.path.exists(test_file_path):
        with open(test_file_path, 'w') as f:
            f.write("This is a test file.")

    if check_file_validity(test_file_path, max_age):
        print(f"文件 '{test_file_path}' 有效。")
    else:
        print(f"文件 '{test_file_path}' 无效或不存在。")
