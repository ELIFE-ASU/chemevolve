import numpy as np
import PropensityFunctions as Propensity
import CoreClasses as Core 
import random
import OutputFunctions as Out
import InitializeFunctions as Init

####################################################
### Load C library
####################################################
from ctypes import cdll
from ctypes import byref, c_int, c_ulong, c_double, POINTER
def get_libpath():
    """
    Get the library path of the the distributed SSA library.
    """
    import os
    import re
    from os.path import dirname, abspath, realpath, join
    from platform import system

    dirname = os.getcwd()
    if system() == 'Linux':
        library = 'Linux-SSA.so'
    elif system() == 'Darwin':
        library = 'OSX-SSA.so'
    elif system() == 'Windows':
        library = "Win-SSA.so"
    else:
        raise RuntimeError("unsupported platform - \"{}\"".format(system()))

    return os.path.join(dirname, 'chemevolve', 'clibs', library)

_SSA_LIB = cdll.LoadLibrary(get_libpath())
#                               current_t, next_t,  r_seed, max_x, max_y, num_m, num_r, concentrations,     constants         propensity_ints, reaction_arr,  catalyst_arr
_SSA_LIB.SSA_update.argtypes = (c_double, c_double, c_int, c_int, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_int), POINTER(c_double))
_SSA_LIB.SSA_update.restype = c_double
SSA_update = _SSA_LIB.SSA_update ### Renaming function for convinence
####################################################
####################################################
def pick_reaction(dice_roll, CRS, concentrations, **kwargs):
	''' Picks a reaction to occur stochastically 

	Arguements:
		- dice_roll: float which should be a number between zero and the total propensity of reactions
		- CRS: the CRS object which contains all possible reactions and molecules
		- concentrations: the list of concentrations indexed by molecule ID
		- propensity_function: which propensity function to use, default: standard

	Return:
		- rxn: a Reaction object'''

	checkpoint = 0.0
	for rxn in CRS.reactions:
		reactant_concentrations = [concentrations[i] for i in rxn.reactants]
		catalyst_concentrations = [concentrations[i] for i in rxn.catalysts]
		reactant_coeff = rxn.reactant_coeff
		catalyzed_constants = rxn.catalyzed_constants
		#print rxn.catalysts
		if rxn.prop == 'STD':
			# print "Reactant concentrations: ", reactant_concentrations
			# print 'Product ID numbers: ',rxn.products
			checkpoint += Propensity.standard_propensity(rxn, CRS, concentrations)
			#print "dice_roll: ", dice_roll, ' checkpoint: ', checkpoint
			if checkpoint >= dice_roll:
				break
			
		
	#raw_input("Enter")
	return rxn
####################################################
def execute_rxn(rxn, CRS, concentrations):
	''' Executes a single reaction instance

	Arguements:
		- rxn: Reaction object to execute_rxn
		- CRS: CRS object containing the entire system
		- concentrations: list of molecule concentrations indexed by ID

	Return:
		- concentrations: updated list of molecule concentrations indexed by ID '''
	num_reactants = len(rxn.reactants)
	
	num_products = len(rxn.products)
	
	# Reduce Reactants
	for i in range(num_reactants):
		reactant_index = rxn.reactants[i]
		concentrations[reactant_index] -= rxn.reactant_coeff[i]
		
	# Increase Products	
	for i in range(num_products):
		product_index =rxn.products[i]
		concentrations[product_index] += rxn.product_coeff[i]
		
	return concentrations
####################################################
def SSA_evolve(tau, tau_max, concentrations, CRS, random_seed, output_prefix= None,  t_out= None):

	if (output_prefix != None and t_out == None):
		raise ValueError('Output file prefix specified but no output frequency given, please provide an output time frequency')
		
	elif (output_prefix == None and type(t_out) == float):
		raise ValueError('Output frequency provided but output file prefix was not provided, please provide a file prefix name')
		
	import sys
	import random
	from ctypes import c_int,  c_double, POINTER
	constants, propensity_ints, reaction_arr, catalyst_arr = Init.convert_CRS_to_npArrays(CRS)
	concentrations_ptr, constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr= Init.get_c_pointers(concentrations, constants, propensity_ints, reaction_arr, catalyst_arr)
	freq_counter = 0.0
	random.seed(random_seed)
	while tau < tau_max:
		# Get seed
		r_seed = random.randint(0, sys.maxint)
		# Update concentrations in place using C function
		c_tau = SSA_update(c_double(tau), c_double(freq_counter),r_seed, c_int(1),c_int(1), c_int(len(CRS.molecule_list)), c_int(len(constants)), concentrations_ptr, constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr )
		# Update Time
		tau = c_tau
		# Update random seed
		random.jumpahead(tau-freq_counter)
		print tau
		# Output data
		Out.output_concentrations(concentrations, 'tutorial_data',time = freq_counter)
		freq_counter += t_out
	Out.tidy_timeseries(CRS.molecule_list, 'tutorial_data', delete_dat = True)

	return concentrations