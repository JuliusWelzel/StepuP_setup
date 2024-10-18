from sync_scripts.pytrigno import TrignoEMG
import matplotlib.pyplot as plt
import pylsl as lsl

srate_emg = 2148 # sampling rate of the EMG sensors, can be edited at the base station
s_buffer = 1 # seconds to buffer and send to LSL
n_chns_emg = 6 # number of channels, 6 is minimum for Stepup
samples_per_read = int(srate_emg * s_buffer)

# initiate python connection to the Trigno base station, make sure host is correctly selected
dev = TrignoEMG(channel_range=(0, n_chns_emg),
                samples_per_read = samples_per_read,
                units='mV',
                host='localhost')
# set srate at the base station
dev.rate = srate_emg

# create lsl outlet
info = lsl.StreamInfo('DelSys', 'EMG', n_chns_emg + 1, srate_emg, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info, chunk_size=samples_per_read, max_buffered=120)

# start streaming once the lab recorder is ready
input("Press Enter to start streaming...")

# start the streaming from the base station
dev.start()
# send data forever
print('Streaming data...')
while True:
    data = dev.read() # read data from the base station in chucks
    outlet.push_chunk(data.T) # push the data to the LSL outlet



