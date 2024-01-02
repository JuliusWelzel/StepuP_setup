from biosiglive.interfaces.pytrigno import TrignoEMG
import matplotlib.pyplot as plt
import pylsl as lsl

srate_emg = 2000
s_buffer = 1
n_chns_emg = 4
dev = TrignoEMG(channel_range=(0, n_chns_emg),
                samples_per_read=srate_emg * s_buffer,
                units='mV',
                host='localhost')

# create lsl outlet
info = lsl.StreamInfo('DelSys', 'EMG', n_chns_emg, srate_emg, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info)

# test multi-channel
dev.set_channel_range((0, n_chns_emg))
dev.rate = srate_emg

input("Press Enter to start streaming...")

t_read = []
t_push = []

dev.start()
# send data for 10 seconds
for i in range(5):
    # time the net function
    data = dev.read()
    outlet.push_chunk(data.T)

dev.stop()

