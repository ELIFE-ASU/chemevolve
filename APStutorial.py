import numpy as np
import random
import math

import chemevolve as ce
from chemevolve import APSfunctions as APS # Since we'll use a APS module here
from chemevolve import Plotting as Plots # Since we'll plot the data at the end

#### Generate a chemical Reaction System (CRS)
max_length = 4 # Maximum Length of binary polymers
beta = 1.0 # inverse "temperature"
k_d = 1.0   # Backward (degradation) Reaction Rate constant
APS_heatmap = 'C_Int_3merplus_0-3DHR_060916_new_matrices_SO4.csv'
amino_acids = 'ADEG'#HKLPTV'

CRS = APS.generate_CRS_from_AA_intensities(APS_heatmap, amino_acids, max_length, beta, kd= 1.0)

# ### Generate initial concentrations
mass_per_monomer = 10000.0/len(amino_acids)
N_L = 1 # Size of the lattice (diffusion not yet implemented, fix at 1)
num_molecules = len(CRS.molecule_list)

### Initialize array
concentrations = np.zeros( (N_L, N_L, num_molecules), dtype = np.float64 )
# Set monomer values
for i in range(num_molecules):
	if len(CRS.molecule_list[i]) == 1:
		concentrations[0,0,i] = mass_per_monomer
		
### Time Evolve
tau = 0.0 # Set current time
tau_max = 1.0 # Total Integration Interval
t_output = 0.1 # How frequently should data be output
freq_counter = 0.0 # Counts which output is coming next
rand_seed = 1337 # Seed for random number generator
output_prefix = 'tutorial_data' # This is a string that will procceed all file names assoicated with the outputs of this simulation
concentrations = ce.SSA_evolve(tau, tau_max, concentrations, CRS, rand_seed, output_prefix = output_prefix, t_out = t_output)


# # Visualize the Data
Plots.plot_length_distribution(output_prefix + '_time_series_df.csv')
Plots.plot_molecule_distribution(output_prefix + '_time_series_df.csv')