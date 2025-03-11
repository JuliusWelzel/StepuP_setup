import pygds
import pylsl as lsl
import socket
import time
import numpy as np

class LabRecorder:
    def __init__(self, host="localhost", port=22345):
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = socket.create_connection((self.host, self.port))
            print(f"Connected to LabRecorder at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to LabRecorder: {e}")

    def send_command(self, command):
        if self.connection:
            try:
                self.connection.sendall(command.encode('utf-8') + b'\n')
                print(f"Sent command: {command}")
            except Exception as e:
                print(f"Failed to send command: {e}")

    def start_recording(self, root, template, run, participant, task):
        self.send_command("select all")
        filename_command = f"filename {{root:{root}}} {{template:{template}}} {{run:{run}}} {{participant:{participant}}} {{task:{task}}}"
        self.send_command(filename_command)
        self.send_command("start")

    def stop_recording(self):
        self.send_command("stop")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from LabRecorder")


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

# initiate LabRecorder
lab_recorder = LabRecorder()

lab_recorder.connect()
lab_recorder.start_recording(
    root="C:\\Data\\", #update the path to the desired location
    template="exp%n\\%p_task_%b.xdf",# update the file name template
    participant="P003", # participant ID
    task="CS" # task name one of CS (comfortable speed), FS (fixed speed), FAM (Famlilirazation)
)

# Wait for user input to start data acquisition
input("Press Enter to start data acquisition...")

# Record the start time
start_time = time.time()

# Wait for user input to get and push data
input("Press Enter to finish recording and push data...")

# Record the end time
end_time = time.time()

# Calculate the number of samples to read based on the elapsed time
elapsed_time = end_time - start_time
samples_per_read = int(srate * elapsed_time)

# Get and push data
data = eeg.GetData(samples_per_read) # read data from the base station
outlet.push_chunk(data) # push the data to the LSL outlet

# Wait for user input to end recording
input("Press Enter to stop recording...")

lab_recorder.stop_recording()
lab_recorder.disconnect()

eeg.Close()


