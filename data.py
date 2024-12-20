import numpy as np

# Load the .npz file
import matplotlib.pyplot as plt
data = np.load('SL_ObjWall_0_699.npz', allow_pickle=True)
permittivity = []
# Print all the keys (parameters) in the file
for i in range(40,50):
    permittivity.append(data['params'][i]['wall_material'])
print(permittivity)
# Filter out None values
# Extract x and y coordinates
# x_coords, y_coords = zip(*filtered_points)
# Plot the points on a 300x300 dimension plot with equal aspect ratio
# Adjust the plot so coordinates span from (0, 0) to (300, 300) directly
# plt.figure(figsize=(6, 6))  # Square figure
# plt.scatter(x_coords, y_coords, marker='o', label='Sample Points')
# plt.title('Scatter Plot with Coordinates from (0, 0) to (300, 300)')
# plt.xlabel('X Coordinate')
# plt.ylabel('Y Coordinate')
# plt.xlim(0, 300)  # X-axis from 0 to 300
# plt.ylim(300, 0)  # Y-axis from 0 to 300
# plt.gca().set_aspect('equal', adjustable='box')  # Equal aspect ratio
# plt.legend()
# plt.grid(True)
# plt.show()

