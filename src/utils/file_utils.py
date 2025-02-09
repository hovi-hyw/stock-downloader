import os
import time

def check_file_validity(file_path, max_age_days):
    """检查文件是否存在且在有效期内"""
    if not os.path.exists(file_path):
        return False

    file_mtime = os.path.getmtime(file_path)
    file_age_days = (time.time() - file_mtime) / (60 * 60 * 24)
    return file_age_days <= max_age_days

if __name__ == '__main__':
    # 示例用法
    test_file_path = "test_file.txt"
    max_age = 7 # 天

    # 创建一个测试文件
    if not os.path.exists(test_file_path):
        with open(test_file_path, 'w') as f:
            f.write("This is a test file.")

    if check_file_validity(test_file_path, max_age):
        print(f"文件 '{test_file_path}' 有效。")
    else:
        print(f"文件 '{test_file_path}' 无效或不存在。")