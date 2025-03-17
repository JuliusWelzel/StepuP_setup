import matplotlib.pyplot as plt
import numpy as np
import pyxdf

file_path = r"C:\Users\juliu\Desktop\kiel\stepup_setup_jw\data\test_sydney_110325\MaynaTestWalk01.xdf"  # Replace with your XDF file path

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

# find Mocap stream
mocap_stream = [s for s in streams if s['info']['type'][0] == 'MoCap'][0]
# find EEG stream
eeg_stream = [s for s in streams if s['info']['type'][0] == 'EEG'][0]
# find Marker stream
marker_stream = [s for s in streams if s['info']['type'][0] == 'Markers'][0]

# preparethe dats
mocap_times = mocap_stream['time_stamps'] - eeg_stream['time_stamps'][0]
mocap_raw = mocap_stream['time_series']

eeg_times = eeg_stream['time_stamps'] - eeg_stream['time_stamps'][0]
eeg_raw = eeg_stream['time_series']

# information about the columns
# <Column A>Timestamps
# <Colum B(0)>FrameNumbers
# <Colum (1)C>Frame rate
# <Colum D(2)>Total Time that the loop has taken for capturing the data from Vicon(It's just for our understanding, don't worry about it)
# <Colum E(3)-CF(82)>Vicon Data<Colum BM(63)-BT(70)>Left Foot and Right Foot(Extra Markers)<Colum BU(71)-CF(82)>Unlabeled Markers>
# <Colum CG(83)-AAV(722)EMG Data>We used only two sensors, that 'why all other columns are zero
# <Colum AAW(723)-AHV(904)>Force Plates Data

# extract mocap marker data
mocap_times = mocap_raw[:,0]
frames_mocap = mocap_raw[:,1]
vicon_data = mocap_raw[:,3:83]
lf_z_vicon = mocap_raw[:,65]
emg_data = mocap_raw[:,83:723]
some_emg = emg_data[:,0]

# make 3 subplots
fig, axs = plt.subplots(3, 1, sharex=True)
# plot 1 emg
axs[0].plot(mocap_times, some_emg) 
axs[0].set_ylabel('EMG')
#axs[0].set_ylim([-.7,.5])
#axs[0].legend(['RfEmgR', 'BfEmgR', 'RfEmgL', 'BfEmgL'])

# plot 2 mocap
#axs[1].plot(mocap_times[idx_34], marker_34[:,2])
axs[1].plot(mocap_times, lf_z_vicon)
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Z position (?)')
#axs[1].legend(['Marker 34', 'Marker 294', 'Marker 296'])

    
# plot 3 eeg
axs[2].plot(eeg_times, eeg_stream['time_series'][:,0])
axs[2].set_ylabel('EEG')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylim([-100, 100])

# set xlim 20-30s for all subplots
for ax in axs:
    ax.set_xlim([10, 25])
