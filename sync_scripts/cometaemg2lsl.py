#########################################################
#                                                       #
#   File myon30_test.py                                 #
#                                                       #
#                                                       #
#########################################################

# Import Python libaries
#import enum
import time
import numpy as np
import matplotlib.pyplot as plt
import pylsl as lsl

# Import the kinedata Python interface for Myon hardware 
import waveX_SDK_interface as waveX

#Globals for testing
event = None
aktos = None                # Models the EMG capture system
channel0 = []               # Contains measured EMG data, channel 0
channel1 = []               # Contains measured EMG data, channel 1
channel2 = []               # Contains measured EMG data, channel 2
channel3 = []               # Contains measured EMG data, channel 3
channel10 = []              # Contains measured EMG data, channel 10
#channel8 = []               # Contains IMU data, channel 8, quaternions

# channel for testing picoX 03 with emg+imu
picoX03_emg = []


def stateChangedHandler(source, args):
    # This function handles the StateChanged events
    #print("\r\nStateChanged event handler called")
    printSystemState(aktos)
    print('from state change handler')


    
def dataAvailableHandler(source, args):
    # This function handles the DataAvailable events
    # Arguments source: ? - to be investigated
    #           args: DataAvailableEventArgs object
    # Returns resultcode
    
    #print("DataAvailable event handler called")
    global event, picoX03_emg, outlet

    
    event = args 
    print("Number of samples is: ", args.ScanNumber)
    tmp_data = args.EmgSamples[0,:]
    # print the size of the data
    print(f"Size of the data: {np.shape(tmp_data)}")
    outlet.push_chunk(tmp_data)

        # channel0.append(args.EmgSamples[0,i])
        # channel1.append(args.EmgSamples[1,i])
        # channel2.append(args.EmgSamples[2,i])
        # channel3.append(args.EmgSamples[3,i])
        # channel10.append(args.EmgSamples[9,i])




def printSystemState(daq):
    # Finds and prints the state of the system
    # Argument daq: waveplus DaqSystem object
    # Returns: state: string, text describing system state

    state = ""
    if daq.State == daq.DeviceState.NotConnected: state = "System is not connected"
    if daq.State == daq.DeviceState.Initializing: state = "System is initializing"
    if daq.State == daq.DeviceState.CommunicationError: state = "System reports communication error"
    if daq.State == daq.DeviceState.InitializingError: state ="System reports initialization error"
    if daq.State == daq.DeviceState.Idle: state =  "System is idle"
    if daq.State == daq.DeviceState.Capturing: state = "System is capturing"

    return state 

# Tests the constructor
aktos = waveX.WaveXAmp()
print(aktos)

# Create instance of CaptureConfiguration class
#cfg = aktos.CaptureConfiguration()
cfg = waveX.CaptureConfiguration() 


#RawData = 0
#Fused9xData_142Hz = 1
#Fused6xData_284Hz = 2
#Fused9xData_71Hz = 3
#Fused6xData_142Hz = 4
#Mixed6xData_142Hz = 5

cfg.EMG_IMU_AcqXType = 4 # for emg+fused #aktos.CaptureConfiguration.Emg_2kHz_Fused6xData_100Hz

aktos.ConfigureCapture(cfg)

IMU_conf = waveX.SensorConfiguration()
IMU_conf.SensorModel = 1 # 1 for MiniX #aktos.SensorModel.Pico_Emg
IMU_conf.SensorMode = 4 # 4 for EMG + IMU  #aktos.SensorMode.EMG_INTERTIAL_SENSOR
IMU_conf.AccelerometerFullScale = aktos.AccelerometerFullScale.g_16
IMU_conf.GyroscopeFullScale = aktos.GyroscopeFullScale.dps_2000

for i in range(17):
    aktos.ConfigureSensor(IMU_conf,i+1)

aktos.UpdateDisplay()
# Create instance of DataSyncBuffer
buf = waveX.DataSyncBuffer()

# Test getting the Aktos system state
print("Current aktos system state is: ", printSystemState(aktos))

# Retrieve number of sensors
nrSensors = aktos.InstalledSensors
print("Number of sensors is ", nrSensors)


# setup CONSTNATS for LSL
SRATE_EMG = 2000 # sampling rate of the EMG sensors, can be edited at the base station
BUFFER_LENGTH_SEC = 0.1 # seconds to buffer and send to LSL
N_CHANS_EMG = 8 # number of channels, 6 is minimum for Stepup
SAMPLES_PER_READ = int(SRATE_EMG * BUFFER_LENGTH_SEC)

# create lsl outlet
info = lsl.StreamInfo('Cometa', 'EMG', nrSensors,  SRATE_EMG, 'float32', 'myuid34234')
outlet = lsl.StreamOutlet(info, chunk_size=SAMPLES_PER_READ, max_buffered=120) 


# Define event handling: register event handlers
aktos.DataAvailable += dataAvailableHandler
aktos.StateChanged += stateChangedHandler

print(printSystemState(aktos))
# Start capturing EMG signals
a = input("Hit <enter> key to start data collection")
aktos.StartCapturing(aktos.DataAvailableEventPeriod.ms_100)
print("Capturing started - please wait for", captureTime, "seconds")

printSystemState(aktos)
time.sleep(captureTime)

# Stop capturing EMG signals
aktos.StopCapturing()
print("Capturing stopped")
print(printSystemState(aktos))

# Finally, disable all sensors
a = input("End of test: hit <enter> key to disable all sensors and exit")
aktos.DisableSensor(0)
aktos.TurnAllSensorLedsOff()
