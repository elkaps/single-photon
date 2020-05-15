import numpy as np
from numba import jit
from modules.coincidence_counts import count_coincidences


@jit(nopython=True)
def g2_heralded(time_arr, sync_arr, coinc_window, tau_max, tau_bin_size, lead_id=2, lag_id=3):

    tau_arr = np.arange(-tau_max+tau_bin_size, tau_max, tau_bin_size)

    signal_events = np.where(sync_arr == 1, 1, 0)
    lead_events = np.where(sync_arr == lead_id, 1, 0)
    lag_events = np.where(sync_arr == lag_id, 1, 0)

    N_A = np.sum(signal_events)
    N_AB = count_coincidences(
        time_arr, sync_arr, coinc_window, signal_id=1, idler_id=lead_id)
    N_AC = count_coincidences(
        time_arr, sync_arr, coinc_window, signal_id=1, idler_id=lag_id)

    total_time = time_arr[-1]

    # dt contains the time difference time[i+1] - time[i]
    dt = np.diff(time_arr)

    g2 = []

    for tau in tau_arr:

        coincidence_counter = 0

        for index, c in enumerate(signal_events[1:-1]):
            # index starts at 0 and is therefore the index of the previous event

            # Skip if there is no event
            if c == 0:
                continue

            # time of the event
            current_time = time_arr[index+1]

            # initialize variables
            lead_previous_time = 0
            lead_next_time = total_time+2*coinc_window
            lag_previous_time = 0
            lag_next_time = total_time+2*coinc_window

            # search for the previous and next lead event
            for search_index in range(index, 0):
                if lead_events[search_index] == 1:
                    lead_previous_time = time_arr[search_index]
                    break

            for search_index in range(index+2, len(lead_events)):
                if lead_events[search_index] == 1:
                    lead_next_time = time_arr[search_index]
                    break

            # search for the previous and next lag event
            for search_index in range(index, 0):
                if lag_events[search_index] == 1:
                    lag_previous_time = time_arr[search_index]
                    break

            for search_index in range(index+2, len(lag_events)):
                if lag_events[search_index] == 1:
                    lag_next_time = time_arr[search_index]
                    break

            # time difference between the events
            dt_lead_prev = lead_previous_time - current_time
            dt_lead_next = lead_next_time - current_time

            dt_lag_prev = lag_previous_time - current_time
            dt_lag_next = lag_next_time - current_time

            # check if the event occurred in the coincidence window
            coinc_found = False
            if abs(dt_lead_next) <= coinc_window/2:
                # check if a lag events occur around time tau
                if tau - tau_bin_size/2 <= dt_lag_next <= tau + tau_bin_size/2:
                    coinc_found = True
            if abs(dt_lead_prev) <= coinc_window/2:
                # check if a lag events occur around time tau
                if tau - tau_bin_size/2 <= dt_lag_prev <= tau + tau_bin_size/2:
                    coinc_found = True

            if coinc_found:
                coincidence_counter += 1

        g2.append(coincidence_counter/(N_AB*N_AC)*total_time /
                  coinc_window*coinc_window/tau_bin_size)

    return g2, tau_arr
