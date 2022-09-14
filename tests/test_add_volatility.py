import pytest
import pandas as pd

from stockbee.indicators import add_volatility

BMax = "VLT_BMax"
SMax = "VLT_SMax"
BMean = "VLT_BMean"
SMean = "VLT_SMean"
BMed = "VLT_BMed"
SMed = "VLT_SMed"

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

def test_if_add_volatility_inputs_and_outputs_dataframe(empty_dataframe):
    assert type(add_volatility(empty_dataframe)) is pd.DataFrame

def test_if_add_volatility_returns_dataframe_with_proper_columns_added(empty_dataframe):
    dataframe_out = add_volatility(empty_dataframe)
    assert BMax in dataframe_out.columns
    assert SMax in dataframe_out.columns
    assert BMean in dataframe_out.columns
    assert SMean in dataframe_out.columns
    assert BMed in dataframe_out.columns
    assert SMed in dataframe_out.columns
