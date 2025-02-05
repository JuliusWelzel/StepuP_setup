import csv
import numpy as np
from pylsl import StreamInfo, StreamOutlet

class CsvWriter:
    filename = "data.csv"

    def __init__(self, num_channels, sample_rate):
        self.h1_sensors = []
        self.h2_channels = []
        self.data = [[] for _ in range(num_channels)]  # Initialize data with the correct number of channels
        self.lsl_info = StreamInfo('DelsysData', 'EMG', num_channels, sample_rate, 'float32', 'myuid34234')
        self.lsl_outlet = StreamOutlet(self.lsl_info)

    def appendSensorHeader(self, sensor):
        self.h1_sensors.append("(" + str(sensor.PairNumber) + ")" + sensor.FriendlyName)

    def appendSensorHeaderSeperator(self):
        self.h1_sensors.append("")

    def appendYTSensorHeaderSeperator(self):
        self.h1_sensors.append("")
        self.h1_sensors.append("")

    def appendChannelHeader(self, channel):
        self.h2_channels.append(channel.Name + " (" + str(round(channel.SampleRate, 3)) + ")")

    def appendYTChannelHeader(self, channel):
        self.h2_channels.append(channel.Name + " Time Series")
        self.h2_channels.append(channel.Name + " (" + str(round(channel.SampleRate, 3)) + ")")

    def push_to_lsl(self, data_chunk):
        self.lsl_outlet.push_chunk(data_chunk)

    def exportCSV(self):
        try:
            with open(self.filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                maxlen = 0

                csvwriter.writerow(self.h1_sensors)
                csvwriter.writerow(self.h2_channels)

                for chan_data in self.data:
                    length = len(chan_data)
                    if length > maxlen:
                        maxlen = length

                for i in range(maxlen):
                    row = []
                    for chan_data in self.data:
                        try:
                            if chan_data[i] == "":
                                row.append("")
                            else:
                                row.append(chan_data[i])
                        except IndexError:
                            row.append("")

                    csvwriter.writerow(row)
                    self.push_to_lsl(row)  # Push each row to LSL

        except PermissionError:
            print("ERROR: CSV Export failed because the file is being used by another program")
            return False

        except Exception as e:
            print("CSV Export Failed: " + e)
            return False

        return True

    def exportYTCSV(self):
        try:
            with open(self.filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                maxlen = 0

                csvwriter.writerow(self.h1_sensors)
                csvwriter.writerow(self.h2_channels)

                for chan_data in self.data:
                    length = len(chan_data)
                    if length > maxlen:
                        maxlen = length

                for i in range(maxlen):
                    row = []
                    if i == 100:
                        print()
                    for chan_data in self.data:
                        try:
                            timeval = chan_data[i].Item1
                            cdata = chan_data[i].Item2
                            if chan_data[i] == "":
                                row.append("")
                                row.append("")
                            else:
                                row.append(timeval)
                                row.append(cdata)
                        except IndexError:
                            row.append("")
                            row.append("")

                    csvwriter.writerow(row)
                    self.push_to_lsl(row)  # Push each row to LSL
        except PermissionError:
            print("ERROR: CSV Export failed because the file is being used by another program")
            return False

        except Exception:
            print("CSV Export Failed")
            return False

        return True

    def clearall(self):
        self.h1_sensors = []
        self.h2_channels = []
        self.data = [[] for _ in range(len(self.data))]  # Reinitialize data with the same number of channels

    def cleardata(self):
        self.data = [[] for _ in range(len(self.data))]  # Reinitialize data with the same number of channels
