import clr
import os
import sys

python_dll_path = r"C:\franc\anaconda3\python39.dll"  # Modify this path according to your Python installation
os.environ["PYTHONNET_PYDLL"] = python_dll_path

sys.path.append(r"C:\Users\franc\Documents\IRCCS-ISNB\StepuP\Instrumentation\SDK\WaveX SDK")
a = clr.AddReference("WaveX")

import os
path = r"C:\Users\franc\Documents\IRCCS-ISNB\StepuP\Instrumentation\SDK\WaveX SDK\WaveX.dll"
print(os.path.exists(path))  # expected outpuut: True

from System.Reflection import Assembly
# load the DLL
assembly = Assembly.LoadFile(path)

# Stampa i nomi dei tipi disponibili
for type in assembly.GetTypes():
    print(type.FullName)
    

from System import AppDomain
# Mostra tutte le classi nel modulo WaveX
waveXAssembly = AppDomain.CurrentDomain.Load("WaveX")
for type in waveXAssembly.GetTypes():
    print(type.FullName)

# from WaveX import DaqSystem
#import WaveX
from WaveX import *
import matplotlib.pyplot as plt
import pylsl as lsl
import numpy as np
import pyxdf
import socket

srate_emg = 2000# sampling rate of the EMG sensors, can be edited at the base station
s_buffer = 1 # seconds to buffer and send to LSL
N_chns_emg = 8 # number of channels, 6 is minimum for Stepup
samples_per_read = int(srate_emg * s_buffer)

# create lsl outlet
info = lsl.StreamInfo('Cometa', 'EMG', N_chns_emg,  srate_emg, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info, chunk_size=samples_per_read, max_buffered=120) 

from System.Reflection import Assembly
from System import Activator, EventHandler

daq_system_type = assembly.GetType('WaveX.DaqSystem')

if daq_system_type and daq_system_type.IsClass:
    # Use Activator to create an instance
    daq_system = Activator.CreateInstance(daq_system_type)
    print("DaqSystem initialized successfully.")
else:
    print("DaqSystem not found or is not a class in the loaded assembly.")


sensors = daq_system.InstalledSensors
print(f"Numero di sensori connessi: {sensors}")

#Configure the sensors
capture_config = daq_system.CaptureConfiguration()

    
from WaveX.Common.Definitions import EmgAcqXType
from WaveX.Common.Definitions import DataAvailableEventPeriod
from WaveX.Common.Definitions import DataAvailableEventArgs

capture_config.EMG_AcqXType = EmgAcqXType.Emg_2kHz

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
    
    data_counter += 1
    
    # Print the data shape for debugging
    print(f"Data shape before pushing to LSL: {np.shape(emg_data_np.T)}")
    print(f"Data before pushing to LSL: {emg_data_np.T}")

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