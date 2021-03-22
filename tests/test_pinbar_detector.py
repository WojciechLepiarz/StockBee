#!/usr/bin/env python

"""Tests for `stockbee` package."""

import pytest
import pandas as pd
from stockbee.detectors import pinbar_detector

@pytest.fixture
def dataframe_with_data():
    new_dataframe = pd.DataFrame()
    
def test_if_pinbar_detector_inputs_and_outputs_dataframe():
    dataframe = pd.DataFrame([])
    assert type(pinbar_detector(dataframe)) is pd.DataFrame

def test_if_pinbar_detector_returns_dataframe_with_column_pinbar_added():
    dataframe_out = pinbar_detector(pd.DataFrame([]))
    assert "pinbar" in dataframe_out.columns

def test_if_pinbar_column_is_0s_and_1s():
