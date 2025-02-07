import akshare as ak
hist_df = ak.stock_board_concept_hist_em(symbol="昨日连板_含一字",start_date="20250201", end_date="20990101")
print(hist_df)