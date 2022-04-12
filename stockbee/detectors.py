import pandas as pd
import numpy as np
from stockbee.internal_functions import calculate_body_and_tails


#  Pinbar detector takes dataframe with price data (OHLC) and produces new columns 
#  with information if given record is a pinbar signal for buy or sell
def pinbar_detector(data: pd.DataFrame, 
                    labelPinBuy: str="PIN_Buy", labelPinSell: str="PIN_Sell", 
                    labelOpen: str="<OPEN>", labelHigh: str="<HIGH>", 
                    labelLow: str="<LOW>", labelClose: str="<CLOSE>") -> pd.DataFrame:
    data[labelPinBuy] = np.zeros((len(data.index), 1), dtype=np.int)
    data[labelPinSell] = np.zeros((len(data.index), 1), dtype=np.int)
    tempColumns = []
    data, newColumns = calculate_body_and_tails(data)
    tempColumns += newColumns
    # calculate tails
    # set flags
    data = data.drop(tempColumns, axis=1, errors='ignore')
    return data
