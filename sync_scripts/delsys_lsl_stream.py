from pytrigno import TrignoEMG
import matplotlib.pyplot as plt
import pylsl as lsl
import numpy as np
import pyxdf
import socket


srate_emg = 2000
s_buffer = 1
n_chns_emg = 4
samples_per_read = int(srate_emg * s_buffer)

dev = TrignoEMG(channel_range=(0, n_chns_emg),
                samples_per_read = samples_per_read,
                units='mV',
                host='localhost')
# set srate
dev.rate = srate_emg

# create lsl outlet
info = lsl.StreamInfo('DelSys', 'EMG', n_chns_emg + 1, srate_emg, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info, chunk_size=samples_per_read, max_buffered=120)

# connect to lab recorder
lr = socket.create_connection(("localhost", 11223))
# update lab recorder settings
lr.sendall(b"update\n")
lr.sendall(b"select all\n")
lr.sendall(b"filename {root:C:\\Users\\juliu\\Desktop\\kiel\\stepup_setup_jw\\sync_scripts\\} {template:test_emg.xdf}\n")

input("Press Enter to start streaming...")
#
# start lab recorder from python
lr.sendall(b"start\n")

dev.start()
# send data for 10 seconds
print('Streaming data...')
for i in range(4):
    # time the net function
    data = dev.read()
    outlet.push_chunk(data.T)

dev.stop()
lr.sendall(b"stop\n")

# Load in the data
data_lsl, header = pyxdf.load_xdf('test_emg.xdf', )

nms_streams = [stream["info"]["name"][0] for stream in data_lsl]

emg_times = data_lsl[0]["time_stamps"] -  data_lsl[0]["time_stamps"][0]
emg_raw = data_lsl[0]["time_series"]

plt.plot(np.array(emg_raw)[-2000:, 0])
plt.plot(data[0,:].T)

