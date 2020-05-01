import numpy as np
from numba import jit

@jit(nopython=True)
def count_coincidences(time_arr, sync_arr, coinc_window, signal_id=1, idler_id=2):
    """count the coincidences of a measurement
    Args:
        time_arr (np.array): Array containing the timestamp in picoseconds
        sync_arr (np.array): Array containing the detector index in which the event occurred
        coinc_window (int): Coincidence window in picoseconds 
    """

    total_time = time_arr[-1]
    
    # dt contains the time difference time[i+1] - time[i]
    dt = np.diff(time_arr)

    coinc_counter = 0

    for index, (event, dt_i) in enumerate(zip(sync_arr[1:-1], dt)):
        # event is the channel in which an event occurred
        # index starts at 0 and is therefore the index of the previous event
        # dt is the time difference between the event and the previous event 
        
        coinc_found = False

        # only look for idler events
        if event == idler_id:

            # check if the previous event is in a different channel
            if sync_arr[index] != event:
                if dt_i <= coinc_window/2:
                    coinc_found = True
                    
            # check if the next index exists         
            if index+2 < len(sync_arr):

                # check if the next event is in a different channel
                if sync_arr[index+2] != event:
                    if dt[index+1] <= coinc_window/2:
                        coinc_found = True
        
        if coinc_found:
            coinc_counter += 1

    return coinc_counter