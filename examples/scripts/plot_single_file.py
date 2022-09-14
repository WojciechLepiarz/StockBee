import pandas as pd
import sys
from stockbee.plots import plot_candlestick

if __name__ == "__main__":
    file_path = sys.argv[1]
    data = pd.read_csv(file_path, index_col=1)
    data.index = pd.to_datetime(data.index, format="%Y%m%d")
    plot_candlestick(data)
