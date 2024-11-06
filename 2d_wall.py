from gprMax.gprMax import api
from gprMax.receivers import Rx
from tools.outputfiles_merge import merge_files
from tools.plot_Bscan import get_output_data, mpl_plot as mpl_plot_Bscan 
from tools.plot_Ascan import mpl_plot as mpl_plot_Ascan
from gprMax.receivers import Rx
import h5py
import numpy as np
import matplotlib.pyplot as plt
import argparse
import random
import os



class Wall_Func():
    def __init__(self, args) -> None:
        self.args = args
        self.wall = args.wall
        self.wall_thickness = args.wall_thickness
        self.wall_height = args.wall_height
        self.wall_material = args.wall_material
        self.wall_permittivity = args.wall_permittivity
        self.object_permittivity = args.object_permittivity
        self.wall_conductivity = args.wall_conductivity
        self.wall_loss = args.wall_loss

        # Geometry load
        self.geofolder = os.getcwd() + '/Geometry'
        self.geofile = self.geofolder + '/geometry.png'

        # Data load
        self.data = np.load('SL_ObjWall.npz')
        self.pix = int(self.data['square_size']/100/0.002)
        self.num_scan = 50

    def view_geometry(self):
        import numpy.ma as ma
        # Create a 5000x5000 array initialized with -1
        large_array = np.full((2000, 2000), 1, dtype=int)
        # Open the HDF5 file
        with h5py.File('Wall_2D.h5', 'r') as f:
            data = f['data'][:]

        # Print the raw data for reference
        print(data)  # Use data[:] to display the full array
        data = np.squeeze(data, axis=2)
        # Override the values in the large array with the data
        large_array[0:0 + data.shape[0], 0:0 + data.shape[1]] = data

        # Create a masked array where values of -1 are masked (transparent)
        masked_data = ma.masked_where(large_array == -1, large_array)

        # Set the extent to match the pixel dimensions of the data (5000x5000)
        extent = [0, 2000, 0, 2000]

        # Generate the image with origin set to 'lower' to match the (0,0) origin at the bottom-left
        plt.imshow(masked_data, cmap='viridis', origin='lower', extent=extent)

        # # Add a colorbar for reference
        # cbar = plt.colorbar()
        # cbar.set_label('Value')
        plt.axis('equal')

        # Set the plot limits to show the full 5000x5000 region
        plt.xlim(0, 2000)
        plt.ylim(0, 2000)

        # Display the plot with labeled axes
        plt.title("Geometry Visualization")
        # plt.xlabel("X-axis (pixels)")
        # plt.ylabel("Y-axis (pixels)")
        plt.show()

    def preprocess(self):
        from PIL import Image
        import numpy as np
        import h5py

        img = Image.open(self.geofile).convert('RGBA')  # Convert the image to RGBA mode

        # Define the color map with a tolerance
        color_map = {
            (255, 255, 255): -1,  # White (transparent)
            (255, 255, 0): 0,     # Yellow
            (255, 102, 0): 1      # Orange
        }
        tolerance = 5

        def match_color(pixel, color_map, tolerance):
            for color, value in color_map.items():
                if all(abs(pixel[i] - color[i]) <= tolerance for i in range(3)):
                    return value
            return -1  # Default value if no match is found

        arr_2d = np.zeros((self.pix, self.pix), dtype=int)
        img_resized = img.resize((self.pix, self.pix))

        for y in range(self.pix):
            for x in range(self.pix):
                pixel_color = img_resized.getpixel((x, y))
                arr_2d[y, x] = match_color(pixel_color, color_map, tolerance)

        np.savetxt('output_array.txt', arr_2d, fmt='%d', delimiter=' ')
        self.filename = 'geometry_2d.h5'
        arr_3d = np.expand_dims(arr_2d, axis=2)

        with h5py.File('./Geometry/' + self.filename, 'w') as file:
            dset = file.create_dataset("data", data=arr_3d)
            file.attrs['dx_dy_dz'] = (0.002, 0.002, 0.002)

    def run_2D(self):

        # Run gprMax
        self.input = './Wall_2D.in'
        src_to_rx = 0.1
        resol = 0.002
        time_window = 50e-9
        pml_cells = 20
        pml = resol * pml_cells

        src_to_wall = 0.1
        src_to_rx = 0.05
        src_to_pml = 0.02

        sharp_domain = float(self.data['square_size']/100) + 2 * src_to_wall + 2* src_to_rx, self.data['square_size']/100 +  2* src_to_wall + 2*src_to_rx
        # sharp_domain = float(self.data['square_size']/100) + 2 * src_to_wall + src_to_rx, self.data['square_size']/100 +  2* src_to_wall + src_to_rx
        domain_2d = [
            float(sharp_domain[0] + 2 * pml + src_to_pml), 
            float(sharp_domain[1] + 2 * pml + src_to_pml), 
            0.002
        ]

        # Preprocess geometry

        try:
            with open('{}materials.txt'.format('Wall2D_'), "w") as file:
                file.write('#material: {} 0 1 0 wall\n'.format(self.wall_permittivity))
                file.write('#material: {} 0 1 0 object\n'.format(self.object_permittivity))
            self.preprocess()
        except Exception as e:
            print(e)

        src_position = [0.10, 0.10, 0]
        rx_position = [0.10 + src_to_rx, 0.10, 0]        
        
        # src_position = [0.10, 0.10, 0]
        # rx_position = [0.10, 0.10 - src_to_rx, 0]

        # src_position = [0.10 + 2* src_to_wall + self.data['square_size']/100, 0.10, 0]
        # rx_position = [0.10 + 2* src_to_wall + self.data['square_size']/100 +  src_to_rx, 0.10, 0]

        # src_position = [0.10 + 2* src_to_wall + self.data['square_size']/100, 0.10 + 2* src_to_wall + self.data['square_size']/100, 0]
        # rx_position = [0.10 + 2* src_to_wall + self.data['square_size']/100 , 0.10 + 2* src_to_wall + self.data['square_size']/100 + src_to_rx, 0]

        # src_position = [0.10 , 0.10 + 2* src_to_wall + self.data['square_size']/100, 0]
        # rx_position = [0.10 - src_to_rx, 0.10 + 2* src_to_wall + self.data['square_size']/100 , 0]
        
        src_steps = [float((self.data['square_size']/100 + 2* src_to_wall)/ self.num_scan), 0, 0]
        print(src_steps)
        config = f'''

#title: Wall Object Imaging

Configuration
#domain: {domain_2d[0]:.3f} {domain_2d[1]:.3f} {domain_2d[2]:.3f}
#dx_dy_dz: 0.002 0.002 0.002
#time_window: {time_window}

#pml_cells: {pml_cells} {pml_cells} 0 {pml_cells} {pml_cells} 0

Source - Receiver - Waveform
#waveform: ricker 1 1.0e9 my_wave

#hertzian_dipole: z {src_position[0]:.3f} {src_position[1]:.3f} {src_position[2]:.3f} my_wave 
#rx: {rx_position[0]:.3f} {rx_position[1]:.3f} {rx_position[2]:.3f}
#src_steps: {src_steps[0]:.3f} 0 0
#rx_steps: {src_steps[0]:.3f} 0 0

Geometry objects read

#geometry_objects_read: {0.10 + src_to_wall:.3f} {0.10 + src_to_wall:.3f} {0:.3f} Geometry/geometry_2d.h5 Wall2D_materials.txt
#geometry_objects_write: 0 0 0 {domain_2d[0]:.3f} {domain_2d[1]:.3f} {domain_2d[2]:.3f} Wall_2D 
        '''

        with open(self.input, 'w') as f:
            f.write(config)
            f.close()
        
        api(self.input, 
            n=self.num_scan-22, 
            # gpu=[0], 
            restart=23,
            geometry_only=False, geometry_fixed=False)
        
        merge_files(str(self.input.replace('.in','')), True)
        output_file =str(self.input.replace('.in',''))+ '_merged.out'
        dt = 0

        with h5py.File(output_file, 'r') as f1:
            data1 = f1['rxs']['rx1']['Ez'][()]
            dt = f1.attrs['dt']
            f1.close()

        # with h5py.File('base.out', 'r') as f1:
        #     data_source = f1['rxs']['rx1']['Ez'5][()]
        # src = data_source
        # # src = src[:, np.newaxis]
        # data1 = np.subtract(data1, src)

        with h5py.File(output_file, 'w') as f_out:
            f_out.attrs['dt'] = dt  # Set the time step attribute
            f_out.create_dataset('rxs/rx1/Ez', data=data1)

        # Draw data with normal plot
        rxnumber = 1
        rxcomponent = 'Ez'
        plt = mpl_plot_Bscan("merged_output_data", data1, dt, rxnumber,rxcomponent)
        
        file_names = "Wall2D"
        fig_width = 15
        fig_height = 15

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

        plt.imshow(data1, cmap='gray', aspect='auto')
        plt.axis('off')
        ax.margins(0, 0)  # Remove any extra margins or padding
        fig.tight_layout(pad=0)  # Remove any extra padding

        save_filename = file_names
        plt.savefig(save_filename + ".png")

        # outputs = Rx.defaultoutputs
        # outputs = ['Ez']
        # plt = mpl_plot_Ascan(self.input.replace('.in','.out'),outputs, fft=True)
        # f = h5py.File(self.input.replace('.in','')+'.h5', 'r')
        # dset = f['data']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wall Scanning for Through Wall Imaging")      
    parser.add_argument('--wall', type=str, default='wood', help='wall material')
    parser.add_argument('--wall_thickness', type=float, default=0.10, help='wall thickness')
    parser.add_argument('--wall_height', type=float, default=1.0, help='wall height')
    parser.add_argument('--wall_material', type=str, default='wood', help='wall material')
    parser.add_argument('--wall_permittivity', type=float, default=4.0, help='wall permittivity')
    parser.add_argument('--wall_conductivity', type=float, default=0.01, help='wall conductivity')
    parser.add_argument('--object_permittivity', type=float, default=13.0, help='object permittivity')
    parser.add_argument('--wall_loss', type=float, default=0.0, help='wall loss')

    args = parser.parse_args()

    # start  adaptor
    wallimg = Wall_Func(args=args)
    wallimg.run_2D()