import numpy as np
import sys

from plot import plot_spectrum, plot_constellation_diagram
from acquisition_and_tracking import acquisition, tracking
from demodulation_and_bit_synch import demodulate, remove_offset_introduced_by_loop, bit_synchronization
from decoding import decode

file_path = 'real_sig.dat'
data = np.fromfile(file_path, dtype=np.int16)

fs = 4e6
plot = True

if plot: plot_spectrum(data,fs)

prn_id, doppler_offset, code_phase_offset = acquisition(data,fs,plot)
if prn_id == 0:
    print("Acquisition failed. No signal from any satellite detected.")
    sys.exit()

I, Q = tracking(data,100000,fs,prn_id,doppler_offset,code_phase_offset,plot)
I_normalized = I / np.sqrt(np.mean(I**2))
Q_normalized = Q / np.max(Q)

bit_data = demodulate(I_normalized)
loop_samples_offset = remove_offset_introduced_by_loop(bit_data)
bit_data = bit_data[loop_samples_offset:]

if plot: plot_constellation_diagram(I_normalized, Q_normalized, loop_samples_offset)

bit_string = bit_synchronization(bit_data)
decode(bit_string)
