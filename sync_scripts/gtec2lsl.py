import pygds
import pylsl as lsl
import socket
import time
import numpy as np

class LabRecorder:
    """
    A class to interface with the LabRecorder software for recording data streams.
    Attributes:
        host (str): The hostname or IP address of the LabRecorder server.
        port (int): The port number of the LabRecorder server.
        connection (socket.socket): The socket connection to the LabRecorder server.
    """
    def __init__(self, host="localhost", port=22345):
        """
        Initializes the LabRecorder with the specified host and port.
        Args:
            host (str): The hostname or IP address of the LabRecorder server. Defaults to "localhost".
            port (int): The port number of the LabRecorder server. Defaults to 22345.
        """
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """"
        This method attempts to create a socket connection to the LabRecorder server
        using the specified host and port. If the connection fails, it prompts the
        user to enter a new port number and retries the connection.

        Attributes:
            self.connection (socket.socket): The socket connection to the LabRecorder server.
            self.host (str): The hostname or IP address of the LabRecorder server.
            self.port (int): The port number of the LabRecorder server.

        Raises:
            Exception: If the connection to the LabRecorder server fails.
        """
        while True:
            try:
                self.connection = socket.create_connection((self.host, self.port))
                print(f"Connected to LabRecorder at {self.host}:{self.port}")
                break
            except Exception as e:
                print(f"Failed to connect to LabRecorder: {e}")
                self.port = int(input("Enter a new port number: "))

    def send_command(self, command):
        """
        Sends a command to the LabRecorder server.
        Args:
            command (str): The command to send to the LabRecorder server.
        """
        if self.connection:
            try:
                self.connection.sendall(command.encode('utf-8') + b'\n')
                print(f"Sent command: {command}")
            except Exception as e:
                print(f"Failed to send command: {e}")

    def start_recording(self):
        """
        Starts recording data with the specified parameters.

        """
        self.send_command("select all")
        self.send_command("start")

    def stop_recording(self):
        """
        Stops the recording.
        """
        self.send_command("stop")

    def disconnect(self):
        """
        Closes the connection to the LabRecorder server.
        """
        if self.connection:
            self.connection.close()
            print("Disconnected from LabRecorder")


# print initial message
print("Initialising GDS device...")

# initalise the gtec device
eeg = pygds.GDS()

n_chns_eeg = 64 # number of channels, 6 is minimum for Stepup
srate = eeg.SamplingRate # sampling rate of the EEG sensors, can be edited at the base station
s_buffer = 1 # seconds to buffer and send to LSL
samples_per_read = int(srate * s_buffer)

# get impedance values and print
impedances = eeg.GetImpedanceEx()

print("Initialising LSL outlet...")
# initiate LSL outlet
info = lsl.StreamInfo('GTec', 'EEG', n_chns_eeg , srate, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info, chunk_size=samples_per_read, max_buffered=120)

# initiate LabRecorder
lab_recorder = LabRecorder()

# Connect to LabRecorder
lab_recorder.connect()

# Wait for user input to start data acquisition
input("Press Enter to start data acquisition...")

# Start recording, specify path and file name template
lab_recorder.start_recording()

# store lsl start time
start_time = lsl.local_clock()

# Wait for user input to get and push data
input("Press Enter to finalize recording and push data...")

# Record the end time
end_time = lsl.local_clock()

# Calculate the number of samples to read based on the elapsed time
elapsed_time = lsl.local_clock() - start_time
samples_per_read = int(srate * elapsed_time)

# Get and push data
start_read_time = lsl.local_clock()
data = eeg.GetData(samples_per_read) # read data from the base station
end_read_time = lsl.local_clock()

# print if data has been successfully read from device
if data is not None:
    print(f"Data read successfully: {data.shape}")
    print(f"Time taken to read data: {end_read_time - start_read_time} seconds")

start_push_time = lsl.local_clock()
outlet.push_chunk(data, timestamp=start_read_time) # push the data to the LSL outlet
end_push_time = lsl.local_clock()

# print if data has been successfully pushed to LSL
print(f"Data pushed to LSL")
print(f"Time taken to push data: {end_push_time - start_push_time} seconds")

# Wait for user input to end recording
input("Press Enter to stop recording and close LSL...")

# Stop recording after user input
lab_recorder.stop_recording()

# pause for 1 second
time.sleep(1)
lab_recorder.disconnect()

eeg.Close()
