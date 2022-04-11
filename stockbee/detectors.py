import pandas as pd
import numpy as np

def pinbar_detector(data: pd.DataFrame, labelPinBuy: str="PIN_Buy", labelPinSell: str="PIN_Sell"):
    data[labelPinBuy] = np.ones((len(data.index), 1), dtype=np.int)
    data[labelPinSell] = np.zeros((len(data.index), 1), dtype=np.int)
    return data