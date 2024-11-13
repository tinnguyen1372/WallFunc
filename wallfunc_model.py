import h5py
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, ifft, fftfreq, fftshift

def extract_data(file_name):
    with h5py.File(file_name, 'r') as f:
        # Assuming the data you want to extract is in the 'rxs/rx1/Ey' dataset
        data = f['rxs']['rx1']['Ez'][()]
    return data


file_name = 'Base10.out'
data = extract_data(file_name)
velocity = 3e8
timwin = 50e-9
samples =data.shape[0]
waveform = 1e9
dt = timwin/samples
pixdistance = (2.5 / waveform) / dt


def print_peak_distances(peaks):
    if len(peaks) > 1:
        distance = peaks[1] - peaks[0]
    return distance

# def fk_migration(b_scan, velocity):
#     # Frequency-Wavenumber (F-K) migration using FFT
#     b_scan_fft = fft(b_scan)
#     kx = np.fft.fftfreq(len(b_scan),d=dt)
#     kz = np.sqrt((2 * np.pi * fftshift(fftfreq(len(b_scan))) / velocity) ** 2 - kx ** 2)
#     kz[np.isnan(kz)] = 0

#     # Frequency-wavenumber domain manipulation and inverse FFT
#     migrated = np.abs(ifft(b_scan_fft * np.exp(1j * kz)))
#     return migrated



# Load and preprocess data
for i in range(0, 10):
    b_scan = data[:, i]

# print(pixdistance)


    # Initial peak detection to analyze reflection characteristics
    peaks, _ = find_peaks(b_scan, height=1, distance=int(pixdistance), prominence=0.1)
    plt.figure()
    # print_peak_distances(peaks)
    plt.plot(b_scan)
    for i, peak in enumerate(peaks):
        plt.text(peak, b_scan[peak], str(i), fontsize=8, ha='center')
    plt.title('A-Scan with Peaks')
    plt.xlabel('Index')
    plt.ylabel('Amplitude')
    plt.show()
# print()


    # Apply Frequency-Wavenumber Migration
    migrated_fk = fk_migration(b_scan, velocity)
    peaks, _ = find_peaks(migrated_fk, height=1, distance=int(pixdistance), prominence=0.1)
    plt.figure()
    plt.plot(migrated_fk)
    for i, peak in enumerate(peaks):
        plt.text(peak, migrated_fk[peak], str(i), fontsize=8, ha='center')
    plt.title('F-K Migrated A-Scan')
    plt.xlabel('Index')
    plt.ylabel('Amplitude')
    plt.show()
