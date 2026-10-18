# Startpaket Radar-Aktivitätserkennung

Fertig berechnete Spektrogramme und Merkmale für den Datensatz *Radar signatures of human activities* (University of Glasgow),
damit die Arbeit direkt bei Merkmalen, Verfahren und Validierung beginnen kann.

## Dateien

| Datei | Inhalt |
|---|---|
| `radar_merkmale.csv` | 1754 Zeilen (eine je Aufnahme), 11 Spalten Metadaten + 88 Merkmale |
| `merkmale_beschreibung.csv` | Name, Gruppe, Einheit und Bedeutung jedes Merkmals |
| `spektrogramme/` | 1754 Micro-Doppler-Spektrogramme als NumPy-Dateien `0000.npz` … `1753.npz` |
| `einlesen.py` | Einlesen der Tabelle und eines Spektrogramms (numpy, pandas; Abbildung mit matplotlib) |

## Metadaten-Spalten

| Spalte | Bedeutung |
|---|---|
| `datei` | Name der Rohdatei im Originaldatensatz (z. B. `1P36A01R01.dat`) |
| `kampagne` | Messkampagne (Datum, Ort) |
| `person` | eindeutige Personenkennung über alle Kampagnen (105 Personen) |
| `aktivitaet_nr`, `aktivitaet` | 1 Gehen · 2 Hinsetzen · 3 Aufstehen · 4 Aufheben · 5 Trinken · 6 Sturz |
| `wiederholung` | Nummer der Wiederholung |
| `alter` | Alter in Jahren (21–98; bei 54 Aufnahmen unbekannt) |
| `geschlecht` | m / w (bei 18 Aufnahmen unbekannt) |
| `umgebung` | Labor, Aufenthaltsraum, Wohnanlage, Seniorenzentrum |
| `dauer_s` | Dauer der Aufnahme in s (Gehen 10 s bzw. 20 s, sonst 5 s) |
| `spektrogramm` | zugehörige Datei im Ordner `spektrogramme/` |

## Spektrogramme

Je Aufnahme eine Datei `spektrogramme/NNNN.npz` (laden mit `numpy.load`):

| Feld | Inhalt |
|---|---|
| `spek` | Micro-Doppler-Spektrogramm in dB (Maximum 0 dB, unten auf −40 dB begrenzt), 128 Doppler-Bins × Zeitrahmen |
| `f_hz` | Doppler-Frequenz je Zeile in Hz (−250 … +246 Hz); Geschwindigkeit v = f · λ/2, positiv = auf das Radar zu |
| `t_s` | Zeit je Spalte in s (ein Rahmen je 32 ms) |
| `rt` | Entfernungs-Zeit-Karte in dB, 50 Entfernungszellen (je 0,375 m) × Zeitrahmen |
| `dauer_s`, `fc`, `bw` | Dauer der Aufnahme, Trägerfrequenz, Bandbreite |

Die Zahl der Zeitrahmen hängt von der Dauer der Aufnahme ab (5 s → 149, 10 s → 305, 20 s → 618).

## Wie die Merkmale entstanden sind

Rohdaten (FMCW-Radar 5,8 GHz, 1 ms je Chirp, 128 Abtastwerte) → Entfernungs-FFT je Chirp → MTI-Filter
(Butterworth-Hochpass 4. Ordnung, 3,75 Hz, entfernt ruhende Ziele) → STFT je Entfernungszelle (Hann, 256 ms, Schritt 32 ms)
→ Micro-Doppler-Spektrogramm in dB (±250 Hz, Dynamik 40 dB).
Alle Merkmale stammen aus dem mittleren **5-s-Ausschnitt** jeder Aufnahme (gleich lang für alle Aktivitäten). Geschwindigkeiten über v = f_D · λ/2 mit λ = 5,17 cm; positiv = auf das Radar zu.

## Hinweise

- Die Zeilen sind nach Kampagne, Person, Aktivität und Wiederholung sortiert.
- Die Merkmale sind nicht normiert.
- Die Merkmale sind ein Angebot, keine Musterlösung: eigene Merkmale sind ausdrücklich erwünscht.

## Quelle und Lizenz

F. Fioranelli, S. A. Shah, H. Li, A. Shrestha, S. Yang, J. Le Kernec: *Radar signatures of human activities*.
University of Glasgow, 2019. DOI [10.5525/gla.researchdata.848](https://doi.org/10.5525/gla.researchdata.848),
Lizenz CC BY 4.0. Die Merkmale sind daraus abgeleitet (Hochschule Trier, Maschinelles Lernen, WS 2026/27)
und stehen ebenfalls unter CC BY 4.0. In der Arbeit den Originaldatensatz zitieren.
