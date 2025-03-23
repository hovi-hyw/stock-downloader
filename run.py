from StockDownloader.src.main import main
import sys

def display_menu():
    """
    显示交互式菜单，让用户选择运行模式
    
    Returns:
        int: 用户选择的运行模式，如果用户选择退出则返回None
    """
    print("\n股票数据下载与API服务 - 运行模式选择")
    print("-" * 40)
    print("1: 只下载指数日线数据")
    print("2: 只下载股票日线数据")
    print("3: 只更新指数日线数据")
    print("4: 只更新股票日线数据")
    print("5: 只下载股票和指数日线数据")
    print("6: 只更新股票和指数日线数据")
    print("7: 更新stock_info以及index_info表")
    print("8: 启动完整的API服务和定时任务")
    print("0: 退出程序")
    print("-" * 40)
    
    while True:
        try:
            choice = input("请输入您的选择 (0-8): ")
            if choice == "0":
                return None
            choice = int(choice)
            if 1 <= choice <= 8:
                return choice
            else:
                print("无效的选择，请输入0-8之间的数字")
        except ValueError:
            print("无效的输入，请输入数字")

if __name__ == "__main__":
    mode = display_menu()
    
    if mode is None:
        print("程序已退出")
        sys.exit(0)
    
    # 如果选择了选项8，则不传递mode参数，启动完整服务
    if mode == 8:
        main()
    else:
        # 传递用户选择的模式给main函数
        sys.argv = [sys.argv[0], "--mode", str(mode)]
        main()