#!/usr/bin/env python

"""Tests for `stockbee` package."""

import pytest
import pandas as pd
from stockbee.detectors import pinbar_detector

def test_if_pinbar_detector_inputs_and_outputs_dataframe():
    dataframe = pd.DataFrame([])
    assert type(pinbar_detector(dataframe)) is pd.DataFrame
