"""Tests for `stockbee.detectors.pinbar_detector`."""

import pandas as pd
import pytest
from stockbee.detectors import detect_pinbar


defaultPinBuyLabel = "PIN_Buy"
defaultPinSellLabel = "PIN_Sell"

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


def test_if_pinbar_detector_inputs_and_outputs_dataframe():
    dataframe_out = pd.DataFrame([])
    assert type(detect_pinbar(dataframe_out)) is pd.DataFrame

def test_if_pinbar_detector_returns_dataframe_with_column_pinbar_added():
    dataframe_out = detect_pinbar(pd.DataFrame([]))
    assert defaultPinBuyLabel in dataframe_out.columns
    assert defaultPinSellLabel in dataframe_out.columns

def test_custom_pinbar_labels():
    dataframe_out = detect_pinbar(pd.DataFrame([]), labelBuy="BuyPin", labelSell="SellPin")
    assert "BuyPin" in dataframe_out.columns
    assert "SellPin" in dataframe_out.columns

def test_if_pinbar_column_is_0s_and_1s(dataframe_with_test_data):
    inputDataFrame = detect_pinbar(dataframe_with_test_data)
    inputDataFrame.loc[inputDataFrame[defaultPinBuyLabel] == 1] = 0
    inputDataFrame.loc[inputDataFrame[defaultPinSellLabel] == 1] = 0
    assert inputDataFrame[defaultPinBuyLabel].sum() == 0
    assert inputDataFrame[defaultPinSellLabel].sum() == 0

def test_if_any_spare_columns_remain(empty_dataframe):
    inputDataFrame = detect_pinbar(empty_dataframe)
    assert len(inputDataFrame.columns) == 9

def test_pinbar_buy_sell_detection(dataframe_with_test_data):
    inputDataFrame = detect_pinbar(dataframe_with_test_data)
    inputDataFrame = inputDataFrame.astype({"PINB_GT": int, "PINS_GT": int}, errors='raise') 
    assert inputDataFrame[defaultPinBuyLabel].equals(inputDataFrame["PINB_GT"])
    assert inputDataFrame[defaultPinSellLabel].equals(inputDataFrame["PINS_GT"])
