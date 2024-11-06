import h5py
import numpy as np

def extract_data(file_name):
    with h5py.File(file_name, 'r') as f:
        # Assuming the data you want to extract is in the 'rxs/rx1/Ey' dataset
        data = f['rxs']['rx1']['Ez'][()]
    return data

file_name = 'Base0.out'
data = extract_data(file_name)
output_file = 'extracted_data.txt'
np.savetxt(output_file, data)
print(data.shape)  # Output: (100, 100, 100)