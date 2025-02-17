import matplotlib.pyplot as plt
import numpy as np
import pyxdf

file_path = r"C:\Users\User\Desktop\kiel\stepup\stepup_setup_jw\data\test_vicon_delsys_telaviv_170225.xdf"  # Replace with your XDF file path


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

# preparethe data
emg_times = emg_stream['time_stamps'] - emg_stream['time_stamps'][0]
emg_raw = emg_stream['time_series']

mocap_times = mocap_stream['time_stamps'] - mocap_stream['time_stamps'][0]
mocap_raw = mocap_stream['time_series']

# extract only marker 503
idx = np.where(mocap_raw[:,3] == 503)
marker_raw = mocap_raw[idx][:,0:3]

plt.plot(emg_times, emg_raw[:,0]) 
plt.plot(mocap_times, mocap_raw[:,2])
plt.xlabel('Time (s)')
plt.xlim([10,10.3])