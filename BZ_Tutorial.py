import numpy as np
import random
import math

import chemevolve as ce

#### Create CRS from BZ file
BZ_CRS = ce.Parser().parse_file('BZ_CRS.txt')

### Generate initial concentrations
N_L = 1 # Size of the lattice (diffusion not yet implemented, fix at 1)
num_molecules = len(BZ_CRS.molecule_list)

# Initialize array
concentrations = np.zeros( (N_L, N_L, num_molecules), dtype = np.float64 )
Aindex = BZ_CRS.molecule_dict['A']
Bindex = BZ_CRS.molecule_dict['B']
Xindex = BZ_CRS.molecule_dict['X']
Yindex = BZ_CRS.molecule_dict['Y']

# Set monomer values
concentrations[0,0,Aindex] = 5000
concentrations[0,0,Bindex] = 50
concentrations[0,0,Xindex] = 2000
concentrations[0,0,Yindex] = 1000

### Time Evolve
tau = 0.0 # Set current time
tau_max = 1.0 # Total Integration Interval
t_output = 0.010 # How frequently should data be output?
freq_counter = 0.0 # Counts which output is coming next
rand_seed = 2337 # Seed for random number generator

output_prefix = 'BZ_data' # This is a string that will procceed all file names assoicated with the outputs of this simulation

# This function does the time evolution
concentrations = ce.SSA_evolve_python(tau, tau_max, concentrations, BZ_CRS, rand_seed, output_prefix = output_prefix, t_out = t_output)


# Visualize the Data
from chemevolve import Plotting as Plots # Since we'll plot the data at the end
Plots.plot_time_series(output_prefix + '_time_series_df.csv', ['X', 'Y'])