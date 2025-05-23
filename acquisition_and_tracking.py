import numpy as np
import sys
from scipy.signal import resample

from ca_codes import codeG1, CAcodes
from plot import plot_tracking_results, plot_correlation_surface

def print_acquisition_results(prn_id, doppler_offset, code_phase_offset):
    print(f"\n----------------- Acquisition results -----------------")
    print("  1) Detected satellite PRN ID:", prn_id)
    print("  2) Doppler offset:", np.abs(doppler_offset))
    print("  3) Code-phase offset:", code_phase_offset)

def acquisition(data, fs, plot=False):
    detection_factor = 2.5
    chip_rate = 1.023e6
    num_chips = 1023
    freq_range = 10e3
    freq_resolution = 200

    # Calculating length of shortest sequence including 1023 chips
    num_samples = int((num_chips / chip_rate) * fs)
    signal = data[:num_samples][:, np.newaxis]

    # Calculating phase values at various frequency offsets
    freq_offset = np.arange(0, freq_range + 1, freq_resolution)
    code_phase_offset = ((2 * np.pi / fs) * np.arange(num_samples))
    phases = np.outer(code_phase_offset, freq_offset)

    removed_carrier_signal = np.exp(-1j * phases) * signal
    removed_carrier_signal_spectrum = np.fft.fft(removed_carrier_signal, axis=0)

    # Calculating acquisition detection threshold
    g1 = 1 - 2 * codeG1()
    upsampled_g1 = resample(g1, num_samples)
    upsampled_g1_spectrum = np.fft.fft(upsampled_g1)[:, np.newaxis]

    noise = np.abs(np.fft.ifft(removed_carrier_signal_spectrum * np.conj(upsampled_g1_spectrum),axis=0))
    detection_threshold = np.max(noise) * np.sqrt(detection_factor)

    # Acquisition algorithm
    for i in range(32):
        cacode = 1 - 2 * CAcodes(i + 1)
        upsampled_cacode = resample(cacode, num_samples)
        upsampled_cacode_spectrum = np.fft.fft(upsampled_cacode)[:, np.newaxis]

        time_corrval = np.abs(np.fft.ifft(
            removed_carrier_signal_spectrum * np.conj(upsampled_cacode_spectrum), axis=0))

        if np.max(time_corrval) > detection_threshold:
            code_phase_offset = np.argmax(np.max(time_corrval, axis=1))
            doppler_offset = freq_offset[np.argmax(np.max(time_corrval, axis=0))]

            print_acquisition_results(i+1, doppler_offset, code_phase_offset)
            if plot: plot_correlation_surface(i, time_corrval, freq_offset, num_samples)

            return i+1, doppler_offset, code_phase_offset

    print("No satellites detected")
    sys.exit()

def calc_loop_coeff(noise_bandwidth, damping_ratio, gain):
    wn = noise_bandwidth * 8 * damping_ratio / (4 * damping_ratio**2 + 1)
    tau1 = gain / (wn**2)
    tau2 = (2 * damping_ratio) / wn
    coeff1 = tau2 / tau1
    coeff2 = 1 / tau1

    return coeff1, coeff2

def tracking(data,process_time,fs,prn_id,doppler_offset,code_phase_offset,plot=False):
    base_chip_rate = 1.023e6
    num_chips = 1023
    early_late_spacing = 0.5
    cacode = CAcodes(prn_id)

    dll_noise_bandwidth = 2.0
    dll_damping_ratio = 0.7
    dll_gain = 1.0
    pll_noise_bandwidth = 12.0
    pll_damping_ratio = 0.2
    pll_gain = 1.0

    dll_coeff1, dll_coeff2 = calc_loop_coeff(
                                dll_noise_bandwidth,
                                dll_damping_ratio,
                                dll_gain
                            )
    pll_coeff1, pll_coeff2 = calc_loop_coeff(
                                pll_noise_bandwidth,
                                pll_damping_ratio,
                                pll_gain
                            )

    I_P = np.zeros(process_time)
    Q_P = np.zeros(process_time)
    dll_discriminator = np.zeros(process_time)
    pll_discriminator = np.zeros(process_time)
    dll_nco = np.zeros(process_time)
    pll_nco = np.zeros(process_time)
    chip_rate = np.zeros(process_time)
    chip_rate[0] = base_chip_rate
    carrier_freq = np.zeros(process_time)
    carrier_freq[0] = doppler_offset
    data = data[code_phase_offset:]
    rem_code_offset = 0.0
    rem_phase = 0.0
    data_index = 0

    for i in range(1,process_time):
        code_step = chip_rate[i-1] / fs
        num_samples = int(np.ceil((num_chips - rem_code_offset) / code_step))

        signal = data[data_index:data_index + num_samples]
        data_index += num_samples
        
        code_offset = (np.arange(num_samples) * code_step) + rem_code_offset
        code_offset = np.mod(code_offset, num_chips)
        prompt_code = cacode[np.floor(code_offset).astype(int)]
        
        code_offset_early = np.mod(code_offset - early_late_spacing, num_chips)
        early_code = cacode[np.floor(code_offset_early).astype(int)]

        code_offset_late = np.mod(code_offset + early_late_spacing, num_chips)
        late_code = cacode[np.floor(code_offset_late).astype(int)]

        rem_code_offset = np.mod(code_offset[-1] + code_step, num_chips)

        time = np.arange(num_samples) / fs
        phase = (carrier_freq[i-1] * 2.0 * np.pi * time) + rem_phase
        rem_phase = phase[-1] + (carrier_freq[i-1] * 2.0 * np.pi / fs)
        rem_phase = np.mod(rem_phase, 2 * np.pi)

        I_sig = np.cos(phase) * signal
        Q_sig = -np.sin(phase) * signal

        I_E = np.sum(early_code * I_sig)
        Q_E = np.sum(early_code * Q_sig)
        I_P[i] = np.sum(prompt_code * I_sig)
        Q_P[i] = np.sum(prompt_code * Q_sig)
        I_L = np.sum(late_code * I_sig)
        Q_L = np.sum(late_code * Q_sig)

        pll_discriminator[i] = np.arctan(Q_P[i] / I_P[i])

        pll_nco[i] = pll_nco[i-1] + pll_coeff1 * pll_discriminator[i] \
            + pll_coeff2 * (pll_discriminator[i] - pll_discriminator[i-1])
        carrier_freq[i] = doppler_offset + pll_nco[i] / (2 * np.pi)

        E = np.sqrt(I_E**2 + Q_E**2)
        L = np.sqrt(I_L**2 + Q_L**2)
        dll_discriminator[i] = (E - L) / (E + L + 1e-6)

        dll_nco[i] = dll_nco[i-1] + dll_coeff1 * dll_discriminator[i] \
            + dll_coeff2 * (dll_discriminator[i] - dll_discriminator[i-1])
        chip_rate[i] = base_chip_rate - dll_nco[i]

    if plot: plot_tracking_results(carrier_freq, dll_nco)

    return I_P, Q_P
