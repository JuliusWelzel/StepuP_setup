from biosiglive.gui.plot import LivePlot
from biosiglive import (
    PytrignoClient,
    RealTimeProcessingMethod,
    PlotType,
)
from time import sleep, time
interface = PytrignoClient(ip="localhost", system_rate=200)

n_electrodes = 6
muscle_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",

]
interface.add_device(
    nb_channels=n_electrodes,
    device_type="emg",
    name="emg",
    rate=2000,
    device_data_file_key="emg",
    processing_method=RealTimeProcessingMethod.ProcessEmg,
    moving_average=True,
    device_range=(0, n_electrodes-1),
)


emg_raw_plot = LivePlot(
    name="emg_raw", rate=100, plot_type=PlotType.Curve, nb_subplots=n_electrodes, channel_names=muscle_names
)
emg_raw_plot.init(plot_windows=10000, colors=(255, 0, 0), y_labels="EMG (mV)")

time_to_sleep = 1 / 100
count = 0
while True:
    tic = time()
    raw_emg = interface.get_device_data(device_name="emg")
    emg_raw_plot.update(raw_emg)
    count += 1
    loop_time = time() - tic
    real_time_to_sleep = time_to_sleep - loop_time
    if real_time_to_sleep > 0:
        sleep(real_time_to_sleep)
