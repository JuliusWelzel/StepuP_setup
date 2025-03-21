import matplotlib.pyplot as plt
import numpy as np
import pyxdf

file_path = r"C:\Users\juliu\Desktop\kiel\stepup_setup_jw\data\test_telaviv_190325.xdf"  # Replace with your XDF file path


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

# find EMG stream
emg_stream = [s for s in streams if s['info']['type'][0] == 'EMG'][0]
# find Mocap stream
mocap_stream = [s for s in streams if s['info']['type'][0] == 'MoCap'][0]
# find EEG stream
eeg_stream = [s for s in streams if s['info']['type'][0] == 'EEG'][0]

# preparethe data
emg_times = emg_stream['time_stamps'] - emg_stream['time_stamps'][0]
emg_raw = emg_stream['time_series']

mocap_times = mocap_stream['time_stamps'] - mocap_stream['time_stamps'][0]
mocap_raw = mocap_stream['time_series']

eeg_times = eeg_stream['time_stamps'] - eeg_stream['time_stamps'][0]
eeg_raw = eeg_stream['time_series']

# print unique marker ids, and number of occurences per makrer id
marker_ids = mocap_raw[:,3]
unique_marker_ids = set(marker_ids)
for marker_id in unique_marker_ids:
    print(f"Marker {int(marker_id)}: {np.sum(marker_ids == marker_id)}")
    
# remove all markers which have less than 100 frames
for marker_id in unique_marker_ids:
    if np.sum(marker_ids == marker_id) < 150:
        idx = np.where(marker_ids == marker_id)
        mocap_raw = np.delete(mocap_raw, idx, axis=0)
        marker_ids = np.delete(marker_ids, idx)
        
# extract only marker 503
idx_34 = np.where(mocap_raw[:,3] == 600)
idx_294 = np.where(mocap_raw[:,3] == 248)
idx_296 = np.where(mocap_raw[:,3] == 220)
marker_34 = mocap_raw[idx_34][:,0:3]
marker_294 = mocap_raw[idx_294][:,0:3]
marker_296 = mocap_raw[idx_296][:,0:3]

# make 3 subplots
fig, axs = plt.subplots(3, 1, sharex=True)
# plot 1 emg
axs[0].plot(emg_times, emg_raw) 
axs[0].set_ylabel('EMG')
axs[0].set_ylim([-.7,.5])
#axs[0].legend(['RfEmgR', 'BfEmgR', 'RfEmgL', 'BfEmgL'])

# plot 2 mocap
#axs[1].plot(mocap_times[idx_34], marker_34[:,2])
axs[1].plot(mocap_times[idx_294], marker_294[:,2])
axs[1].plot(mocap_times[idx_296], marker_296[:,2])
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Z position (?)')
#axs[1].legend(['Marker 34', 'Marker 294', 'Marker 296'])

    
# plot 3 eeg
axs[2].plot(eeg_times, eeg_stream['time_series'][:,0])
axs[2].set_ylabel('EEG')
axs[2].set_xlabel('Time (s)')

# set xlim 20-30s for all subplots
for ax in axs:
    ax.set_xlim([25, 30])



# print mean and variance of diff between time stamps from eeg
mean_diff = np.mean(np.diff(eeg_times))
var_diff = np.var(np.diff(eeg_times))
print(f"Mean difference between EEG time stamps: {mean_diff}")
print(f"Variance of difference between EEG time stamps: {var_diff}")


# plot emg, mocap and eeg timestamps as as thick lines
fig, ax = plt.subplots()
ax.plot(emg_stream['time_stamps'] , np.ones_like(emg_times), linewidth=5)
ax.plot(mocap_stream['time_stamps'] , 2*np.ones_like(mocap_times), linewidth=5)
ax.plot(eeg_stream['time_stamps'] , 3*np.ones_like(eeg_times), linewidth=5)
ax.set_yticks([1,2,3])
ax.set_yticklabels(['EMG', 'MoCap', 'EEG'])
ax.set_xlabel('Time (s)')
