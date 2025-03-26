import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import mne
import numpy as np
import pyxdf
from pathlib import Path



file_path = r"C:\Users\juliu\Desktop\kiel\stepup_setup_jw\data\Test_bologna_25_03_25\4_WALKING_14\sub-P001_ses-S001_task-Default_run-001_eeg_old6.xdf"  # Replace with your XDF file path

streams, header = pyxdf.load_xdf(file_path)

eeg_stream = [s for s in streams if s['info']['type'][0] == 'EEG'][0]

data = eeg_stream["time_series"].T
sfreq = float(eeg_stream["info"]["nominal_srate"][0])
montage = mne.channels.make_standard_montage("standard_1020")
channels = eeg_stream["info"]["desc"][0]["channels"][0]["channel"]
ch_names = [channel["label"][0] for channel in channels]
ch_types = [channel["type"][0] for channel in channels]
# change all labels to misc when not EEG
ch_types = ["eeg" if ch_type == "EEG" else "misc" for ch_type in ch_types]
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
raw = mne.io.RawArray(data, info)

# pick only eeg channels
raw.pick_types(eeg=True)

print(f"Computing electrode bridges")
ed_data = mne.preprocessing.compute_bridged_electrodes(raw)


bridged_idx, ed_matrix = ed_data

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), layout="constrained")
fig.suptitle("Subject 6 Electrical Distance Matrix")

# take median across epochs, only use upper triangular, lower is NaNs
ed_plot = np.zeros(ed_matrix.shape[1:]) * np.nan
triu_idx = np.triu_indices(ed_plot.shape[0], 1)
for idx0, idx1 in np.array(triu_idx).T:
    ed_plot[idx0, idx1] = np.nanmedian(ed_matrix[:, idx0, idx1])

# plot full distribution color range
im1 = ax1.imshow(ed_plot, aspect="auto")
cax1 = fig.colorbar(im1, ax=ax1)
cax1.set_label(r"Electrical Distance ($\mu$$V^2$)")

# plot zoomed in colors
im2 = ax2.imshow(ed_plot, aspect="auto", vmax=5)
cax2 = fig.colorbar(im2, ax=ax2)
cax2.set_label(r"Electrical Distance ($\mu$$V^2$)")
for ax in (ax1, ax2):
    ax.set_xlabel("Channel Index")
    ax.set_ylabel("Channel Index")


# plot psd of all channels
fig, ax = plt.subplots()
raw.plot_psd(ax=ax, fmax=100, show=False)
ax.set_title("PSD of all channels")
ax.set_ylim([80, 180])
plt.show()

# plot one random channel and one with lowest mean
fig, axs = plt.subplots(2, 1, sharex=True)
raw.plot( picks=[0], show=False)
raw.plot( picks=[np.argmin(np.mean(raw._data, axis=1))], show=False)
axs[0].set_title("PSD of random channel")
axs[1].set_title("PSD of channel with lowest mean")

# plot tf of all channels
fig, ax = plt.subplots()
raw.plot(duration=10, n_channels=10, scalings="auto", picks=[0], show=False)
raw.plot(duration=10, n_channels=10, scalings="auto", picks=[np.argmin(np.mean(raw._data, axis=1))], show=False)
ax.set_title("Time-frequency of all channels")
plt.show()
