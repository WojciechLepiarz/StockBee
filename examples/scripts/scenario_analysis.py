import pandas as pd
from stockbee.scenario_generator import generate_scenarios

inputDataFrame = pd.read_csv("..\\..\\tests\\test_data\\test_stock_data.mst", index_col=1)
inputDataFrame.index = pd.to_datetime(inputDataFrame.index, format="%Y%m%d")

my_scenarios = generate_scenarios(inputDataFrame, "PINB_GT")
