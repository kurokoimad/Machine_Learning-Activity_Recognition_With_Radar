"""Startpaket einlesen: Merkmalstabelle mit Labels und Spektrogramme.

Benötigt: numpy, pandas (für die Abbildung matplotlib).   Aufruf im Ordner des Startpakets: python einlesen.py
"""
import numpy as np
import pandas as pd

tab = pd.read_csv("radar_merkmale.csv")
beschreibung = pd.read_csv("merkmale_beschreibung.csv")

META = ["datei", "kampagne", "person", "aktivitaet_nr", "aktivitaet", "wiederholung",
        "alter", "geschlecht", "umgebung", "dauer_s", "spektrogramm"]
meta = tab[META]                    # Labels und Angaben zu jeder Aufnahme
X = tab.drop(columns=META)          # 88 Merkmale, eine Zeile je Aufnahme


def lade_spektrogramm(i):
    """Spektrogramm der Aufnahme in Zeile i: Doppler x Zeit in dB, Doppler-Achse in Hz, Zeitachse in s."""
    d = np.load(tab.loc[i, "spektrogramm"])
    return d["spek"].astype(np.float32), d["f_hz"], d["t_s"]


if __name__ == "__main__":
    print(f"{len(tab)} Aufnahmen, {X.shape[1]} Merkmale, {meta['person'].nunique()} Personen")
    print(meta["aktivitaet"].value_counts().to_string())

    s, f, t = lade_spektrogramm(0)
    print("Spektrogramm 0:", meta.loc[0, "aktivitaet"], s.shape, f"{f[0]:.0f} … {f[-1]:.0f} Hz, {t[-1]:.2f} s")

    try:
        import matplotlib.pyplot as plt
        v = f * (3e8 / 5.8e9) / 2                        # Doppler-Frequenz -> Geschwindigkeit in m/s
        plt.pcolormesh(t, v, s, shading="auto")
        plt.xlabel("Zeit in s"); plt.ylabel("Geschwindigkeit in m/s"); plt.colorbar(label="dB")
        plt.title(meta.loc[0, "aktivitaet"]); plt.show()
    except ImportError:
        pass
