"""
This class creates an instance of the Trigno base. Put your key and license here.
"""
import threading
import time
from pythonnet import load

from Export.CsvWriter import CsvWriter
from pylsl import StreamInfo, StreamOutlet

load("coreclr")
import clr
import csv

clr.AddReference("resources/DelsysAPI")
clr.AddReference("System.Collections")

from Aero import AeroPy

key = "MIIBKjCB4wYHKoZIzj0CATCB1wIBATAsBgcqhkjOPQEBAiEA/////wAAAAEAAAAAAAAAAAAAAAD///////////////8wWwQg/////wAAAAEAAAAAAAAAAAAAAAD///////////////wEIFrGNdiqOpPns+u9VXaYhrxlHQawzFOw9jvOPD4n0mBLAxUAxJ02CIbnBJNqZnjhE50mt4GffpAEIQNrF9Hy4SxCR/i85uVjpEDydwN9gS3rM6D0oTlF2JjClgIhAP////8AAAAA//////////+85vqtpxeehPO5ysL8YyVRAgEBA0IABP4N9/1hnJme3H+1HPSxVgW2STNgm26RMpG+voOQ50FcUa3s9HUNpWyz2Y3Q8b6SHnh3NnVjfrSNQ3rnPyGbhhc="
license = "<License>  <Id>f31e72ce-1cf5-40c1-a0b9-c163fce6b9ae</Id>  <Type>Standard</Type>  <Quantity>10</Quantity>  <LicenseAttributes>    <Attribute name='Software'></Attribute>  </LicenseAttributes>  <ProductFeatures>    <Feature name='Sales'>True</Feature>    <Feature name='Billing'>False</Feature>  </ProductFeatures>  <Customer>    <Name>Jeff Hausdorff</Name>    <Email>Jhausdor@tlvmc.gov.il</Email>  </Customer>  <Expiration>Sun, 31 Dec 2034 05:00:00 GMT</Expiration>  <Signature>MEYCIQC2yLZxpAYPnVKZ+h5Gr0rBv8ScrqFDfyl+Ty1ZUkRrtAIhAPRFPUUG0GECh85U2QgRCF0FaF1Q645q3bjE3T46hOcX</Signature></License>"


