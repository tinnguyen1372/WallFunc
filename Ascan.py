import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, ifft, fftfreq, fftshift
data = np.loadtxt('extracted_data.txt')
velocity = 3e8
timwin = 50e-9
samples =data.shape[0]
dt = timwin/samples
pixdistance = (2.5 / 1e9) / dt
Ascan_peaks = []

samples =data.shape[0]
dt = timwin/samples

def print_peak_distances(peaks):
    distances = np.diff(peaks)
    for i, distance in enumerate(distances):
        print(f"Distance between peak {i} and peak {i+1}: {distance}")
# print(pixdistance)
# Load and preprocess data
for i in range(20):
    b_scan = data[:, i]
# dt = b_scan[1] - b_scan[0]
# Initial peak detection to analyze reflection characteristics
    peaks, _ = find_peaks(b_scan, height=1,distance=int(pixdistance))
    print(peaks[1],peaks[2])
plt.figure()
# print_peak_distances(peaks)
plt.plot(b_scan)
for i, peak in enumerate(peaks):
    plt.text(peak, b_scan[peak], str(i), fontsize=8, ha='center')
plt.title('A-Scan with Peaks')
plt.xlabel('Index')
plt.ylabel('Amplitude')
plt.show()
print()

# Define migration functions
# def stolt_migration(b_scan, velocity):
#     # FFT of the input data
#     data_fft = fft(b_scan,norm='forward')
#     freqs = fftfreq(len(b_scan), d=dt)  # Sampling interval

#     return data_fft

# def fk_migration(b_scan, velocity):
#     # Frequency-Wavenumber (F-K) migration using FFT
#     b_scan_fft = fft(b_scan)
#     kx = np.fft.fftfreq(len(b_scan),d=dt)
#     kz = np.sqrt((2 * np.pi * fftshift(fftfreq(len(b_scan))) / velocity) ** 2 - kx ** 2)
#     kz[np.isnan(kz)] = 0

#     # Frequency-wavenumber domain manipulation and inverse FFT
#     migrated = np.abs(ifft(b_scan_fft * np.exp(1j * kz)))
#     return migrated


# # Initial velocity assumption (m/s)
# velocity = 3e8

# # Apply Stolt Migration
# migrated_stolt = stolt_migration(b_scan, velocity)
# peaks, _ = find_peaks(migrated_stolt, height=1, distance=200)

# plt.figure()
# plt.plot(migrated_stolt)
# for i, peak in enumerate(peaks):
#     plt.text(peak, migrated_stolt[peak], str(i), fontsize=8, ha='center')
# # print_peak_distances(peaks)
# plt.title('Stolt Migrated A-Scan')
# plt.xlabel('Index')
# plt.ylabel('Amplitude')
# plt.show()
# print()

# # Apply Frequency-Wavenumber Migration
# migrated_fk = fk_migration(b_scan, velocity)
# peaks, _ = find_peaks(migrated_fk, height=1, distance=200)
# print(_['peak_heights'][1])

# plt.figure()
# plt.plot(migrated_fk)
# for i, peak in enumerate(peaks):
#     plt.text(peak, migrated_fk[peak], str(i), fontsize=8, ha='center')
# # print_peak_distances(peaks)
# plt.title('F-K Migrated A-Scan')
# plt.xlabel('Index')
# plt.ylabel('Amplitude')
# plt.show()
