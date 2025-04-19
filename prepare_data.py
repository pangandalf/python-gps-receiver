import numpy as np

file_path = '2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN/2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat'
output_file_path = 'data.dat'

complex_data = np.fromfile(file_path, dtype=np.int16)
print("Omiting the imaginary part of the signal")
data = complex_data[0::2]
print(f"Saving the real part of the signal to {output_file_path}")
data.tofile(output_file_path)
print("Done!")
