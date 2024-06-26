import pyxdf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore
from scipy.signal import find_peaks


# Load in the data
data, header = pyxdf.load_xdf('data/sync_mocap_eeg_motion.xdf')

nms_streams = [stream["info"]["name"][0] for stream in data]

mocap_times = data[0]["time_stamps"] -  data[0]["time_stamps"][0]
mocap_raw = data[0]["time_series"]

eeg_times = data[1]["time_stamps"] - data[0]["time_stamps"][1]
eeg_raw = data[1]["time_series"]

peak_eeg = find_peaks(zscore(eeg_raw[:,1]), distance=2)

plt.plot(mocap_times,  zscore(mocap_raw[:,2]))
plt.plot(eeg_times, zscore(eeg_raw[:,1]))
plt.xlim(15,30)
plt.ylim(0,3)
plt.axvline(eeg_times[peak_eeg[0]])