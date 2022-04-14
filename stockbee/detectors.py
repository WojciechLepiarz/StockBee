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
    data, newColumns = calculate_body_and_tails(data, labelOpen, labelHigh, labelLow, labelClose)
    tempColumns += newColumns
    if(newColumns):
        data.loc[
            ((data["tailDown"] > 3*data["body"].abs()) & (data["tailUp"] < 0.5*data["tailDown"])),
            labelPinBuy
        ] = 1
        data.loc[
            ((data["tailUp"] > 3*data["body"].abs()) & (data["tailDown"] < 0.5*data["tailUp"])),
            labelPinSell
        ] = 1
    data = data.drop(tempColumns, axis=1, errors='ignore')
    return data
