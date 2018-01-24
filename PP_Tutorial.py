import numpy as np
import random
import math

import chemevolve as ce

#### Create CRS and READ PP file
PP_CRS = ce.Parser().parse_file('PP_CRS.txt')

### Generate initial concentrations
N_L = 1 # Size of the lattice (diffusion not yet implemented, fix at 1)
#total_mass = 
num_molecules = len(PP_CRS.molecule_list)

# Initialize array
concentrations = np.zeros( (N_L, N_L, num_molecules), dtype = np.float64 )
Aindex = PP_CRS.molecule_dict['A']
Bindex = PP_CRS.molecule_dict['B']
Eindex = PP_CRS.molecule_dict['E']

# Set monomer values
concentrations[0,0,Aindex] = 1000
concentrations[0,0,Bindex] = 1000
concentrations[0,0,Eindex] = 20


### Time Evolve
tau = 0.0 # Set current time
tau_max = 2.0 # Total Integration Interval
t_output = 0.010 # How frequently should data be output
freq_counter = 0.0 # Counts which output is coming next
rand_seed = 1337 # Seed for random number generator
output_prefix = 'PP_data' # This is a string that will procceed all file names assoicated with the outputs of this simulation
concentrations = ce.SSA_evolve_python(tau, tau_max, concentrations, PP_CRS, rand_seed, output_prefix = output_prefix, t_out = t_output)


# Visualize the Data
from chemevolve import Plotting as Plots # Since we'll plot the data at the end
# Plots.plot_length_distribution(output_prefix + '_time_series_df.csv')
# Plots.plot_molecule_distribution(output_prefix + '_time_series_df.csv')
Plots.plot_time_series(output_prefix + '_time_series_df.csv', ['A', 'B'])