import numpy as np
from numpy.fft import fft, fftshift
from plot import plot_spectrum

# Load data from file (samples should include only the real part of the signal)
file_path = 'real_sig.dat'
data = np.fromfile(file_path, dtype=np.int16)

sig = data[:int(4e6)]               # 1 second of the signal

N = len(sig)
fs = 4e6 
f = np.linspace(-fs/2, fs/2, N)     # frequency axis vector (Hz)
fft_signal = fftshift(fft(sig)/N)   # FFT of the signal with center of the spectrum at 0 Hz

plot_spectrum(f, fft_signal)