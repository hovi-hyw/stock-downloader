import os

# 定义要创建的目录和文件结构
structure = {
    'config': ['config.py'],
    'data': ['downloader.py', 'stock_downloader.py', 'index_downloader.py', 'list_downloader.py'],
    'db': ['db_manager.py', 'models.py', 'init_db.py'],
    'services': ['update_service.py', 'save_service.py', 'batch_service.py'],
    'utils': ['retry_utils.py', 'file_utils.py', 'logging_utils.py'],
    '.': ['main.py']  # '.' 表示当前目录
}

# 获取当前工作目录
base_path = os.getcwd()

# 创建目录和文件
for folder, files in structure.items():
    folder_path = os.path.join(base_path, folder)
    if folder != '.':
        os.makedirs(folder_path, exist_ok=True)  # 创建目录
    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'w') as f:
            pass  # 创建空文件

print("目录和文件创建完成。")
