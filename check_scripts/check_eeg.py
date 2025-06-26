import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import mne
import numpy as np
import pyxdf
from pathlib import Path


file_path = r"C:\Users\User\Desktop\kiel\stepup\stepup_setup_jw\data\Walking1.xdf"  # Replace with your XDF file path

streams, header = pyxdf.load_xdf(file_path)

eeg_stream = [s for s in streams if s['info']['type'][0] == 'EEG'][0]

data = eeg_stream["time_series"].T
sfreq = float(eeg_stream["info"]["nominal_srate"][0])

n_channels = eeg_stream['time_series'].shape[1]
# Example: Set your channel names and types
montage = mne.channels.make_standard_montage("standard_1020")
ch_names = montage.ch_names[:n_channels]  # Use the first n_channels from the montage
ch_types = ['eeg'] * n_channels  # or mix as needed

# change all labels to misc when not EEG
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
raw = mne.io.RawArray(data, info)

raw.set_montage(montage, match_case=False)

# pick only eeg channels
raw.pick_types(eeg=True)

print(f"Computing electrode bridges")
ed_data = mne.preprocessing.compute_bridged_electrodes(raw)


bridged_idx, ed_matrix = ed_data

fig, (ax1) = plt.subplots(1, 1, figsize=(8, 8), layout="constrained")
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


# plot psd of all channels
fig, ax = plt.subplots()
raw.plot_psd(ax=ax, fmax=40, show=False)
ax.set_title("PSD of all channels")
ax.set_ylim([110, 160])
plt.show()

