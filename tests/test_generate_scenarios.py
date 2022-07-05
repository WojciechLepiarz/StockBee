import pandas as pd
import pytest
from stockbee.scenario_generator import generate_scenarios

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

def test_inputs_and_output(empty_dataframe):
    assert type(generate_scenarios(empty_dataframe, "label", 7., 8)) is pd.DataFrame

def test_if_output_index_size_equals_periods(dataframe_with_test_data):
    assert len(generate_scenarios(dataframe_with_test_data, "PINB_GT", 7., 21).index) == 21

def test_if_output_columns_size_equals_triggers(dataframe_with_test_data):
    generated_output = generate_scenarios(dataframe_with_test_data, "PINB_GT", 1., 20)
    assert len(generated_output.columns) == dataframe_with_test_data["PINB_GT"].sum()

def test_if_output_collects_close_data(dataframe_with_test_data):
    generated_output = generate_scenarios(dataframe_with_test_data, "PINB_GT")
    dataframe_with_test_data.reset_index(inplace=True)
    indices = dataframe_with_test_data.loc[dataframe_with_test_data["PINB_GT"]>=1.].index
    sum_of_entries = 0.
    for ii in indices:
        sum_of_entries += dataframe_with_test_data.loc[ii:ii+10,"<CLOSE>"].sum()
    dataframe_with_test_data.set_index("<DTYYYYMMDD>", inplace=True)
    assert generated_output.values.sum() == sum_of_entries
