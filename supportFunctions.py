# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:12:30 2024

@author: Valerio A. Arcobelli
         valerio.arcobelli2@unibo.it
         
This is a support script for the Automaticity Sound Processing Analysis.
"""

import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def sound_peaks_detection(samples,ploti):
    audio_signal = np.array(samples, dtype=np.float32)
    audio_signal /= np.abs(audio_signal).max()  # Normalize the signal
    
    
    # Parameters: TODO find a more dynamic way to find the proper thresholds.
    height_threshold = 0.45  # it is really sensitive!!!!
    minimum_distance_between_peaks = 25000  # it is really sensitive!!!!
    
    
    # Detect peaks
    peaks, properties = find_peaks(audio_signal, height=height_threshold, distance=minimum_distance_between_peaks)
    
    peak_indices = peaks

    if ploti:
        plt.figure(figsize=(12, 6))
        plt.plot(audio_signal, label='Original Signal')
        
        # Highlight the peaks where the time difference between consecutive peaks is less than the mean
        plt.scatter(peak_indices, audio_signal[peak_indices], color='blue', label='Peaks with Time Diff < Mean')
        
        plt.title('Original Signal with Highlighted Peaks')
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.show()
    
    return peaks, properties



# OLD CODE, not to be considered.
# import numpy as np
# from scipy.signal import find_peaks, butter, lfilter
# import matplotlib.pyplot as plt


# audio_signal = np.array(samples, dtype=np.float32)
# audio_signal /= np.abs(audio_signal).max()  # Normalize the signal


# # Parameters: TODO find a more dynamic way to find the proper thresholds.
# height_threshold = 0.37  # it is really sensitive!!!!
# minimum_distance_between_peaks = 16000  # it is really sensitive!!!!


# # Detect peaks
# peaks, properties = find_peaks(audio_signal, height=height_threshold, distance=minimum_distance_between_peaks)

# # Visualize peaks
# plt.figure(figsize=(10, 4))
# plt.plot(audio_signal, label='Normalized Audio Signal')
# plt.plot(peaks, audio_signal[peaks], "x", label='Detected Peaks')
# plt.title('Detected Peaks in Audio Signal')
# plt.xlabel('Sample Index')
# plt.ylabel('Amplitude')
# plt.legend()
# plt.show()

# # get the time difference between the peaks
# time_differences = np.diff(peaks)          
# mean_time_diff = np.mean(time_differences)
# # apply some reduction coefficient
# mean_time_diff = mean_time_diff - mean_time_diff*0.30
# less_than_mean_time_diff = time_differences[time_differences < mean_time_diff]

# # Histogram of time differences
# plt.hist(time_differences, bins=30, alpha=0.7, label='All Time Differences')
# plt.hist(less_than_mean_time_diff, bins=30, alpha=0.7, label='Less Than Mean Time Differences', color='r')
# plt.axvline(mean_time_diff, color='k', linestyle='dashed', linewidth=1, label='Mean Time Difference')
# plt.title('Histogram of Time Differences')
# plt.xlabel('Time Differences (samples)')
# plt.ylabel('Frequency')
# plt.legend()
# plt.show()

# # get index from the time differences and plot over the signal
# indices_less_than_mean = np.where(time_differences < mean_time_diff)[0]
# peak_indices = peaks[indices_less_than_mean]

# plt.figure(figsize=(12, 6))
# plt.plot(audio_signal, label='Original Signal')

# # Highlight the peaks where the time difference between consecutive peaks is less than the mean
# plt.scatter(peak_indices, audio_signal[peak_indices], color='red', label='Peaks with Time Diff < Mean')

# plt.title('Original Signal with Highlighted Peaks')
# plt.xlabel('Sample Index')
# plt.ylabel('Amplitude')
# plt.legend()
# plt.show()
