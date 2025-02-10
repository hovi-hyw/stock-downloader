import subprocess
from src.core.logger import logger

def run_script(script_name):
    """运行指定的 Python 脚本"""
    try:
        logger.info(f"开始运行脚本: {script_name}")
        subprocess.run(["python", script_name], check=True)
        logger.info(f"脚本 {script_name} 运行完成")
    except subprocess.CalledProcessError as e:
        logger.error(f"脚本 {script_name} 运行出错: {e}")
    except FileNotFoundError:
        logger.error(f"Python 解释器未找到，请确保 Python 已安装并添加到 PATH 环境变量。")


def main():
    scripts_to_run = [
        "scripts/download/download_index.py",
        "scripts/download/download_concept.py",
        "scripts/download/download_stock.py",
    ]

    for script in scripts_to_run:
        run_script(script)

    logger.info("所有数据下载任务完成")


if __name__ == "__main__":
    main()