class TrignoBase():
    """
    AeroPy reference imported above then instantiated in the constructor below
    All references to TrigBase. call an AeroPy method (See AeroPy documentation for details)
    """

    def __init__(self, collection_data_handler):
        self.TrigBase = AeroPy()
        self.collection_data_handler = collection_data_handler
        self.channel_guids = []
        self.channelcount = 0
        self.pairnumber = 0
        self.csv_writer = None  # Initialize later after determining the number of channels and sample rate

    # -- AeroPy Methods --
    def PipelineState_Callback(self):
        return self.TrigBase.GetPipelineState()

    def Connect_Callback(self):
        """Callback to connect to the base"""
        self.TrigBase.ValidateBase(key, license)

    def Pair_Callback(self):
        return self.TrigBase.PairSensor(self.pair_number)

    def CheckPairStatus(self):
        return self.TrigBase.CheckPairStatus()

    def CheckPairComponentAdded(self):
        return self.TrigBase.CheckPairComponentAdded()

    def Scan_Callback(self):
        """Callback to tell the base to scan for any available sensors"""
        try:
            f = self.TrigBase.ScanSensors().Result
        except Exception as e:
            print("Python demo attempt another scan...")
            time.sleep(1)
            self.Scan_Callback()

        self.all_scanned_sensors = self.TrigBase.GetScannedSensorsFound()
        print("Sensors Found:\n")
        for sensor in self.all_scanned_sensors:
            print("(" + str(sensor.PairNumber) + ") " +
                sensor.FriendlyName + "\n" +
                sensor.Configuration.ModeString + "\n")

        self.SensorCount = len(self.all_scanned_sensors)
        for i in range(self.SensorCount):
            self.TrigBase.SelectSensor(i)

        return self.all_scanned_sensors


    def Start_Callback(self, start_trigger, stop_trigger):
        """Callback to start the data stream from Sensors"""
        self.start_trigger = start_trigger
        self.stop_trigger = stop_trigger

        configured = self.ConfigureCollectionOutput()
        if configured:
            #(Optional) To get YT data output pass 'True' to Start method
            self.TrigBase.Start(self.collection_data_handler.streamYTData)
            self.collection_data_handler.threadManager(self.start_trigger, self.stop_trigger)
            self.csv_writer.lsl_outlet = StreamOutlet(self.csv_writer.lsl_info)  # Initialize LSL outlet

    def ConfigureCollectionOutput(self):
        if not self.start_trigger:
            self.collection_data_handler.pauseFlag = False

        self.collection_data_handler.DataHandler.packetCount = 0
        self.collection_data_handler.DataHandler.allcollectiondata = []

        # Pipeline Armed when TrigBase.Configure already called.
        # This if block allows for sequential data streams without reconfiguring the pipeline each time.
        # Reset output data structure before starting data stream again
        if self.TrigBase.GetPipelineState() == 'Armed':
            self.csv_writer.cleardata()
            for i in range(len(self.channelobjects)):
                self.collection_data_handler.DataHandler.allcollectiondata.append([])
            return True


        # Pipeline Connected when sensors have been scanned in sucessfully.
        # Configure output data using TrigBase.Configure and pass args if you are using a start and/or stop trigger
        elif self.TrigBase.GetPipelineState() == 'Connected':
            self.channelcount = 0
            self.TrigBase.Configure(self.start_trigger, self.stop_trigger)
            configured = self.TrigBase.IsPipelineConfigured()
            if configured:
                self.channelobjects = []
                self.plotCount = 0
                self.emgChannelsIdx = []
                globalChannelIdx = 0
                self.channel_guids = []
                sample_rate = 0

                for i in range(self.SensorCount):

                    selectedSensor = self.TrigBase.GetSensorObject(i)
                    print("(" + str(selectedSensor.PairNumber) + ") " + str(selectedSensor.FriendlyName))

                    if len(selectedSensor.TrignoChannels) > 0:
                        print("--Channels")

                        for channel in range(len(selectedSensor.TrignoChannels)):
                            ch_object = selectedSensor.TrignoChannels[channel]
                            if str(ch_object.Type) == "SkinCheck":
                                continue

                            ch_guid = ch_object.Id
                            ch_type = str(ch_object.Type)

                            get_all_channels = True
                            if get_all_channels:
                                self.channel_guids.append(ch_guid)
                                globalChannelIdx += 1

                            if ch_type == 'EMG':
                                self.emgChannelsIdx.append(globalChannelIdx-1)
                                self.plotCount += 1
                                sample_rate = round(ch_object.SampleRate, 3)  # Get the sample rate of the EMG channel

                # Initialize CsvWriter with the number of EMG channels and sample rate
                self.csv_writer = CsvWriter(len(self.emgChannelsIdx), sample_rate)
                self.csv_writer.clearall()

                # CSV Export Config
                for i in range(self.SensorCount):
                    selectedSensor = self.TrigBase.GetSensorObject(i)
                    self.csv_writer.appendSensorHeader(selectedSensor)
                    if len(selectedSensor.TrignoChannels) > 0:
                        for channel in range(len(selectedSensor.TrignoChannels)):
                            ch_object = selectedSensor.TrignoChannels[channel]
                            if str(ch_object.Type) == "SkinCheck":
                                continue
                            if not self.collection_data_handler.streamYTData:
                                self.csv_writer.appendChannelHeader(ch_object)
                                if channel > 0 & channel != len(selectedSensor.TrignoChannels):
                                    self.csv_writer.appendSensorHeaderSeperator()
                            else:
                                self.csv_writer.appendYTChannelHeader(ch_object)
                                if channel == 0:
                                    self.csv_writer.appendSensorHeaderSeperator()
                                elif channel > 0 & channel != len(selectedSensor.TrignoChannels):
                                    self.csv_writer.appendYTSensorHeaderSeperator()

                return True
        else:
            return False

    def Stop_Callback(self):
        """Callback to stop the data stream"""
        self.collection_data_handler.pauseFlag = True
        self.TrigBase.Stop()
        print("Data Collection Complete")
        self.csv_writer.data = self.collection_data_handler.DataHandler.allcollectiondata
        self.csv_writer.lsl_outlet = None  # Stop LSL outlet

    # ---------------------------------------------------------------------------------
    # ---- Helper Functions

    def getSampleModes(self, sensorIdx):
        """Gets the list of sample modes available for selected sensor"""
        sampleModes = self.TrigBase.AvailibleSensorModes(sensorIdx)
        return sampleModes

    def getCurMode(self, sensorIdx):
        """Gets the current mode of the sensors"""
        if sensorIdx >= 0 and sensorIdx <= self.SensorCount:
            curModes = self.TrigBase.GetCurrentSensorMode(sensorIdx)
            return curModes
        else:
            return None


    def setSampleMode(self, curSensor, setMode):
        """Sets the sample mode for the selected sensor"""
        self.TrigBase.SetSampleMode(curSensor, setMode)
        mode = self.getCurMode(curSensor)
        sensor = self.TrigBase.GetSensorObject(curSensor)
        if mode == setMode:
            print("(" + str(sensor.PairNumber) + ") " + str(sensor.FriendlyName) +" Mode Change Successful")
