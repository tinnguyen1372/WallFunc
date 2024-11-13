import numpy as np

# Load the .npz file
data = np.load('SL_ObjWall_0_2000.npz', allow_pickle=True)
# Access the stored parameters
# Access the stored parameters
all_params = data['params']

# Initialize a list to store the tuples
output_array = []

# Slice the array from start_index to end_index
sliced_params = all_params[0:20]

# Iterate through each dictionary in the sliced array and duplicate tuples
for param in sliced_params:
    # Create a tuple of (wall_thickness, wall_permittivity) and duplicate it
    wall_tuple = (param['wall_thickness'], round(param['permittivity_wall'],2))
    output_array.extend([wall_tuple] * 10)

# Convert the list of tuples to a NumPy array
output_array = np.array(output_array)

# Print the shape of the loaded parameters
print(output_array)
