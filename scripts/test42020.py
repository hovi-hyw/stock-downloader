import akshare as ak

def concept_test():
    hist_df = ak.stock_board_concept_hist_em(symbol="昨日连板_含一字",start_date="20250201", end_date="20990101")
    print(hist_df)

def stock_test():
    hist_df = ak.stock_zh_a_spot()
    print(hist_df)

if __name__ == '__main__':
    stock_test()