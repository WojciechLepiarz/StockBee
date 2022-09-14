"""Tests for `stockbee.internal_functions.calculate_body_and_tails`."""

import pandas as pd
import pytest

from stockbee.internal_functions import calculate_body_and_tails
testColumns = ["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"]

@pytest.fixture
def dataframe_with_test_data():
    inputDataFrame = pd.read_csv(".\\tests\\test_data\\test_stock_data.mst", index_col=1)
    inputDataFrame.index = pd.to_datetime(inputDataFrame.index, format="%Y%m%d")
    return inputDataFrame

def test_if_calculate_body_and_tails_inputs_and_outputs_dataframe():
    dataframe_out = pd.DataFrame([])
    assert type(calculate_body_and_tails(dataframe_out)[0]) is pd.DataFrame
    assert type(calculate_body_and_tails(dataframe_out)[1]) is list

def test_if_calculate_body_and_tails_returns_dataframe_with_column_body_added():
    dataframe_out = calculate_body_and_tails(pd.DataFrame([], columns=testColumns))[0]
    assert "body" in dataframe_out.columns

def test_if_body_is_calculated(dataframe_with_test_data):
    dataframe_out = calculate_body_and_tails(dataframe_with_test_data)[0]
    dataframe_out["bodyGT"] = dataframe_out["<CLOSE>"]-dataframe_out["<OPEN>"]
    assert dataframe_out["body"].equals(dataframe_out["bodyGT"])

def test_if_added_columns_are_in_list():
    dataframe_out, added_columns = calculate_body_and_tails(pd.DataFrame([], columns=testColumns))
    for name in dataframe_out.columns:
        if name not in testColumns:
            assert name in added_columns

def test_if_tails_columns_are_added():
    dataframe_out = calculate_body_and_tails(pd.DataFrame([], columns=testColumns))[0]
    assert "tailUp" in dataframe_out.columns
    assert "tailDown" in dataframe_out.columns

def test_if_tailUp_is_calculated(dataframe_with_test_data):
    dataframe_out = calculate_body_and_tails(dataframe_with_test_data)[0]
    dataframe_out.loc[dataframe_out["body"] > 0, "tailUpGT"] = dataframe_out["<HIGH>"]-dataframe_out["<CLOSE>"]
    dataframe_out.loc[dataframe_out["body"] <= 0, "tailUpGT"] = dataframe_out["<HIGH>"]-dataframe_out["<OPEN>"]
    assert dataframe_out["tailUp"].equals(dataframe_out["tailUpGT"])
