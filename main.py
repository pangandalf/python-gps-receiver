import numpy as np
import sys

from plot import plot_spectrum, plot_constellation_diagram
from acquisition_and_tracking import acquisition, tracking
from demodulation_and_bit_synch import demodulate, remove_offset_introduced_by_loop, bit_synchronization
from decoding import decode

file_path = 'real_sig.dat'
data = np.fromfile(file_path, dtype=np.int16)

fc = 0
fs = 4e6
plot = True

if plot: plot_spectrum(data,fs)

prn_id, doppler_offset, code_phase_offset = acquisition(data,fc,fs,plot)
if prn_id == 0: sys.exit()

I_P, Q_P = tracking(data,100000,fs,prn_id,doppler_offset,code_phase_offset,plot)
I_P_normalized = I_P / np.sqrt(np.mean(I_P**2))

bit_data = demodulate(I_P_normalized)
loop_samples_offset = remove_offset_introduced_by_loop(bit_data)
bit_data = bit_data[loop_samples_offset:]

if plot: plot_constellation_diagram(I_P_normalized, Q_P, loop_samples_offset)

bit_string = bit_synchronization(bit_data)
decode(bit_string)
