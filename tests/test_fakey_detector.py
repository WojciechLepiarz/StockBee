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

def test_if_fakey_detector_inputs_and_outputs_dataframe():
    dataframe_out = pd.DataFrame([])
    assert type(fakey_detector(dataframe_out)) is pd.DataFrame

def test_if_pinbar_detector_returns_dataframe_with_column_fakey_added():
    dataframe_out = fakey_detector(pd.DataFrame([]))
    assert defaultFakeyBuyLabel in dataframe_out.columns
    assert defaultFakeySellLabel in dataframe_out.columns

# def test_custom_pinbar_labels():
#     dataframe_out = fakey_detector(pd.DataFrame([]), labelPinBuy="BuyPin", labelPinSell="SellPin")
#     assert "BuyPin" in dataframe_out.columns
#     assert "SellPin" in dataframe_out.columns

# def test_if_pinbar_column_is_0s_and_1s(dataframe_with_test_data):
#     inputDataFrame = pinbar_detector(dataframe_with_test_data)
#     inputDataFrame.loc[inputDataFrame[defaultPinBuyLabel] == 1] = 0
#     inputDataFrame.loc[inputDataFrame[defaultPinSellLabel] == 1] = 0
#     assert inputDataFrame[defaultPinBuyLabel].sum() == 0
#     assert inputDataFrame[defaultPinSellLabel].sum() == 0

# def test_if_any_spare_columns_remain(dataframe_with_test_data):
#     inputDataFrame = pinbar_detector(dataframe_with_test_data)
#     assert len(inputDataFrame.columns) == 10

# def test_pinbar_buy_sell_detection(dataframe_with_test_data):
#     inputDataFrame = pinbar_detector(dataframe_with_test_data)
#     inputDataFrame = inputDataFrame.astype({"PINB_GT": int, "PINS_GT": int}, errors='raise') 
#     assert inputDataFrame[defaultPinBuyLabel].equals(inputDataFrame["PINB_GT"])
#     assert inputDataFrame[defaultPinSellLabel].equals(inputDataFrame["PINS_GT"])
