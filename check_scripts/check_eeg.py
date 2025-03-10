import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import mne
import numpy as np
import pyxdf
from pathlib import Path


fname = Path("C:/Users/juliu/Desktop/kiel/stepup_setup_jw/data/test_telaviv_050325/TreadmillTrial1.xdf")
streams, header = pyxdf.load_xdf(fname)

eeg_stream = [s for s in streams if s['info']['type'][0] == 'EEG'][0]

data = eeg_stream["time_series"].T
sfreq = float(eeg_stream["info"]["nominal_srate"][0])
montage = mne.channels.make_standard_montage("standard_1020")
ch_names = montage.ch_names[:64]
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types="eeg")
raw = mne.io.RawArray(data, info)

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
plt.show()

# plot first 20sec of time series of channel Cz
fig, ax = plt.subplots()
raw.plot(scalings=dict(eeg=100e-6), duration=1, start=14, n_channels=1)

plt.plot(eeg_stream["time_series"].T[0,:][240:260])