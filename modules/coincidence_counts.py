import numpy as np
from numba import jit

@jit(nopython=True)
def find_closest_prev_event_index(time_arr, event_arr, index, event_id):
    """looks for the soonest event that happened before index"""
    previous_time = 0
    for previous_search_index in range(index-1, -1, -1):
        if event_arr[previous_search_index] == event_id:
            previous_time = time_arr[previous_search_index]
            break
    
    dt_prev = time_arr[index] - previous_time

    # no previous event was found
    if previous_time == 0:
        dt_prev = time_arr[-1]
        previous_search_index = 0

        
    return previous_search_index, dt_prev


@jit(nopython=True)
def find_closest_next_event_index(time_arr, event_arr, index, event_id):
    """looks for the soonest event that happened after index""" 
    next_time = time_arr[-1]
    for next_search_index in range(index+1, len(event_arr)):
        if event_arr[next_search_index] == event_id:
            next_time = time_arr[next_search_index]
            break
    
    dt_next = next_time - time_arr[index] 
        
    return next_search_index, dt_next
        

@jit(nopython=True)
def find_closest_event_index(time_arr, event_arr, index, event_id):
    next_index, dt_next = find_closest_next_event_index(time_arr, event_arr, index, event_id)
    prev_index, dt_prev = find_closest_prev_event_index(time_arr, event_arr, index, event_id)
    
    closest_index = prev_index
    dt = dt_prev
    if dt_next < dt_prev:
        closest_index = next_index
        dt = dt_next
        
    return closest_index, dt

@jit(nopython=True)
def count_coincidences(time_arr, sync_arr, coinc_window, channel_1_id=1, channel_2_id=2):    
    coinc_counter = 0
    for index, event in enumerate(sync_arr):
        if event != channel_1_id:
            continue
        
        _, dt = find_closest_event_index(time_arr, sync_arr, index, channel_2_id)
        
        if dt > coinc_window/2:
            continue
        
        coinc_counter += 1
    
    return coinc_counter


# @jit(nopython=True)
# def count_coincidences(time_arr, sync_arr, coinc_window, signal_id=1, idler_id=2):
#     """count the coincidences of a measurement
#     Args:
#         time_arr (np.array): Array containing the timestamp in picoseconds
#         sync_arr (np.array): Array containing the detector index in which the event occurred
#         coinc_window (int): Coincidence window in picoseconds 
#     """

#     total_time = time_arr[-1]
    
#     # dt contains the time difference time[i+1] - time[i]
#     dt = np.diff(time_arr)

#     coinc_counter = 0

#     for index, (event, dt_i) in enumerate(zip(sync_arr[1:-1], dt)):
#         # event is the channel in which an event occurred
#         # index starts at 0 and is therefore the index of the previous event
#         # dt is the time difference between the event and the previous event 
        
#         coinc_found = False

#         # only look for idler events
#         if event == idler_id:

#             # check if the previous event is in a different channel
#             if sync_arr[index] != event:
#                 if dt_i <= coinc_window/2:
#                     coinc_found = True
                    
#             # check if the next index exists         
#             if index+2 < len(sync_arr):

#                 # check if the next event is in a different channel
#                 if sync_arr[index+2] != event:
#                     if dt[index+1] <= coinc_window/2:
#                         coinc_found = True
        
#         if coinc_found:
#             coinc_counter += 1

#     return coinc_counter