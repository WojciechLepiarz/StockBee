import pandas as pd

def pinbar_detector(data: pd.DataFrame):
    data["pinbar"] = []
    return data