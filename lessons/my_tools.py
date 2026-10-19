import numpy as np

# This function solves both problems we found: 
# every picture now has the same shape, so the code can stack them, 
# and the width no longer gives away "Gehen". 
# We'll use it for real when we train a model on the spectrograms.
def crop_middle(s, keep= 149):
    width = s.shape[1]
    start = (width-keep)//2
    stop = start + keep
    return s[:, start:stop]

for nr in ["0000", "0061"]:
    s = np.load(f"Radar-Startpaket/spektrogramme/{nr}.npz")["spek"]
    print(nr, s.shape, "->", crop_middle(s).shape)

