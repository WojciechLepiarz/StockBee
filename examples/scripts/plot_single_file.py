import pandas as pd
from stockbee.plots import plot_candlestick

file_path = '..\\..\\tests\\test_data\\test_stock_data.mst'
data = pd.read_csv(file_path, index_col=1)
data.index = pd.to_datetime(data.index, format="%Y%m%d")
plot_candlestick(data)
