import numpy as np

from plot import plot_BPSK_symbols, plot_constellation_diagram

def convert_samples_to_bpsk_symbols(I, plot):

    if plot: plot_BPSK_symbols(I, 0, 1000)

    bpsk_symbols = []
    for sample_index in range(len(I)):
        bit_value = np.sign(I[sample_index])
        bpsk_symbols.append(1 if bit_value > 0 else -1)

    return bpsk_symbols

def find_pll_induced_offset(bpsk_symbols):

    pll_offset = 0

    for i in range(len(bpsk_symbols) - 60):
        sum1 = np.sum(bpsk_symbols[i:i+20])
        sum2 = np.sum(bpsk_symbols[i+20:i+40])
        sum3 = np.sum(bpsk_symbols[i+40:i+60])

        if sum1 in [-20,20] and sum2 in [-20,20] and sum3 in [-20,20]:
            if sum1 + sum2 + sum3 in [-20,20]:
                pll_offset = i+60
                break

    return pll_offset

def get_bitstream(bpsk_symbols):

    bit_duration = 20
    bitstream = []
    for sample_index in range(0, len(bpsk_symbols) - bit_duration, bit_duration):
        sum = np.sum(bpsk_symbols[sample_index:sample_index + bit_duration])
        bitstream.append(1 if sum > 0 else 0)

    return ''.join(map(str, bitstream))

def digital_demodulation(I, Q, plot=False):

    I_normalized = I / np.sqrt(np.mean(I**2))
    Q_normalized = Q / np.max(Q)

    bpsk_symbols = convert_samples_to_bpsk_symbols(I_normalized, plot)
    pll_offset = find_pll_induced_offset(bpsk_symbols)
    bpsk_symbols = bpsk_symbols[pll_offset:]
    bitstream = get_bitstream(bpsk_symbols)

    if plot: plot_constellation_diagram(I_normalized, Q_normalized, pll_offset)

    return bitstream
