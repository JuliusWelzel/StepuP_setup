import pyxdf
import matplotlib.pyplot as plt
import numpy as np

N_MARKERS = 15

# Load in the data
data, header = pyxdf.load_xdf('./data/test-walking_witherror.xdf', )

nms_streams = [stream["info"]["name"][0] for stream in data]

emg_times = data[0]["time_stamps"] -  data[0]["time_stamps"][0]
emg_raw = data[0]["time_series"]

# emg raw is a 2D array, with each row being a sample and each column being a channel
# the last column contains the marker id, find the 5 unique marker ids which occur most often
marker_ids = emg_raw[:, -1]
unique_marker_ids, counts = np.unique(marker_ids, return_counts=True)
top_5_marker_ids = unique_marker_ids[np.argsort(counts)[-N_MARKERS:]]

# show how often each marker id occurs
plt.bar(unique_marker_ids, counts)

# extract the columns 1-3 for each of the top 5 marker ids and store them each in a separate array in a dict
marker_data = {}
for marker_id in top_5_marker_ids:
    marker_data[int(marker_id)] = {
        'data': emg_raw[emg_raw[:, -1] == marker_id, 0:3],
        'time_stamps': emg_times[emg_raw[:, -1] == marker_id]
    }

# plot the data
fig, ax = plt.subplots(N_MARKERS, 1, figsize=(10, 10), sharex=True)
for i, marker_id in enumerate(top_5_marker_ids):
    ax[i].plot(marker_data[marker_id]['time_stamps'], marker_data[marker_id]['data'])
    ax[i].set_title(f"Marker {marker_id}")

