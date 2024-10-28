import clr
import os
import sys

#####
# Get system setup
#####

python_dll_path = r"C:\franc\anaconda3\python39.dll"  # Modify this path according to your Python installation
os.environ["PYTHONNET_PYDLL"] = python_dll_path

sys.path.append(r"C:\Users\franc\Documents\IRCCS-ISNB\StepuP\Instrumentation\SDK\WaveX SDK")
a = clr.AddReference("WaveX")

path = r"C:\Users\franc\Documents\IRCCS-ISNB\StepuP\Instrumentation\SDK\WaveX SDK\WaveX.dll"
if os.path.exists(path):
    print(f"The DLL file was found at: {path}")
else:
    print(f"Error: The DLL file was not found at: {path}")


#####
# load the DLL
#####

from System.Reflection import Assembly
assembly = Assembly.LoadFile(path)

# Print available type names
for type in assembly.GetTypes():
    print(type.FullName)
    
from System import AppDomain
# Show all classes in the WaveX module
waveXAssembly = AppDomain.CurrentDomain.Load("WaveX")
for type in waveXAssembly.GetTypes():
    print(type.FullName)

daq_system_type = assembly.GetType('WaveX.DaqSystem')

if daq_system_type and daq_system_type.IsClass:
    # Use Activator to create an instance
    daq_system = Activator.CreateInstance(daq_system_type)
    print("DaqSystem initialized successfully.")
else:
    print("DaqSystem not found or is not a class in the loaded assembly.")

# from load LSL relevant packages
import matplotlib.pyplot as plt
import pylsl as lsl
import numpy as np

# setup CONSTNATS for LSL
SRATE_EMG = 2000 # sampling rate of the EMG sensors, can be edited at the base station
BUFFER_LENGTH_SEC = 1 # seconds to buffer and send to LSL
N_CHANS_EMG = 8 # number of channels, 6 is minimum for Stepup
SAMPLES_PER_READ = int(SRATE_EMG * BUFFER_LENGTH_SEC)

# create lsl outlet
info = lsl.StreamInfo('Cometa', 'EMG', N_CHANS_EMG,  SRATE_EMG, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info, chunk_size=SAMPLES_PER_READ, max_buffered=120) 


# Connect and configure the sensors    
from WaveX.Common.Definitions import EmgAcqXType
from WaveX.Common.Definitions import DataAvailableEventPeriod
from WaveX.Common.Definitions import DataAvailableEventArgs

sensors = daq_system.InstalledSensors
print(f"Number of connected sensors: {sensors}")

#Configure the sensors
capture_config = daq_system.CaptureConfiguration()

capture_config.EMG_AcqXType = EmgAcqXType.Emg_2kHz # set sampling rate to 2 kHz

daq_system.ConfigureCapture(capture_config)
daq_system.EnableSensor(0) # Enable all sensors 

data_counter = 0

def stateChangedHandler(source, args):
    # This function handles the StateChanged events
    #print("\r\nStateChanged event handler called")
    printSystemState(daq_system)
    print('from state change handler')

def dataAvailableHandler(source, args: DataAvailableEventArgs):
    global data_counter
    # Print the number of samples received
    print("Number of samples is: ", args.ScanNumber)

    # Convert the samples to a NumPy array for all channels
    emg_data_np = np.array(args.EmgSamples)  # Get all samples for streaming

    # print type of args.EmgSamples
    # Print the type and shape of the EMG samples for debugging
    print(f"Type of EMG samples: {type(args.EmgSamples)}")
    print(f"Shape of EMG samples: {np.shape(args.EmgSamples)}")
    data_counter += 1

    # Push the entire dataset to the LSL outlet
    outlet.push_chunk(emg_data_np.T)  # Transpose if needed for LSL format

# Subscription to the event
daq_system.DataAvailable += dataAvailableHandler
#daq_system.StateChanged += stateChangedHandler

print('Start Streaming...')
daq_system.StartCapturing(DataAvailableEventPeriod.ms_100)

#daq_system.StopCapturing()
#print(dir(DataAvailableEventPeriod))


# test using random data
'''
import time
while True:
    emg_data = np.random.randn(8).tolist()  # Generate random data (8 channels)
    outlet.push_sample(emg_data)            # Push each sample to LSL
    time.sleep(0.0005)  # Sleep for 0.5 ms (simulates 2000 Hz sampling rate)
'''