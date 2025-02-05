# Version 22-01-2025

'''
To run the entire script it must be in the same folder where the SDK is saved.
'''

import clr
import os

python_dll_path = r"C:\franc\anaconda3\python39.dll"   # Modify this path
os.environ["PYTHONNET_PYDLL"] = python_dll_path

import os
path = r"C:\Users\franc\Documents\IRCCS-ISNB\StepuP\Instrumentation\SDK\WaveX SDK\WaveX.dll" # Modify this path
print(os.path.exists(path))  # it should return 1

from System.Reflection import Assembly
# load the DLL
assembly = Assembly.LoadFile(path)

# print the class available
for type in assembly.GetTypes():
    print(type.FullName)   

from System import AppDomain
# Classes available in module WaveX
waveXAssembly = AppDomain.CurrentDomain.Load("WaveX")
for type in waveXAssembly.GetTypes():
    print(type.FullName)

# from WaveX import DaqSystem
from WaveX import *
import matplotlib.pyplot as plt
import pylsl as lsl
import numpy as np
import pyxdf
import socket
from WaveX.Common.Definitions import EmgAcqXType
from WaveX.Common.Definitions import DataAvailableEventPeriod

srate_emg = 2000 # sampling rate of the EMG sensors, can be edited at the base station
s_buffer = 0.1 # seconds to buffer and send to LSL
chunk_size = 36 # number of channels, 6 is minimum for Stepup
samples_per_read = int(srate_emg * s_buffer)

# create lsl outlet
info = lsl.StreamInfo('Cometa', 'EMG', chunk_size,  srate_emg, 'float32', 'myuid34234')
#outlet = lsl.StreamOutlet(info, chunk_size=samples_per_read, max_buffered=120) 
outlet = lsl.StreamOutlet(info)

# Initialize the Cometa Sensor using DaqSystem
daq_system = DaqSystem()

sensors = daq_system.InstalledSensors
print(f"N. of connected sensors: {sensors}")

# Configure the sensors
capture_config = daq_system.CaptureConfiguration()
capture_config.EMG_AcqXType = EmgAcqXType.Emg_2kHz
daq_system.ConfigureCapture(capture_config)
daq_system.EnableSensor(0) # Enable all sensors 

def on_data_available(sender, e):
    global emg_data, emg_data_np, srate
     
    emg_data = e.EmgSamples
    emg_data_np = np.array(emg_data)
    
    outlet.push_chunk(emg_data_np.T.tolist())  # data are transposed
    
    print("Sending data to LSL")
    
# Start capturing data
daq_system.StartCapturing(DataAvailableEventPeriod.ms_10)
print('Streaming data…')

daq_system.DataAvailable += on_data_available
# Associates the on_data_available function as a handler for the DataAvailable event
# When the system (daq_system) detects that there is data available from EMG sensors, the 
# DataAvailable event is automatically triggered, and the on_data_available function is called

# When the data is available, the system generates the DataAvailable event; 
# the on_data_available function is automatically called and handles sensing the data to LSL

try:
    while True:
        pass  
except KeyboardInterrupt:
    print("\nManual interruption received. Stopping streaming...")
finally:
    # Stop capturing data
    daq_system.StopCapturing()
    print('Streaming stopped')



 