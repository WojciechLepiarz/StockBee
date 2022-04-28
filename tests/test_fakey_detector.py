"""Tests for `stockbee.detectors.fakey_detector`."""

import pandas as pd
import pytest
from stockbee.detectors import fakey_detector


defaultFakeyBuyLabel = "Fakey_Buy"
defaultFakeySellLabel = "Fakey_Sell"

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


def test_if_fakey_detector_inputs_and_outputs_dataframe():
    dataframe_out = pd.DataFrame([])
    assert type(fakey_detector(dataframe_out)) is pd.DataFrame

def test_if_pinbar_detector_returns_dataframe_with_column_fakey_added():
    dataframe_out = fakey_detector(pd.DataFrame([]))
    assert defaultFakeyBuyLabel in dataframe_out.columns
    assert defaultFakeySellLabel in dataframe_out.columns

def test_custom_pinbar_labels():
    dataframe_out = fakey_detector(pd.DataFrame([]), labelBuy="FakeBuy", labelSell="FakeSell")
    assert "FakeBuy" in dataframe_out.columns
    assert "FakeSell" in dataframe_out.columns

def test_if_pinbar_column_is_0s_and_1s(dataframe_with_test_data):
    inputDataFrame = fakey_detector(dataframe_with_test_data)
    inputDataFrame.loc[inputDataFrame[defaultFakeyBuyLabel] == 1] = 0
    inputDataFrame.loc[inputDataFrame[defaultFakeySellLabel] == 1] = 0
    assert inputDataFrame[defaultFakeyBuyLabel].sum() == 0
    assert inputDataFrame[defaultFakeySellLabel].sum() == 0

def test_if_any_spare_columns_remain(empty_dataframe):
    inputDataFrame = fakey_detector(empty_dataframe)
    assert len(inputDataFrame.columns) == 9

def test_pinbar_buy_sell_detection(dataframe_with_test_data):
    inputDataFrame = fakey_detector(dataframe_with_test_data)
    inputDataFrame = inputDataFrame.astype({"FAKEYB_GT": int, "FAKEYS_GT": int}, errors='raise') 
    assert inputDataFrame[defaultFakeyBuyLabel].equals(inputDataFrame["FAKEYB_GT"])
    assert inputDataFrame[defaultFakeySellLabel].equals(inputDataFrame["FAKEYS_GT"])
