import pandas as pd
import numpy as np
from stockbee.internal_functions import calculate_body_and_tails



def pinbar_detector(data: pd.DataFrame, 
                    labelPinBuy: str="PIN_Buy", labelPinSell: str="PIN_Sell", 
                    labelOpen: str="<OPEN>", labelHigh: str="<HIGH>", 
                    labelLow: str="<LOW>", labelClose: str="<CLOSE>") -> pd.DataFrame:
    """
    Pinbar detector takes dataframe with price data (OHLC) and produces new columns 
    with information if given record is a pinbar signal for buy or sell.
    

    Args:
        data (pd.DataFrame): input dataframe
        labelPinBuy (str, optional): label used for pin buy signal column. Defaults to "PIN_Buy".
        labelPinSell (str, optional): label used for pin sell signal column. Defaults to "PIN_Sell".
        labelOpen (str, optional): Open price label in input dataframe. Defaults to "<OPEN>".
        labelHigh (str, optional): High price label in input dataframe. Defaults to "<HIGH>".
        labelLow (str, optional): Low price label in input dataframe. Defaults to "<LOW>".
        labelClose (str, optional): Close pirce label in input dataframe. Defaults to "<CLOSE>".

    Returns:
        pd.DataFrame: Input dataframe with added columns for detected signals.
    """
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


def fakey_detector() -> pd.DataFrame:
    data = pd.DataFrame()
    return data