import os
import sys
from concurrent.futures import ThreadPoolExecutor
from src.core.logger import logger
import subprocess

def run_script(script_name):
    """运行指定的 Python 脚本"""
    try:
        logger.info(f"开始运行脚本: {script_name}")
        python_path = sys.executable  # 动态获取当前 Python 解释器路径
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        subprocess.run([python_path, script_name], env=env, check=True)
        logger.info(f"脚本 {script_name} 运行完成")
    except subprocess.CalledProcessError as e:
        logger.error(f"脚本 {script_name} 运行出错: {e}")
    except FileNotFoundError:
        logger.error(f"Python 解释器未找到，请确保 Python 已安装并添加到 PATH 环境变量。")

def main():
    scripts_to_run = [
        "download_index.py",  # 指数数据下载
        "download_stock.py",  # 股票数据下载
    ]

    with ThreadPoolExecutor(max_workers=len(scripts_to_run)) as executor:
        futures = [executor.submit(run_script, script) for script in scripts_to_run]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"脚本执行失败: {e}")

    logger.info("所有数据下载任务完成")

if __name__ == "__main__":
    main()