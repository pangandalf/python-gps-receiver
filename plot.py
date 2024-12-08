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

def plot_tracking_results(pll_discriminator, pll_nco, carrier_freq, dll_discriminator, dll_nco, code_freq):

    plt.figure(figsize=(10, 15))

    plt.subplot(6, 1, 1)
    plt.plot(pll_discriminator)
    plt.ylabel('PLL Discriminator')

    plt.subplot(6, 1, 2)
    plt.plot(pll_nco)
    plt.ylabel('PLL NCO')

    plt.subplot(6, 1, 3)
    plt.plot(carrier_freq)
    plt.ylabel('Carrier Frequency')

    plt.subplot(6, 1, 4)
    plt.plot(dll_discriminator)
    plt.ylabel('DLL Discriminator')

    plt.subplot(6, 1, 5)
    plt.plot(dll_nco)
    plt.ylabel('DLL NCO')

    plt.subplot(6, 1, 6)
    plt.plot(code_freq)
    plt.ylabel('Code Frequency')

    plt.xlabel('Time (samples)')
    plt.tight_layout()
    plt.show()

def plot_constellation_diagram(I_P_normalized, Q_P, sample_delay):

    Q_P_normalized = Q_P / np.max(Q_P)
    
    plt.figure(figsize=(6, 6))
    plt.plot(I_P_normalized[sample_delay:], Q_P_normalized[sample_delay:], '.')
    plt.title('Constellation Diagram')
    plt.xlabel('I Prompt')
    plt.ylabel('Q Prompt')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
