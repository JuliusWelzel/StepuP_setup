import pyxdf
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore
from scipy.signal import find_peaks


# Load in the data
data, header = pyxdf.load_xdf('data/test_emg.xdf')

nms_streams = [stream["info"]["name"][0] for stream in data]

emg_times = data[0]["time_stamps"] -  data[0]["time_stamps"][0]
emg_raw = data[0]["time_series"]

plt.plot(emg_times, emg_raw[:,1])
