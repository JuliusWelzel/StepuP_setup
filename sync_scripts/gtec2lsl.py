import pygds
import pylsl as lsl



# initalise the gtec device
eeg = pygds.GDS()

n_chns_eeg = 64 # number of channels, 6 is minimum for Stepup
srate = eeg.SamplingRate # sampling rate of the EEG sensors, can be edited at the base station
s_buffer = 1 # seconds to buffer and send to LSL
samples_per_read = int(srate * s_buffer)

# get impedance values and print
impedances = eeg.GetImpedanceEx()
print(impedances)

# initiate LSL outlet
info = lsl.StreamInfo('GTec', 'EEG', n_chns_eeg , srate, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info, chunk_size=samples_per_read, max_buffered=120)

# start streaming once the lab recorder is ready
input("Press Enter to start streaming...")
# start the streaming from the base station
print('Streaming data...')
while True:
    data = eeg.GetData(srate) # read data from the base station in chucks (1s)
    outlet.push_chunk(data) # push the data to the LSL outlet

eeg.Close()


