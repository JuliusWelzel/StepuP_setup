import matplotlib.pyplot as plt
import numpy as np
import pyxdf
from scipy.signal import butter, filtfilt

file_path = r"C:\Users\User\Desktop\kiel\stepup\stepup_setup_jw\data\test_sync_telaviv_200225.xdf"  # Replace with your XDF file path


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

# print unique marker ids, and number of occurences per makrer id
marker_ids = mocap_raw[:,3]
unique_marker_ids = set(marker_ids)
for marker_id in unique_marker_ids:
    print(f"Marker {int(marker_id)}: {np.sum(marker_ids == marker_id)}")
    
# remove all markers which have less than 100 frames
for marker_id in unique_marker_ids:
    if np.sum(marker_ids == marker_id) < 100:
        idx = np.where(marker_ids == marker_id)
        mocap_raw = np.delete(mocap_raw, idx, axis=0)
        mocap_raw = np.delete(mocap_raw, idx, axis=0)
        marker_ids = np.delete(marker_ids, idx)
        
# extract only marker 503
idx_34 = np.where(mocap_raw[:,3] == 24)
marker_34 = mocap_raw[idx_34][:,0:3]

# prep eeg (high-pass filer 1 hz)
def highpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data, axis=0)
    return y

# Apply high-pass filter to EEG data
eeg_sample_rate = float(eeg_stream['info']['nominal_srate'][0])
eeg_filtered = highpass_filter(eeg_stream['time_series'], cutoff=1.0, fs=eeg_sample_rate)



# make 3 subplots
fig, axs = plt.subplots(3, 1, sharex=True)
# plot 1 emg
axs[0].plot(emg_times, emg_raw) 
axs[0].set_ylabel('EMG')
axs[0].legend(['RfEmgR', 'BfEmgR', 'RfEmgL', 'BfEmgL'])

# plot 2 mocap
axs[1].plot(mocap_times[idx_34], marker_34[:,2])
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Z position (?)')
axs[1].legend(['Marker 34', 'Marker 294', 'Marker 296'])

# plot 3 eeg
axs[2].plot(eeg_times, eeg_stream['time_series'][:,0])
axs[2].set_ylabel('EEG')
axs[2].set_xlabel('Time (s)')

# set xlim 20-30s for all subplots
# peak 1 = 10-17
# peak 2 = 305-312
# peak 3 = 590-612
for ax in axs:
    ax.set_xlim([890, 910])