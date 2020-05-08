import pandas as pd
import numpy as np
# use pandas for data loading since it's much faster thaan numpy

def read_csv(path):
    df = pd.read_csv(path, delimiter=',', dtype={0: 'uint8', 1:'uint64'}, chunksize=1e7)

    sync = np.array([], dtype=np.uint8)
    time = np.array([], dtype=np.uint64)

    for chunk in df:
        sync = np.append(sync, chunk.T.iloc[0].to_numpy(dtype=np.uint8))
        time = np.append(time, chunk.T.iloc[1].to_numpy(dtype=np.uint64))
 
    return sync, time


# sync, time = read_csv('measurements/coincidence_counts/window_width/5_2_1_window_width.csv')