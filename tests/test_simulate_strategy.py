import pytest
import pandas as pd

from stockbee.strategy_simulator import Strategy

@pytest.fixture
def dataframe_with_test_data():
    inputDataFrame = pd.read_csv(".\\tests\\test_data\\test_stock_data.mst", index_col=1)
    inputDataFrame.index = pd.to_datetime(inputDataFrame.index, format="%Y%m%d")
    return inputDataFrame

@pytest.fixture
def empty_dataframe():
    basic_columns = ["<TICKER>", "<DTYYYYMMDD>", "<OPEN>", "<HIGH>",
                     "<LOW>", "<CLOSE>", "<VOL>"]
    return pd.DataFrame([], columns=basic_columns)

def test_strategy_init():
    my_strategy = Strategy()
    assert type(my_strategy) is Strategy

def test_strategy_simulate_interface(empty_dataframe):
    my_strategy = Strategy()
    assert type(my_strategy.simulate(empty_dataframe, 100., 5)) is pd.DataFrame
    assert type(my_strategy.simulate(empty_dataframe)) is pd.DataFrame
