import numpy as np

def demodulate(I_P_normalized):

    bit_data = []
    for sample_index in range(len(I_P_normalized)):
        bit_value = np.sign(I_P_normalized[sample_index])
        bit_data.append(1 if bit_value > 0 else -1)
    
    return bit_data

def remove_offset_introduced_by_loop(bit_data):

    expected_sum = np.sum(bit_data[0:20])
    loop_samples_offset = 0
    for i in range(len(bit_data) - 20):

        if expected_sum in [-20,20] and np.sum(bit_data[i+20:i+40]) in [-20,20] and np.sum(bit_data[i+40:i+60]) in [-20,20]:
            loop_samples_offset = i+100
            break

        expected_sum = expected_sum - bit_data[i] + bit_data[i + 20]

    return loop_samples_offset

def bit_synchronization(bit_data):

    bit_duration = 20  # in miliseconds
    bit_stream = []
    for sample_index in range(0, len(bit_data) - bit_duration, bit_duration):
        I_sum = np.sum(bit_data[sample_index:sample_index + bit_duration])
        bit_stream.append(1 if I_sum > 0 else 0)

    return ''.join(map(str, bit_stream))
