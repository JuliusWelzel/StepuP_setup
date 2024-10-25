#########################################################################
#                                                                       #
# Program waveX_SDK_interface.py                                        #
#                                                                       #
# Python interface for Myon/Cometa systems using the waveX SDK          #
# For communication with the Myon Aktos system                          #
#                                                                       #
#                                                                       #
#########################################################################

# Import the Microsoft Common Language Runtime
import sys
import clr
import os
#from System.Reflection import Assembly

# dll_path = r"C:\Users\feder\Desktop\WaveX\WaveX_SDK\WaveX_SDK_example\PYTHON_WaveX_example\WaveX_SDK_example\WaveX.dll"

# if os.path.exists(dll_path):
#     print("Il file DLL esiste.")
# else:
#     print("Il file DLL non esiste.")

# # Aggiungi la directory della DLL a sys.path
# sys.path.append(os.path.dirname(dll_path))

# # Carica la DLL
# Assembly.LoadFile(dll_path)

# # Aggiungi il riferimento alla DLL
# clr.AddReference("WaveX")
sys.path.append(r"C:\Users\franc\Downloads\WaveX_SDK_example (1)")
a = clr.AddReference("WaveX")
b = clr.AddReference("WaveX.BSys")
c = clr.AddReference("WaveX.Common")
d = clr.AddReference("WaveX.PSys")
e = clr.AddReference("WaveX.XSys")
#f = clr.AddReference("WaveX.Common.Definitions")

# import ctypes

# Load the DLL
# wave_x_dll = ctypes.CDLL('./WaveX.dll')

# Call a function from the DLL


#b=clr.AddReference("Waveplus.DaqSys")




# Import all attributes from the Waveplus.DaqSys module
from WaveX import *
from WaveX.BSys import *
from WaveX.Common import *
from WaveX.Common.Definitions import *
from WaveX.PSys import *
from WaveX.XSys import *
#from Waveplus.DaqSys import *
#from WaveplusLab.Shared.Definitions import *


# Version information
COPYRIGHT = "Federica Berardi"
NOTE = "Using waveX library"
VERSION = "test"

from System.Reflection import Assembly
# Carica la DLL
path = r"C:\Users\franc\Downloads\WaveX_SDK_example (1)\WaveX_SDK_example\WaveX.dll"
assembly = Assembly.LoadFile(path)
#######################################
''' PARTE AGGIUNTA '''
from System.Reflection import Assembly
from System import Activator, EventHandler

daq_system_type = assembly.GetType('WaveX.DaqSystem')

if daq_system_type and daq_system_type.IsClass:
    # Use Activator to create an instance
    daq_system = Activator.CreateInstance(daq_system_type)
    print("DaqSystem initialized successfully.")
else:
    print("DaqSystem not found or is not a class in the loaded assembly.")
########################################



class WaveXAmp(DaqSystem):
    # Class that models the EMG capture system
    # It inherits attributes from the WaveX class


    def __init__(self):
        self.version = VERSION
        self.copyright = COPYRIGHT
        self.note = NOTE


    class DeviceState():
        # Python equivalent of enumerated type
        # Defines the ensembles of all states that the state machine can assume
        # Refer to Waveplus.Daq.Net software library Release 3.0.0.2

        NotConnected = 0
        Initializing = 1
        CommunicationError = 2
        InitializingError = 3
        Idle = 4
        Capturing = 5

        

    class SamplingRate():
        # Python equivalent of enumerated type
        # Defines enumerates for sampling rate
        # Refer to Waveplus.Daq.Net software library Release 3.0.0.2

        Hz_2000 = 0
    


    class DeviceError():
        # Python equivalent of enumerated type
        # NOT updated

        Success = 0
        DeviceNotConnected = 1
        SendingCommand = 2
        ReceivingCommandReply = 3
        DeviceErrorExecutingCommand = 4
        ConfiguringCapture = 5
        WrongCaptureConfigurationImuAcqType = 6
        WrongCaptureConfigurationSamplingRate = 7
        WrongCaptureConfigurationSamplingRateFromDevice = 8
        WrongCaptureConfigurationDataAvailableEventPeriod = 9
        WrongSensorConfigurationAccelerometerFullScale = 10
        WrongSensorConfigurationGyroscopeFullScale = 11
        WrongSensorConfigurationSensorType = 12 
        WrongFootSwProtocol = 13
        WrongDeviceTypeFromDevice = 14
        WrongSensorNumber = 15
        WrongFootSwSensorNumber = 16
        FootSwSensorNotInstalled = 17
        ReadingBackCaptureConfigurationSamplingRate = 18
        ReadingBackCommunicationTestData = 19
        ReadingBackSensorCommandBuffer = 20
        DataTransferThreadingStartingTimeout = 21
        ActionNotAllowedInTheCurrentDeviceState = 22
        ActionNotAllowedInTheCurrentDataTransferState = 23
        WrongDeviceState = 24
        WrongDeviceAction = 25
        TimeoutExecutingSensorCommand = 26
        CommandNotExecutedByAllSensors = 27
        WrongDaqTimeOutValue = 28
        BadSensorCommunication = 29
        SyncBuffer1Overrun = 30
        SyncBuffer2Overrun = 31
        ImuCalibrationNotAvailable = 32
        


    class DataAvailableEventPeriod():
        # Python equivalent of enumerated type
        # Defines enumerates for DataAvailableEventPeriod
        # Refer to Waveplus.Daq.Net software library Release 3.0.0.2

        ms_100 = 0
        ms_50 = 1
        ms_25 = 2
        ms_10 = 3


    class CaptureConfiguration():
        # Python equivalent of enumerated type
        # Defines enumerates for CaptureConfiguration
        # Refer to Waveplus.Daq.Net software library Release 3.0.0.2
        Emg_2kHz = 0
        Emg_2kHz_RawAccGyroMagData_100Hz = 1
        Emg_2kHz_RawAccGyroData_200Hz = 2
        Emg_2kHz_Fused6xData_100Hz = 3
        RawAccGyroMagData_400Hz = 4
        RawAccGyroData_500Hz = 5
        Fused6xData_400Hz = 6
        Fused9xData_400Hz = 7
        Mixed6xData_200Hz = 8
        Mixed9xData_200Hz = 9

    class SensorMode():
        # Python equivalent of enumerated sensor mode
        # Defines enumerates for CaptureConfiguration
        EMG_SENSOR = 0
        INERTIAL_SENSOR = 1
        ANALOG_GP_SENSOR = 2
        EMG_INTERTIAL_SENSOR = 3

    class SensorModel():
        # Python equivalent of enumerated sensor mode
        # Defines enumerates for CaptureConfiguration
        Undefined = 0
        Mini_EmgImu = 1
        Mini_Emg = 2
        Pico_EmgImu = 3
        Pico_Emg = 4
        Imu = 5
        Lite = 6


    class AccelerometerFullScale():
        # Python equivalent of enumerated type
        # Defines enumerates for CaptureConfiguration
        # Refer to Waveplus.Daq.Net software library Release 3.0.0.2
        g_2 = 0
        g_4 = 1
        g_8 = 2
        g_16 = 3


    class GyroscopeFullScale():
        # Python equivalent of enumerated type
        # Defines enumerates for CaptureConfiguration
        # Refer to Waveplus.Daq.Net software library Release 3.0.0.2
        dps_250 = 0
        dps_500 = 1
        dps_1000 = 2
        dps_2000 = 3






