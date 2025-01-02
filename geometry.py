import numpy as np
import matplotlib.pyplot as plt
import argparse
import random
from matplotlib.colors import ListedColormap
from scipy.interpolate import CubicSpline
def create_geometry(square_size, air_size, rect_width, rect_height, wall_thickness):
    objwall_gap = 15 # gap between object and wall
    
    # Initialize the square room with walls
    geometry = np.zeros((square_size, square_size), dtype=int)
    
    # Set the air region
    air_start = (square_size - air_size) // 2
    air_end = air_start + air_size
    geometry[air_start + wall_thickness:air_end, air_start:air_end] = 1  # Air is represented by 1
    # geometry[air_start:air_end, air_start:air_end - wall_thickness] = 1  # Air is represented by 1
    
    # Generate random position for the rectangle within the air region with padding
    # rect_y = air_start + (air_size - rect_height) // 2
    # rect_x = air_start + (air_size - rect_width) // 2
    rect_y = random.randint(air_start + wall_thickness + objwall_gap, air_end - rect_height - square_size//4)
    rect_x = random.randint(air_start + int(6*square_size/22), air_end - rect_width - int(6*square_size/22))
    # rect_y = random.randint(air_start + objwall_gap + wall_thickness + square_size//2, air_end - rect_height - objwall_gap - wall_thickness)
    # rect_x = (random.randint(air_start + 30, air_end - rect_width -30))
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
    object_color = [1, 0, 0]  # object color
    x_center, y_center = None, None
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
        square_size = 250  # Adjust range as needed
        wall_thickness = random.randint(15, 30)

        
        # Generate random floating-point values for permittivity
        # Base permittivity values for wall materials
        wall_materials = {
            "Concrete": 5.24,
            "Brick": 3.91,
            "Plasterboard": 2.73,
            "Wood": 1.99,
            "Glass": 6.31,
        }
        variance_factor = 0.1  # Adjust this to 0.2 for higher variability

        wall_material = random.choice(list(wall_materials.keys()))
        base_permittivity = wall_materials[wall_material]
        variance = base_permittivity * variance_factor
        permittivity_wall = round(random.uniform(base_permittivity -variance, base_permittivity +variance), 2)    

        permittivity_object = random.uniform(4, 40.0)

        # Create the folder if it doesn't exist
        if not os.path.exists('./Geometry'):
            os.makedirs('./Geometry')
        if not os.path.exists('./Geometry/Base') and not os.path.exists('./Geometry/Object'): 
            os.makedirs('./Geometry/Base')
            os.makedirs('./Geometry/Object')
        filename = './Object/geometry{}.png'.format(args.start+i)
        base = './Base/base{}.png'.format(args.start+i)

        params_filename = 'SL_Obj4Wall_{}_{}.npz'.format(args.start, args.end)


        args.square_size = square_size
        args.wall_thickness = wall_thickness
        rect_width = random.randint(30, 50)
        rect_height = random.randint(30, 50)
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

        # Define the shape
        shape = random.choice(['rectangle', 'triangle', 'circle'])

        # Function to create the shape and extract edges
        def create_shape_and_edges(shape):
            edges = []
            if shape == 'rectangle':
                # Define rectangle edges
                top_edge = [(x, rect_y) for x in range(rect_x, rect_x + rect_width)]
                bottom_edge = [(x, rect_y + rect_height) for x in range(rect_x, rect_x + rect_width)]
                left_edge = [(rect_x, y) for y in range(rect_y, rect_y + rect_height)]
                right_edge = [(rect_x + rect_width, y) for y in range(rect_y, rect_y + rect_height)]
                x_center = rect_x + rect_width // 2
                y_center = rect_y + rect_height // 2
                edges = top_edge + bottom_edge + left_edge + right_edge

                # Fill rectangle in the geometry
                geometry[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width] = 2

            elif shape == 'triangle':
                x_center = rect_x + rect_width // 2
                y_center = rect_y + rect_height // 2
                # Define triangle edges (right triangle for simplicity)
                for y in range(rect_height):
                    for x in range(rect_width - y):
                        if x == 0 or y == 0 or x == rect_width - y - 1:
                            edges.append((rect_x + x, rect_y + y))
                # Fill triangle in the geometry
                for y in range(rect_height):
                    for x in range(rect_width - y):
                        geometry[rect_y + y, rect_x + x] = 2

            elif shape == 'circle':
                # Define circle edge
                radius = min(rect_width, rect_height) // 2
                x_center, y_center = rect_x + radius, rect_y + radius
                for angle in np.linspace(0, 2 * np.pi, 100):
                    x = int(x_center + radius * np.cos(angle))
                    y = int(y_center + radius * np.sin(angle))
                    edges.append((x, y))
                # Fill circle in the geometry
                for y in range(-radius, radius):
                    for x in range(-radius, radius):
                        if x**2 + y**2 <= radius**2:
                            geometry[y_center + y, x_center + x] = 2

            # Ensure the edges form a closed loop for periodic spline
            edges.append(edges[0])
            center_and_points = [(x_center, y_center)] + list(edges)
            return edges, center_and_points

        # Create shape and get edges
        edges , center_and_points = create_shape_and_edges(shape)
        save_image(args.filename, geometry, args.square_size, wall_color, air_color, object_color)

        # Extract x and y points
        x_points, y_points = zip(*edges)

        # Cubic spline interpolation
        t = np.linspace(0, 1, len(x_points))  # Parametric variable
        cs_x = CubicSpline(t, x_points, bc_type='periodic')
        cs_y = CubicSpline(t, y_points, bc_type='periodic')

        # Fine-grained t for smooth interpolation
        t_fine = np.linspace(0, 1, 1000)
        x_fine = cs_x(t_fine)
        y_fine = cs_y(t_fine)

        # Create the array: first element is the center, followed by the edge points

        # # Plot the result
        # plt.figure(figsize=(8, 8))
        # plt.plot(x_points, y_points, 'o', label="Sample Points")
        # # plt.plot(x_fine, y_fine, '-', label="Cubic Spline Interpolation")
        # plt.axis('equal')
        # plt.legend()
        # plt.title(f"Cubic Spline Interpolation for {shape.capitalize()}")
        # # plt.show()
        # Save the parameters
        save_parameters(
            args.params_filename,     
            shape=shape,
            square_size=square_size,
            wall_thickness=wall_thickness,
            rect_width=rect_width,
            rect_height=rect_height,
            rect_x=rect_x,
            rect_y=rect_y,
            wall_color=wall_color,
            air_color=air_color,
            object_color=object_color,
            permittivity_wall=permittivity_wall,
            wall_material=wall_material,  # Fixed spacing
            permittivity_object=permittivity_object,
            # center_and_points=center_and_points,
            cse_x_fine=list(x_fine),  # Ensure proper conversion to list
            cse_y_fine=list(y_fine),  # Ensure proper conversion to list
        )


        # Visualize the geometry
        # visualize_geometry(geometry, wall_color, air_color, object_color)