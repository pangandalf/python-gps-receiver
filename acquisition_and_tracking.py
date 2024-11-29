import numpy as np
from scipy.signal import resample

from ca_codes import codeG1, CAcodes
from plot import plot_tracking_results, plot_correlation_surface

def acquisition(data, fs, plot=False):

    detection_factor = 2.5
    chip_rate = 1.023e6
    num_chips = 1023
    freq_range = 10e3
    freq_resolution = 200

    # Calculating length of shortest sequence including 1023 chips
    num_samples = int((num_chips / chip_rate) * fs)
    sig = data[:num_samples][:, np.newaxis]

    freq_idx = np.arange(-freq_range, freq_range + 1, freq_resolution)
    phase_idx = ((-2 * np.pi / fs) * np.arange(num_samples))
    phases = np.outer(phase_idx, freq_idx)

    # Calculating phase values at various frequency offsets
    removed_carrier_sig = np.exp(-1j * phases) * sig
    removed_carrier_sig_spectrum = np.fft.fft(removed_carrier_sig, n=num_samples, axis=0)

    # Calculating acquisition detection threshold
    g1 = 1 - 2 * codeG1()
    upsampled_g1 = resample(g1, num_samples)
    upsampled_g1_spectrum = np.fft.fft(upsampled_g1, n=num_samples)[:, np.newaxis]

    noise = np.abs(np.fft.ifft(removed_carrier_sig_spectrum * np.conj(upsampled_g1_spectrum), axis=0))
    detection_threshold = np.max(noise) * np.sqrt(detection_factor)

    for i in range(32):
        
        cacode = 1 - 2 * CAcodes(i + 1)
        upsampled_cacode = resample(cacode, num_samples)
        upsampled_cacode_spectrum = np.fft.fft(upsampled_cacode, n=num_samples)[:, np.newaxis]

        time_corrval = np.abs(np.fft.ifft(removed_carrier_sig_spectrum * np.conj(upsampled_cacode_spectrum), axis=0))
        code_phase_offset = np.argmax(np.max(time_corrval, axis=1))
        doppler_offset = freq_idx[np.argmax(np.max(time_corrval, axis=0))]

        if np.max(time_corrval) > detection_threshold:
            print(f"\n----------------- Acquisition results -----------------")
            print("  1) Detected satellite PRN ID:", i+1)
            print("  2) Doppler offset:", np.abs(doppler_offset))
            print("  3) Code-phase offset:", code_phase_offset)
        
            if plot: plot_correlation_surface(i, time_corrval, freq_idx, num_samples)

            return i+1, np.abs(doppler_offset), code_phase_offset

    print("No satellites detected")
    return 0, None, None

def calc_loop_coef(noise_bw, zeta, gain):
    
    wn = noise_bw * 8 * zeta / (4 * zeta**2 + 1)
    tau1 = gain / (wn**2)
    tau2 = (2 * zeta) / wn
    coeff1 = tau2 / tau1
    coeff2 = 1 / tau1

    return coeff1, coeff2

def tracking(data,process_time,fs,PRN,doppler_offset,code_phase_offset,plot=False):

    chip_rate = 1.023e6
    num_chips = 1023
    dll_noise_bandwidth = 2.0
    dll_zeta = 0.7
    early_late_spacing = 0.5
    pll_noise_bandwidth = 12.0
    pll_zeta = 0.107

    dll_coeff1, dll_coeff2 = calc_loop_coef(dll_noise_bandwidth, dll_zeta, 1.0)
    pll_coeff1, pll_coeff2 = calc_loop_coef(pll_noise_bandwidth, pll_zeta, 1.0)
    cacode = CAcodes(PRN)

    I_P = np.zeros(process_time)
    Q_P = np.zeros(process_time)
    dll_discriminator = np.zeros(process_time)
    pll_discriminator = np.zeros(process_time)
    dll_nco = np.zeros(process_time)
    pll_nco = np.zeros(process_time)
    code_freq = np.zeros(process_time)
    code_freq[0] = chip_rate
    carrier_freq = np.zeros(process_time)
    carrier_freq[0] = doppler_offset
    rem_code_offset = 0.0
    rem_phase = 0.0
    data_index = 0

    for i in range(1,process_time):

        code_step = code_freq[i-1] / fs
        num_samples = int(np.ceil((num_chips - rem_code_offset) / code_step))

        signal = data[code_phase_offset + data_index:code_phase_offset + data_index + num_samples]
        data_index += num_samples
        
        tcode = (np.arange(num_samples) * code_step) + rem_code_offset
        tcode = np.mod(tcode, num_chips)
        rem_code_offset = np.mod(tcode[-1] + code_step, num_chips)
        
        tcode_early = np.mod(tcode - early_late_spacing, num_chips)
        early_code = cacode[np.floor(tcode_early).astype(int)]

        prompt_code = cacode[np.floor(tcode).astype(int)]

        tcode_late = np.mod(tcode + early_late_spacing, num_chips)
        late_code = cacode[np.floor(tcode_late).astype(int)]

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

        pll_discriminator[i] = 0.5 * np.arctan2(2 * I_P[i] * Q_P[i], I_P[i]**2 - Q_P[i]**2)

        pll_nco[i] = pll_nco[i-1] + pll_coeff1 * pll_discriminator[i] + pll_coeff2 * (pll_discriminator[i] - pll_discriminator[i-1])
        carrier_freq[i] = doppler_offset + pll_nco[i] / (2 * np.pi)

        E_mag = np.sqrt(I_E**2 + Q_E**2)
        L_mag = np.sqrt(I_L**2 + Q_L**2)
        dll_discriminator[i] = (E_mag - L_mag) / (E_mag + L_mag + 1e-6)

        dll_nco[i] = dll_nco[i-1] + dll_coeff1 * dll_discriminator[i] + dll_coeff2 * (dll_discriminator[i] - dll_discriminator[i-1])
        code_freq[i] = chip_rate - dll_nco[i]

    if plot:
        plot_tracking_results(pll_discriminator, pll_nco, carrier_freq, dll_discriminator, dll_nco, code_freq)

    return I_P, Q_P
