import matplotlib.pyplot as plt
import numpy as np
import pyxdf

file_path = r"C:\Users\User\Desktop\kiel\stepup\stepup_setup_jw\data\test_AllDevices_telaviv_19025.xdf"  # Replace with your XDF file path


streams, fileheader = pyxdf.load_xdf(file_path)
print("File loaded successfully.")

if streams is not None:
    print(f"Number of streams: {len(streams)}")
    for i, stream in enumerate(streams):
        print(f"\nStream {i+1}:")
        print(f"Name: {stream['info']['name'][0]}")
        print(f"Type: {stream['info']['type'][0]}")
        print(f"Channel count: {stream['info']['channel_count'][0]}")
        print(f"Sample rate: {stream['info']['nominal_srate'][0]}")
        print(f"Data points: {len(stream['time_series'])}")

# prepare to reshape the data
mocap_times = streams[0]['time_stamps'] - streams[0]['time_stamps'][0]
mocap_raw = streams[0]['time_series']
marker_ids = mocap_raw[:, 3]
unique_marker_ids = set(marker_ids)

# make the subplots each row
fig, axs = plt.subplots(3, 1, sharex=True)
for i in range(3):
    axs[i].plot(mocap_times, mocap_raw[:, [x - 4 + i for x in [3, 6, 9, 12, 15]]])
    axs[i].set_ylabel(f'Axis {i+1}')
    axs[i].set_xlabel('Time (s)')

# plot second against time for each unique marker id
dict_raw = {}
fig, ax = plt.subplots(1, 1)
for marker_id in unique_marker_ids:
    idx = np.where(marker_ids == marker_id)
    ax.plot(mocap_times[idx], mocap_raw[idx, 2].T)
    dict_raw[str(int(marker_id))] = mocap_raw[idx, :3].T
    
# add legend
ax.legend([f'Marker {int(marker_id)}' for marker_id in unique_marker_ids])

# add y label
ax.set_ylabel('Z position (?)')
ax.set_xlabel('Time (s)')
ax.set_xlim([10, 10.3])
