import numpy as np
import pickle
import math

def create_reaction_system(filename):
	'''Reads a saved Reaction System and returns the CRS object 

	Arguements:
		- filename: the path to the saved Reaction System file (str)

	Returns:
		- CRS: Reaction System Object of the CRS class.'''
	from Parser import Parser
	print(filename)
	return Parser.parse_file(filename)
	
def read_concentration_files_old(file_prefix):
	'''Opens a concentration file (.npy array) and a molecule list file 
	returns the numpy array with concentrations the last index identifying the molecular species
	the molecules list maps array indexes to molecular identities'''
	concentration_arr = np.load(file_prefix+ '_concentrations.npy')
	with open(file_prefix+ '_molecules.txt', 'rb') as f:
		molecules = pickle.load(f)

	return molecules, concentration_arr

def read_concentration_files(file_prefix):
	'''Opens a concentration file (.dat pickle list) and a molecule list file 
	returns the numpy array with concentrations the last index identifying the molecular species
	the molecules list maps array indexes to molecular identities'''
	fname = file_prefix+ '_concentrations.dat'
	infile1 = open(fname, 'r+b')
	file1 = pickle.load(infile1)                           # This is a list
	infile1.close()
	concentration_arr = np.array(file1)
	concentration_arr = np.ascontiguousarray(concentration_arr, np.int32)
	with open(file_prefix+ '_molecules.txt', 'rb') as f:
		molecules = pickle.load(f)

	return molecules, concentration_arr

def create_concentration_files_old(file_prefix, N_L, molecules, concentrations, coordinates, dimensions = 2):
	'''Create a concentration file to load as a np array
	dimensions - int, number of spatial dimensions
	N_L - int, size of one side of regular lattice
	molecules - list of strings representing molecules
	concentrations - list of ints representing abdunace of molecule at a particular site
	coordinates - list of tuples, coordinates in the lattice '''

	molecule_list = []
	print(len(molecules), len(concentrations), len(coordinates))
	assert(len(molecules) == len(concentrations) and len(molecules) == len(coordinates))
	assert(len(coordinates[0]) == dimensions)
	# Initialize the lattice 
	shape = [N_L]*dimensions
	# Add a dimension to index the molecules
	shape.append(1)
	concentration_arr = np.zeros(shape)

	for m in range(len(molecules)):
		assert(type(molecules[m]) == str)

		if molecules[m] in molecule_list:
			index = molecule_list.index(molecules[m])
		else:
			molecule_list.append(molecules[m])
			#print 'Molecule: ', molecules[m]
			index = molecule_list.index(molecules[m])
			#print 'Molecule Index: ',index
			if index == concentration_arr.shape[-1]:
				concentration_arr = np.dstack( (concentration_arr,np.zeros([N_L]*dimensions)) )
				#print concentration_arr.shape
		arr_indices = coordinates[m] +(index,)
		
		concentration_arr[arr_indices] = concentrations[m]
	#print molecule_list
	#print concentration_arr
	np.save(file_prefix+ '_concentrations.npy', concentration_arr)
	with open(file_prefix+ '_molecules.txt', 'wb') as f:
		pickle.dump(molecule_list, f)

def create_concentration_files(file_prefix, N_L, molecules, concentrations, coordinates, dimensions = 2):
	'''Create a concentration file to load as a np array
	dimensions - int, number of spatial dimensions
	N_L - int, size of one side of regular lattice
	molecules - list of strings representing molecules
	concentrations - list of ints representing abdunace of molecule at a particular site
	coordinates - list of tuples, coordinates in the lattice '''

	molecule_list = []
	#print len(molecules), len(concentrations), len(coordinates)
	assert(len(molecules) == len(concentrations) and len(molecules) == len(coordinates))
	assert(len(coordinates[0]) == dimensions)
	# Initialize the lattice 
	shape = [N_L]*dimensions
	# Add a dimension to index the molecules
	shape.append(1)
	concentration_arr = np.zeros(shape)

	for m in range(len(molecules)):
		assert(type(molecules[m]) == str)

		if molecules[m] in molecule_list:
			index = molecule_list.index(molecules[m])
		else:
			molecule_list.append(molecules[m])
			#print 'Molecule: ', molecules[m]
			index = molecule_list.index(molecules[m])
			#print 'Molecule Index: ',index
			if index == concentration_arr.shape[-1]:
				concentration_arr = np.dstack( (concentration_arr,np.zeros([N_L]*dimensions)) )
				#print concentration_arr.shape
		arr_indices = coordinates[m] +(index,)
		
		concentration_arr[arr_indices] = concentrations[m]
	#print molecule_list
	#print concentration_arr
	#np.save(file_prefix+ '_concentrations.npy', concentration_arr)
	fname = file_prefix+ '_concentrations.dat'
	outfile1 = open(fname, 'w+b')
	pickle.dump(concentration_arr.tolist(), outfile1)
	outfile1.close()
	with open(file_prefix+ '_molecules.txt', 'wb') as f:
		pickle.dump(molecule_list, f)



