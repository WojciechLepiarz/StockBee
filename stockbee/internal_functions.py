import pandas as pd
import numpy as np
from typing import Tuple

# Function takes dataframe with price data and adds calculated body and tails columns of a given candle (price row)
def calculate_body_and_tails(data: pd.DataFrame, 
                    labelOpen: str="<OPEN>", labelHigh: str="<HIGH>",
                    labelLow: str="<LOW>", labelClose: str="<CLOSE>") -> Tuple[pd.DataFrame, list]:
    
    if not set([labelOpen, labelClose, labelHigh, labelLow]).issubset(set(data.columns)):
        return data, []

    data["body"] = np.zeros((len(data.index), 1), dtype=float)
    data["tailUp"] = np.zeros((len(data.index), 1), dtype=float)
    data["tailDown"] = np.zeros((len(data.index), 1), dtype=float)
    added_columns = ["body", "tailUp", "tailDown"]
    
    data["body"] = data[labelClose] - data[labelOpen]
    data.loc[data["body"] > 0, "tailUp"] = data[labelHigh]-data[labelClose]
    data.loc[data["body"] <= 0, "tailUp"] = data[labelHigh]-data[labelOpen]
    data.loc[data["body"] > 0, "tailDown"] = data[labelOpen]-data[labelLow]
    data.loc[data["body"] <= 0, "tailDown"] = data[labelClose]-data[labelLow]
    
    return data, added_columns
