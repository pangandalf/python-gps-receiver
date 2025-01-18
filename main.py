import numpy as np
import sys

from plot import plot_spectrum
from acquisition_and_tracking import acquisition, tracking
from digital_demodulation import digital_demodulation
from decoding import decode

file_path = 'real_sig.dat'
data = np.fromfile(file_path, dtype=np.int16)

fs = 4e6
plot = False

plot_spectrum(data, fs, plot)

prn_id, doppler_offset, code_phase_offset = acquisition(data, fs, plot)
if prn_id == 0:
    sys.exit()

I, Q = tracking(data, 100000, fs, prn_id, doppler_offset, code_phase_offset, plot)

bitstream = digital_demodulation(I, Q, plot)

decode(bitstream)
