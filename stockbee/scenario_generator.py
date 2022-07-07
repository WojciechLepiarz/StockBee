import pandas as pd

def generate_scenarios(data: pd.DataFrame, label: str, 
                       threshold: float = 1., periods: int = 10, 
                       index_label: str ="<DTYYYYMMDD>", close_label:str = "<CLOSE>") -> pd.DataFrame:
    """Function generates a new dataframe with columns filled with close prices. Each column represents scenarios
        where value from column in data represented by label is above threshold. Column is filled with close prices
        from start of the scenario up to number defined in periods.

    Args:
        data (pd.DataFrame): dataframe with price data and column to be used as a scenario trigger
        label (str): label of the column in data that represents trigger for scenario generator
        threshold (float, optional): Threshold for scenario generator trigger. Values above or equal threshold 
            will result in generating the scenario. Defaults to 1.
        periods (int, optional): How many consecutive close prices to stroe in each scenario. Defaults to 10.
        index_label (str, optional): Label of the index of data. Defaults to "<DTYYYYMMDD>".
        close_label (str, optional): Label of the close price column in data. Defaults to "<CLOSE>".

    Returns:
        pd.DataFrame: dataframe with scenarios - each column is a seperate scenario with close price values and length 
            of periods. If there is not enough values in data, it is filled with zeros. 
    """
    if label not in data.columns:
        return pd.DataFrame(["Error - key not found"])
    data.reset_index(inplace=True)
    scenarios = pd.DataFrame([], index=[ii for ii in range(0, periods)])
    scenario_indices = data.loc[data[label]>=threshold].index
    for index in scenario_indices:
        data_column = data.loc[index:index+periods-1, close_label].values.tolist()
        if len(data_column) < periods:
            data_column.extend([0. for ii in range(0, periods-len(data_column))])
        scenarios[str(data.loc[index, index_label])] = data_column
    data.set_index(index_label, inplace=True)
    return scenarios
