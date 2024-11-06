import numpy as np
import matplotlib.pyplot as plt
import argparse
import random
from matplotlib.colors import ListedColormap

def create_geometry(square_size, air_size, rect_width, rect_height, wall_thickness):
    objwall_gap = 10  # gap between object and wall
    
    # Initialize the square room with walls
    geometry = np.zeros((square_size, square_size), dtype=int)
    
    # Set the air region
    air_start = (square_size - air_size) // 2
    air_end = air_start + air_size
    geometry[air_start + wall_thickness:air_end, air_start:air_end] = 1  # Air is represented by 1
    # geometry[air_start:air_end, air_start:air_end - wall_thickness] = 1  # Air is represented by 1
    
    # Generate random position for the rectangle within the air region
    rect_x = random.randint(air_start + objwall_gap + wall_thickness, air_end - rect_width - objwall_gap -wall_thickness)
    rect_y = random.randint(air_start + objwall_gap + wall_thickness, air_end - rect_height - objwall_gap - wall_thickness)
    
    # Place the rectangle in the geometry
    
    return geometry, rect_x, rect_y

def visualize_geometry(geometry, wall_color, air_color, object_color):
    # Define a custom colormap
    cmap = ListedColormap([
                        wall_color, 
                        air_color, 
                        object_color
                           ])
    
    # Set the figure size
    plt.figure(figsize=(10, 10))
    
    plt.imshow(geometry, cmap=cmap, origin='lower')
    # plt.axis('off')
    # plt.axis([-200, 200, -200, 200])
    plt.title('Geometry with Square Walls, Air Space, and Rectangle Object')
    plt.show()

def save_image(filename, geometry, square_size, wall_color, air_color, object_color):
    # Define a custom colormap
    cmap = ListedColormap([
                        wall_color, 
                        air_color, 
                        object_color
                           ])    
    # Set the figure size
    plt.figure(figsize=(10, 10))
    plt.imshow(geometry, cmap=cmap, origin='lower')
    plt.xlabel('x(t)')
    plt.ylabel('y(t)')
    plt.axis('off')    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig('./Geometry/' + filename, format='png', dpi=square_size/10, bbox_inches='tight', pad_inches=0)
    plt.close()

def save_base(filename, geometry, square_size, wall_color, air_color, object_color):
    # Define a custom colormap
    cmap = ListedColormap([
                        wall_color, 
                        air_color, 
                        # object_color
                           ])    
    # Set the figure size
    plt.figure(figsize=(10, 10))
    plt.imshow(geometry, cmap=cmap, origin='lower')
    plt.xlabel('x(t)')
    plt.ylabel('y(t)')
    plt.axis('off')    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig('./Geometry/' + filename, format='png', dpi=square_size/10, bbox_inches='tight', pad_inches=0)
    plt.close()

def save_parameters(filename, **params):
    # If the file exists, load the current parameters and append the new ones
    if os.path.exists(filename):
        existing_data = np.load(filename, allow_pickle=True)
        # Convert existing data to a list of dictionaries
        all_params = list(existing_data['params'])
    else:
        all_params = []

    # Append the new parameters
    all_params.append(params)

    # Save the updated parameters back to the file
    with open(filename, 'wb') as f:
        np.savez(f, params=all_params)

if __name__ == '__main__':
    # Predefined colors
    wall_color = [1, 1, 0]   # wall color
    air_color = [1, 1, 1]  # air color
    object_color = [1, 0.4, 0]  # object color

    import random
    import os

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate and visualize a geometry with square walls, air space, and a rectangle object.')
    parser.add_argument('--start', type=int, default=0, help='Number of the generated geometry')
    parser.add_argument('--end', type=int, default=10, help='Number of the generated geometry')
    # Use the generated random values
    args = parser.parse_args()
    if (args.start or args.end) is None:
        args.n = 10
    else:
        args.n = args.end + 1 - args.start
    for i in range(args.n):
        # Randomly generate values for the parameters within reasonable ranges
        square_size = random.randint(200, 350)  # Adjust range as needed
        wall_thickness = random.randint(10, 50)
        rect_width = random.randint(10, 60)
        rect_height = random.randint(10, 60)

        # Generate random floating-point values for permittivity
        permittivity_wall = random.uniform(1.5, 10.0)
        permittivity_object = random.uniform(1.5, 10.0)

        # Create the folder if it doesn't exist
        if not os.path.exists('./Geometry'):
            os.makedirs('./Geometry')
        if not os.path.exists('./Geometry/Base') and not os.path.exists('./Geometry/Object'): 
            os.makedirs('./Geometry/Base')
            os.makedirs('./Geometry/Object')
        filename = './Object/geometry{}.png'.format(args.start+i)
        base = './Base/base{}.png'.format(args.start+i)

        params_filename = 'SL_ObjWall_{}_{}.npz'.format(args.start, args.end)


        args.square_size = square_size
        args.wall_thickness = wall_thickness
        args.rect_width = rect_width
        args.rect_height = rect_height
        args.filename = filename
        args.base = base
        args.params_filename = params_filename

        # Create the geometry
        air_size = args.square_size
        geometry, rect_x, rect_y = create_geometry(args.square_size, air_size, args.rect_width, args.rect_height, args.wall_thickness)

        # Save the image

        save_base(args.base, geometry, args.square_size, wall_color, air_color, object_color)
        geometry[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width] = 2  # Rectangle is represented by 2
        save_image(args.filename, geometry, args.square_size, wall_color, air_color, object_color)

        # Save the parameters
        save_parameters(args.params_filename, square_size=args.square_size, wall_thickness=args.wall_thickness, 
                        rect_width=args.rect_width, rect_height=args.rect_height, 
                        rect_x=rect_x, rect_y=rect_y, wall_color=wall_color, air_color=air_color, object_color=object_color,
                        permittivity_wall = permittivity_wall,
                        permittivity_object = permittivity_object)

        # Visualize the geometry
        # visualize_geometry(geometry, wall_color, air_color, object_color)