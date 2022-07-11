import pandas as pd

def add_volatility(data: pd.DataFrame) -> pd.DataFrame: 
    # should calculate max up, down movements over period and mean/median up and down
    added_columns = ["VLT_BMax", "VLT_SMax", "VLT_BMean", "VLT_SMean", "VLT_BMed", "VLT_SMed"]
    return pd.DataFrame([], columns=added_columns)
