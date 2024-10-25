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
picoX03_W = []
picoX03_X = []
picoX03_Y = []
picoX03_Z = []

event01W = []
event01X = []
event01Y = []
event01Z = []


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
    global event, picoX03_emg, picoX03_W, picoX03_X, picoX03_Y, picoX03_Z #channel0, channel1,channel2, channel3, channel10


    
    event = args 
    print("Number of samples is: ", args.ScanNumber)
    for i in range(0, args.ScanNumber):
        picoX03_emg.append(args.EmgSamples[2,i])
        picoX03_W.append(args.ImuSamples[2, 0, i])
        picoX03_X.append(args.ImuSamples[2, 1, i])
        picoX03_Y.append(args.ImuSamples[2, 2, i])
        picoX03_Z.append(args.ImuSamples[2, 3, i])
        # channel0.append(args.EmgSamples[0,i])
        # channel1.append(args.EmgSamples[1,i])
        # channel2.append(args.EmgSamples[2,i])
        # channel3.append(args.EmgSamples[3,i])
        # channel10.append(args.EmgSamples[9,i])
        # event01W.append(args.ImuSamples[7, 0, i])
        # event01X.append(args.ImuSamples[7, 1, i])
        # event01Y.append(args.ImuSamples[7, 2, i])
        # event01Z.append(args.ImuSamples[7, 3, i])
        # channel8.append(args.ImuSamples[7, 0, i])
        # channel8.append(args.ImuSamples[7, 1, i])
        # channel8.append(args.ImuSamples[7, 2, i])
        # channel8.append(args.ImuSamples[7, 3, i])



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

testall = False         # Set True to test everyting
captureTime = 5         # Time during which data are collected


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

if testall:

    # Test getting adminstrative data
    print("Found version info", aktos.version)
    print("Found copyright info:", aktos.copyright)
    print("Found note info: ", aktos.note)
    
    # Test getting the Aktos system state
    print("Current aktos system state is: ", printSystemState(aktos))
    
    # Retrieve number of sensors
    nrSensors = aktos.InstalledSensors
    print("Number of sensors is ", nrSensors)

    # Test enabling the sensors
    a = input("Hit <enter> key to switch sensors ON")
    aktos.EnableSensor(0)

    # Test disabling the sensors
    a = input("Hit <enter> key to switch sensors OFF")
    aktos.DisableSensor(0)

    # Test enabling the sensors
    a = input("Hit <enter> key to switch sensors ON")
    aktos.EnableSensor(0)

    # Test turning LED of sensor 1 on:
    a = input("Hit <enter> key to switch sensor 1 LED ON")
    aktos.TurnSensorLedOn(1)

    # Test turning LED of sensor 1 off:
    a = input("Hit <enter> key to switch sensor 1 LED OFF")
    aktos.TurnAllSensorLedsOff()

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
#a = input("End of test: hit <enter> key to disable all sensors and exit")
#aktos.DisableSensor(0)
#aktos.TurnAllSensorLedsOff()

#Convert lists to numpy arrays
a0 = np.asarray(channel0)
a1 = np.asarray(channel1)
a2 = np.asarray(channel2)
a3 = np.asarray(channel3)
a10 = np.asarray(channel10)

pX3 = np.asarray(picoX03_emg)
pX3W = np.asarray(picoX03_W)
pX3X = np.asarray(picoX03_X)
pX3Y = np.asarray(picoX03_Y)
pX3Z = np.asarray(picoX03_Z)


b0_W = np.asanyarray(event01W)
b0_X = np.asanyarray(event01X)
b0_Y = np.asanyarray(event01Y)
b0_Z = np.asanyarray(event01Z)

# evenly sampled time at 0.5 ms intervals
t = np.arange(0., len(pX3)*0.0005, 0.0005)
print("Number of collected samples:", len(t))

#
# Plot measured data
if testall:
    # Show all graphs
    plt.plot(t, a0,'r', t,a1,'g', t,a2, 'b', t, a3, 'y')
else:
    # Only show channel 0, the first sensor
    # plt.plot(t, pX3, 'r')
    plt.plot(t, pX3W,'r', t,pX3X,'g', t,pX3Y, 'b', t, pX3Z, 'y')
plt.ylabel('EMG signal [microvolts]')
plt.show()

reply = input("Save emg channel 0 data as text? [y/n]: ")
if reply == "y" or reply == "Y":
    name = input("Enter filename: ")
    np.savetxt(name, a0, fmt = '%2.1f', delimiter=" ")
    print("Data saved")

print("Program terminated")

