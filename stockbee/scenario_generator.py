import pandas as pd

def generate_scenarios(data: pd.DataFrame, label: str, 
                       threshold: float = 1., periods: int = 10) -> pd.DataFrame:
    if label not in data.columns:
        return pd.DataFrame(["Error - key not found"])
    data.reset_index(inplace=True)
    scenarios = pd.DataFrame([], index=[ii for ii in range(0, periods)])
    data.set_index("<DTYYYYMMDD>", inplace=True)
    return scenarios
