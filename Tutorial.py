import numpy as np
import random
import math

import chemevolve as ce
from chemevolve import BinaryPolymer as BinPoly # Since we'll use a binary polymer model here

#### Generate a chemical Reaction System (CRS)
max_length = 6 # Maximum Length of binary polymers
k_l = 0.001	# Forward (ligation) Reaction Rate constant
k_d = 1.0   # Backward (degradation) Reaction Rate constant

CRS = BinPoly.generate_all_binary_reactions(max_length, fconstant = k_l, bconstant = k_d)

### Generate initial concentrations
N_L = 1 # Size of the lattice (diffusion not yet implemented, fix at 1)
total_mass = 10000
num_molecules = len(CRS.molecule_list)

# Initialize array
concentrations = np.zeros( (N_L, N_L, num_molecules), dtype = np.float64 )
Aindex = CRS.molecule_dict['A']
Bindex = CRS.molecule_dict['B']
# Set monomer values
concentrations[0,0,Aindex] = total_mass/2.0
concentrations[0,0,Bindex] = total_mass/2.0


### Time Evolve
tau = 0.0 # Set current time
tau_max = 1.0 # Total Integration Interval
t_output = 0.1 # How frequently should data be output
freq_counter = 0.0 # Counts which output is coming next
rand_seed = 1337 # Seed for random number generator
output_prefix = 'tutorial_data' # This is a string that will procceed all file names assoicated with the outputs of this simulation
concentrations = ce.SSA_evolve(tau, tau_max, concentrations, CRS, rand_seed, output_prefix = output_prefix, t_out = t_output)


# Visualize the Data
from chemevolve import Plotting as Plots # Since we'll plot the data at the end
Plots.plot_length_distribution(output_prefix + '_time_series_df.csv')
Plots.plot_molecule_distribution(output_prefix + '_time_series_df.csv')
Plots.plot_time_series(output_prefix + '_time_series_df.csv', ['A', 'B'])