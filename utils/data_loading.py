import pandas as pd
# use pandas for data loading since it's much faster thaan numpy

def read_csv(path):
    return pd.read_csv(path, delimiter=',', dtype=float).T.to_numpy()