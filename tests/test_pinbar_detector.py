#!/usr/bin/env python

"""Tests for `stockbee.detectors.pinbar_detector`."""

import pandas as pd
import pytest

from stockbee.detectors import pinbar_detector

defaultPinBuyLabel = "PIN_Buy"
defaultPinSellLabel = "PIN_Sell"

# @pytest.fixture
# def dataframe_with_data():
#     new_dataframe = pd.DataFrame()
    
def test_if_pinbar_detector_inputs_and_outputs_dataframe():
    dataframe = pd.DataFrame([])
    assert type(pinbar_detector(dataframe)) is pd.DataFrame

def test_if_pinbar_detector_returns_dataframe_with_column_pinbar_added():
    dataframe_out = pinbar_detector(pd.DataFrame([]))
    assert defaultPinBuyLabel in dataframe_out.columns
    assert defaultPinSellLabel in dataframe_out.columns

def test_custom_pinbar_labels():
    dataframe_out = pinbar_detector(pd.DataFrame([]), labelPinBuy="BuyPin", labelPinSell="SellPin")
    assert "BuyPin" in dataframe_out.columns
    assert "SellPin" in dataframe_out.columns

def test_if_pinbar_column_is_0s_and_1s():
    inputDataFrame = pd.read_csv(".\\tests\\test_data\\test_stock_data.mst", index_col=1)
    inputDataFrame.index = pd.to_datetime(inputDataFrame.index, format="%Y%m%d")
    inputDataFrame = pinbar_detector(inputDataFrame)
    inputDataFrame.loc[inputDataFrame[defaultPinBuyLabel] == 1] = 0
    inputDataFrame.loc[inputDataFrame[defaultPinSellLabel] == 1] = 0
    assert inputDataFrame[defaultPinBuyLabel].sum() == 0
    assert inputDataFrame[defaultPinSellLabel].sum() == 0
