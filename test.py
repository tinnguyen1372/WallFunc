import numpy as np

# Load the .npz file
data = np.load('SL_ObjWall_0_2000.npz', allow_pickle=True)
print(data)
# Access the stored parameters
all_params = data['params']

# Print the shape of the loaded parameters
print("Shape of the parameters array:", all_params[0])
