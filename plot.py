import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, fftshift

def plot_spectrum(data, fs):
    
    N = int(fs)
    signal = data[:N]

    f = np.linspace(-fs/2, fs/2, N)
    fft_signal = fftshift(fft(signal)/N)

    plt.figure(figsize=(10, 6))
    plt.plot(f/1e6, 20 * np.log10(np.abs(fft_signal)))  # dB/MHz
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Spectrum of the received GPS signal')
    plt.grid(True)
    plt.show()

def plot_correlation_surface(i, time_corrval, freq_idx, num_samples):

    positive_freq_idx = freq_idx[freq_idx >= 0]
    positive_time_corrval = time_corrval[:, freq_idx >= 0]
    X, Y = np.meshgrid(positive_freq_idx, np.arange(num_samples))

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, positive_time_corrval, cmap='viridis', rstride=1, cstride=1, antialiased=False)
    ax.set_title('Correlation Surface (PRN {})'.format(i + 1))
    ax.set_xlabel('Doppler Shift [Hz]')
    ax.set_ylabel('Code Phase Offset [samples]')
    ax.set_zlabel('Correlation value')
    plt.show()

def plot_tracking_results(carrier_freq, dll_nco):

    plt.figure(figsize=(10, 4))
    plt.plot(carrier_freq[:20000])
    plt.ylabel('Frequency [Hz]',fontsize=14)
    plt.xlabel('Time [milliseconds]',fontsize=14)
    plt.title('Carrier frequency tracking',fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 4))
    plt.plot(dll_nco[:20000])
    plt.ylabel('Offset [chips]',fontsize=14)
    plt.xlabel('Time [milliseconds]',fontsize=14)
    plt.title('DLL NCO',fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.show()

def plot_constellation_diagram(I, Q, sample_delay):
    
    plt.figure(figsize=(6, 6))
    plt.plot(I[sample_delay:], Q[sample_delay:], '.')
    plt.title('Constellation Diagram')
    plt.xlabel('I Prompt')
    plt.ylabel('Q Prompt')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def plot_BPSK_symbols(I, start, end):

    plt.figure(figsize=(10, 4))
    plt.plot(np.arange(start, end), I[start:end])
    plt.ylabel('BPSK value', fontsize=14)
    plt.xlabel('Time [milliseconds]', fontsize=14)
    plt.title('BPSK symbols', fontsize=14)
    plt.xticks([start, end-1], fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.show()
