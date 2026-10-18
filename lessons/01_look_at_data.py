"""Lesson 1: look at the data before doing any machine learning.

Plots one micro-Doppler spectrogram per activity, side by side.
Run from the project root:  .venv/bin/python lessons/01_look_at_data.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "Radar-Startpaket"
WAVELENGTH = 3e8 / 5.8e9  # radar wavelength in m (5.8 GHz carrier)

tab = pd.read_csv(DATA / "radar_merkmale.csv")

fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharey=True)
for ax, (nr, group) in zip(axes.flat, tab.groupby("aktivitaet_nr")):
    row = group.iloc[0]  # first recording of this activity
    d = np.load(DATA / row["spektrogramm"])
    v = d["f_hz"] * WAVELENGTH / 2  # Doppler frequency -> velocity in m/s
    im = ax.pcolormesh(d["t_s"], v, d["spek"], shading="auto", vmin=-40, vmax=0)
    ax.set_title(f"{nr}: {row['aktivitaet']}  ({row['person']})")
    ax.set_xlabel("time in s")
    ax.set_ylim(-4, 4)
for ax in axes[:, 0]:
    ax.set_ylabel("velocity in m/s (+ = towards radar)")
fig.colorbar(im, ax=axes, label="power in dB")

out = Path(__file__).resolve().parent / "01_spectrograms.png"
fig.savefig(out, dpi=110, bbox_inches="tight")
print("saved", out)
