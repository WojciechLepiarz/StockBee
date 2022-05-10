import pandas as pd
import numpy as np
from stockbee.internal_functions import calculate_body_and_tails



def pinbar_detector(data: pd.DataFrame, 
                    labelBuy: str="PIN_Buy", labelSell: str="PIN_Sell", 
                    labelOpen: str="<OPEN>", labelHigh: str="<HIGH>", 
                    labelLow: str="<LOW>", labelClose: str="<CLOSE>") -> pd.DataFrame:
    """
    Pinbar detector takes dataframe with price data (OHLC) and produces new columns 
    with information if given record is a pinbar signal for buy or sell.
    

    Args:
        data (pd.DataFrame): input dataframe
        labelBuy (str, optional): label used for pin buy signal column. Defaults to "PIN_Buy".
        labelSell (str, optional): label used for pin sell signal column. Defaults to "PIN_Sell".
        labelOpen (str, optional): Open price label in input dataframe. Defaults to "<OPEN>".
        labelHigh (str, optional): High price label in input dataframe. Defaults to "<HIGH>".
        labelLow (str, optional): Low price label in input dataframe. Defaults to "<LOW>".
        labelClose (str, optional): Close pirce label in input dataframe. Defaults to "<CLOSE>".

    Returns:
        pd.DataFrame: Input dataframe with added columns for detected signals.
    """
    data[labelBuy] = np.zeros((len(data.index), 1), dtype=np.int)
    data[labelSell] = np.zeros((len(data.index), 1), dtype=np.int)
    data, tempColumns = calculate_body_and_tails(data, labelOpen, labelHigh, labelLow, labelClose)
    if(tempColumns):
        data.loc[
            ((data["tailDown"] > 3*data["body"].abs()) & (data["tailUp"] < 0.5*data["tailDown"])),
            labelBuy
        ] = 1
        data.loc[
            ((data["tailUp"] > 3*data["body"].abs()) & (data["tailDown"] < 0.5*data["tailUp"])),
            labelSell
        ] = 1
    data = data.drop(tempColumns, axis=1, errors='ignore')
    return data

def fakey_detector(data: pd.DataFrame, 
                   labelBuy: str="Fakey_Buy", labelSell: str="Fakey_Sell",
                   labelOpen: str="<OPEN>", labelHigh: str="<HIGH>", 
                   labelLow: str="<LOW>", labelClose: str="<CLOSE>") -> pd.DataFrame:
    data[labelBuy] = np.zeros((len(data.index), 1), dtype=np.int)
    data[labelSell] = np.zeros((len(data.index), 1), dtype=np.int)
    data, tempColumns = calculate_body_and_tails(data, labelOpen, labelHigh, labelLow, labelClose)
    if(tempColumns):
        data["body-1"] = data["body"].shift(1, fill_value=0)
        data["close-1"] = data[labelClose].shift(1, fill_value=0)
        tempColumns += ["body-1", "close-1"]
        data.loc[
            ((data["body-1"] > 0) 
             & (data[labelHigh] > data["close-1"]+data["body-1"].abs()*0.25) 
             & (data[labelOpen] < data["close-1"]) 
             & (data[labelClose] < data["close-1"])),
            labelBuy
        ] = 1
        data.loc[
            ((data["body-1"] < 0) 
             & (data[labelLow] < data["close-1"]-data["body-1"].abs()*0.25) 
             & (data[labelOpen] > data["close-1"]) 
             & (data[labelClose] > data["close-1"])),
            labelSell
        ] = 1
    data = data.drop(tempColumns, axis=1, errors='ignore')
    return data