def convert_CRS_to_npArrays(CRS):
	''' 
	This function converts ChemEvolve CRS objects into 4 numpy arrays. This allows the information to be easily passed to C.

	Input:
		- CRS: Chemical Reaction System Object

	Output:
		- constants: np double array with reaction constant values
		- propensity_ints: np int32 array with integer identifying which propensity function to use
		- reaction_arr: np int32 array with integers indicating the stochimetry of each reaction. 
			Each row is a reaction, each column is a molecule. Reactants are negative, products are postive
		- catalyst_arr: np double array with the effect of each molecule for each reaction.
			Rows are reactions, columns are molecule, non-zero value indicate catalysis 
	''' 

	propensity_dict = {'STD':0, 'RCM':1}

	num_Reactions = len(CRS.reactions)
	num_Molecules = len(CRS.molecule_list)

	constants = [x.constant for x in CRS.reactions]
	constants  = np.array(constants, dtype = float, order = 'C')

	propensity_strs = [x.prop for x in CRS.reactions]
	propensity_ints = np.array([propensity_dict[s] for s in propensity_strs], dtype = int, order = 'C')

	reaction_arr = np.zeros((num_Reactions, num_Molecules), dtype = int)
	catalyst_arr = np.zeros((num_Reactions, num_Molecules), dtype = float)

	for r in range(num_Reactions):
		reactants = CRS.reactions[r].reactants
		reactant_coeff = CRS.reactions[r].reactant_coeff
		products = CRS.reactions[r].products
		product_coeff = CRS.reactions[r].product_coeff
		cat_IDs = CRS.reactions[r].catalysts
		cat_constants = CRS.reactions[r].catalyzed_constants

		for i in range(len(reactants)):
			reaction_arr[r, reactants[i]] = -reactant_coeff[i]

		for i in range(len(products)):
			reaction_arr[r, products[i]] = product_coeff[i]

		for i in range(len(cat_IDs)):
			catalyst_arr[r, cat_IDs[i]] = cat_constants[i]

	
	constants = np.ascontiguousarray(constants, np.float64)
	propensity_ints = np.ascontiguousarray(propensity_ints, np.int32)
	reaction_arr = np.ascontiguousarray(reaction_arr, np.int32)
	catalyst_arr = np.ascontiguousarray(catalyst_arr, np.float64)
	
	return constants, propensity_ints, reaction_arr, catalyst_arr 
		


def get_c_pointers(concentrations, constants, propensity_ints, reaction_arr, catalyst_arr):
	'''This function returns the C pointers to the input arrays. Pointers must be pasted to SSA library functions
	
	Arguments:
		- concentrations: array of doubles containing molecule abundances
		- constants: array of np doubles containing reaction constants
		- propensity_ints: array of np int32 containing propesity integer codes 
		- reaction_arr: np int32 array with integers indicating the stochimetry of each reaction. 
			Each row is a reaction, each column is a molecule. Reactants are negative, products are postive
		- catalyst_arr: np double array with the effect of each molecule for each reaction.
			Rows are reactions, columns are molecule, non-zero value indicate catalysis
	Return:
	 	- concentrations_ptr: points to concentration array
	 	- constants_ptr: points to constants array
	 	- propensity_ints_ptr: points to propensity_ints array
	 	- reaction_arr_ptr: points to reaction_arr array
	 	- catalyst_arr_ptr: points to catalyst_arr
	'''
	from ctypes import c_int,  c_double, POINTER
	concentrations_ptr = concentrations.ctypes.data_as(POINTER(c_double))
	constants_ptr = constants.ctypes.data_as(POINTER(c_double))
	propensity_ints_ptr = propensity_ints.ctypes.data_as(POINTER(c_int))
	reaction_arr_ptr = reaction_arr.ctypes.data_as(POINTER(c_int))
	catalyst_arr_ptr = catalyst_arr.ctypes.data_as(POINTER(c_double))


	return concentrations_ptr, constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr


