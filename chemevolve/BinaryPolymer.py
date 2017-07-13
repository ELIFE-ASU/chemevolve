import numpy as np
import pickle
from InitializeFunctions import *
####################################################
def check_mass(original_mass, CRS, concentrations):
	''' Checks conservation of mass
	Arguements
		- original_mass: integer mass of the original system
		- CRS: CRS object
		- concentrations: array of molecule abundances

		 '''
	mass_conserved = False
	test_mass = 0.0
	molecules = CRS.molecule_list
	for m in molecules:
		index =	molecules.index(m)

		molecule_size = len(m)
		molecule_count = np.sum(concentrations[:,:,index])
		mass = molecule_count*molecule_size

		test_mass += mass 
	if test_mass == original_mass:
		mass_conserved = True
	return mass_conserved, test_mass

####################################################
def generate_all_binary_reactions(max_length, fconstant = 1.0, bconstant = None):
	''' Generates all possible reactions between binary molecules up to size max_length assigns all reactions the same constant and standard prorpenisty
	Arguements:
		- max_length: the maximum length of polymers
		- fconstant: reaction rate constant for forward reactions
		- bconstant: reaction rate constant for reverse reactions, if None given, it will be assigned to be equal to fconstant
	 '''
	import CoreClasses as Core
	import itertools
	rxn_IDs = []
	reaction_list = []
	molecule_list = []
	molecule_dict = {}
	rxn_ID = 0
	#molecule_ID = 0
	monomers = 'AB'
	# If the backward constant is not specified, make it equal the forward constant
	if bconstant == None:
		bconstant = fconstant
	for l in range(1,max_length+1):
		# Generate all sequences of length l+1
		sequences = itertools.product(monomers, repeat = l)
		for seq in sequences:
			s = ''.join(seq)
			molecule_list.append(s)
			molecule_dict[s] = molecule_list.index(s)
			#print s
			for i in range(1,l):
				# Forward Reaction
				rxn_ID = len(reaction_list)
				reactants = [ molecule_dict[s[:i]], molecule_dict[s[i:]] ]
				reactant_coeff = [1,1]
				product_coeff = [1]
				products = [ molecule_dict[s] ]
				reaction_list.append( Core.Reaction(rxn_ID, reactants = reactants, reactant_coeff = reactant_coeff , products = products, product_coeff = product_coeff, constant = fconstant, prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)
				
				# Backward Reaction
				rxn_ID = len(reaction_list)
				reaction_list.append( Core.Reaction(rxn_ID, products = reactants, product_coeff = reactant_coeff, reactants = products, reactant_coeff= reactant_coeff, constant = bconstant, prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)
				
	#print molecule_dict
	newCRS = Core.CRS(molecule_list = molecule_list, molecule_dict = molecule_dict, reactions = reaction_list)
	#print newCRS.molecule_dict
	# fname = 'reversible_binary_length_%i.txt' % max_length
	# newCRS.savetxt(fname)
	return newCRS

####################################################	
def generate_wim_RAF(max_length, fconstant = 1.0, bconstant = None, f_cat = 1.0):
	''' Generates all possible reactions between binary molecules up to size max_length assigns all reactions the same constant and standard prorpenisty
	Arguements:
		- max_length: the maximum length of polymers
		- fconstant: reaction rate constant for forward reactions
		- bconstant: reaction rate constant for reverse reactions, if None given, it will be assigned to be equal to fconstant
	 '''
	import CoreClasses as Core
	import itertools
	rxn_IDs = []
	reaction_list = []
	molecule_list = []
	molecule_dict = {}
	rxn_ID = 0
	#molecule_ID = 0
	monomers = 'AB'
	# If the backward constant is not specified, make it equal the forward constant
	if bconstant == None:
		bconstant = fconstant
	for l in range(1,max_length+1):
		# Generate all sequences of length l+1
		sequences = itertools.product(monomers, repeat = l)
		for seq in sequences:
			s = ''.join(seq)
			molecule_list.append(s)
			molecule_dict[s] = molecule_list.index(s)
			#print s
	for s in molecule_list:
		l = len(s)
		for i in range(1,l):
			# Forward Reaction
			rxn_ID = len(reaction_list)
			reactants = [ molecule_dict[s[:i]], molecule_dict[s[i:]] ]
			reactant_coeff = [1,1]
			product_coeff = [1]
			products = [ molecule_dict[s] ]
			catalysts = list()
			f_list = list()
			if s == 'AA':
				if [s[:i], s[i:]]== ['A', 'A']:
					# print s, s[:i], s[i:]
					catalysts = [molecule_dict['AAA']]
					f_list = [f_cat]
			elif s == 'AAA':
				if [s[:i], s[i:]] == ['AA', 'A']:
					# print s, s[:i], s[i:]
					catalysts = [molecule_dict['AAA']]
					f_list = [f_cat]
			elif s == 'BAA':
				if [s[:i], s[i:]] == ['BA', 'A']:
					print s, s[:i], s[i:]
					catalysts = [molecule_dict['AAA']]
					f_list = [f_cat]
			elif s == 'BB':
				if [s[:i], s[i:]] == ['B', 'B']:
					# print s, s[:i], s[i:]
					catalysts = [molecule_dict['BBB']]
					f_list = [f_cat]
			elif s == 'BBB':
				if [s[:i], s[i:]] == ['B', 'BB']:
					# print s, s[:i], s[i:]
					catalysts = [molecule_dict['BBB']]
					f_list = [f_cat]
			elif s == 'ABB':
				if [s[:i], s[i:]] == ['AB', 'B']:
					# print s, s[:i], s[i:]
					catalysts = [molecule_dict['BBB']]
					f_list = [f_cat]
			
			reaction_list.append( Core.Reaction(rxn_ID, reactants = reactants, reactant_coeff = reactant_coeff , products = products, product_coeff = product_coeff, constant = fconstant, catalysts = catalysts, catalyzed_constants = f_list, prop = 'STD') )
			#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
			rxn_IDs.append(rxn_ID)
			
			# Backward Reaction
			rxn_ID = len(reaction_list)
			reaction_list.append( Core.Reaction(rxn_ID, products = reactants, product_coeff = reactant_coeff, reactants = products, reactant_coeff= reactant_coeff, constant = bconstant, prop = 'STD') )
			#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
			rxn_IDs.append(rxn_ID)
			
	#print molecule_dict
	newCRS = Core.CRS(molecule_list = molecule_list, molecule_dict = molecule_dict, reactions = reaction_list)
	#print newCRS.molecule_dict
	fname = 'RandomRAF/data/wim_RAF/wim_RAF_f_%.4f_length_%i.txt' % (f_cat, max_length)
	newCRS.savetxt(fname)
	print "Wim CRS saved"
	return fname

####################################################
def generate_random_rate_polymerization_reactions(output_name, max_length, fconstant = 1.0, bconstant = None, fdis_type = 'exp', bdis_type= 'exp'):
	''' Generates all possible polymerization reactions for molecules up to size max_length assigns all reactions a random constant and standard prorpenisty
	Arguements:
		- output_name: filename to save as output (should be .txt)
		- max_length: the maximum length of polymers
		- fconstant: mean reaction rate constant for forward reactions
		- bconstant: mean reaction rate constant for reverse reactions, if None given, it will be assigned to be equal to fconstant
	 '''
	import CoreClasses as Core
	import itertools
	rxn_IDs = []
	reaction_list = []
	molecule_list = []
	molecule_dict = {}
	rxn_ID = 0
	#molecule_ID = 0
	monomers = 'AB'
	# If the backward constant is not specified, make it equal the forward constant
	if bconstant == None:
		bconstant = fconstant
	for l in range(1,max_length+1):
		# Generate all sequences of length l+1
		sequences = itertools.product(monomers, repeat = l)
		for seq in sequences:
			s = ''.join(seq)
			molecule_list.append(s)
			molecule_dict[s] = molecule_list.index(s)
			if l >1:
				# Forward Reaction
				if fdis_type == 'exp':
					f_rate = np.random.exponential(scale = fconstant )
				elif fdis_type == 'heavy_tail':
					alpha = 1.0 - (1.0/fconstant)
					f_rate = np.random.pareto(alpha)
				rxn_ID = len(reaction_list)
				reactants = [ molecule_dict[s[:(l-1)]], molecule_dict[s[(l-1):]] ]

				reactant_coeff = [1,1]
				product_coeff = [1]
				products = [ molecule_dict[s] ]
				reaction_list.append( Core.Reaction(rxn_ID, reactants = reactants, reactant_coeff = reactant_coeff , products = products, product_coeff = product_coeff, constant = f_rate, prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)
				
				# Backward Reaction
				if bdis_type == 'exp':
					b_rate = np.random.exponential(scale = bconstant )
				elif bdis_type == 'heavy_tail':
					alpha = 1.0 - (1.0/bconstant)
					b_rate = np.random.pareto(alpha)
				rxn_ID = len(reaction_list)
				reaction_list.append( Core.Reaction(rxn_ID, products = reactants, product_coeff = reactant_coeff, reactants = products, reactant_coeff= reactant_coeff, constant = b_rate, prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)

				if s[:(l-1)] != s[1:l] and l>2:
					if fdis_type == 'exp':
						f_rate = np.random.exponential(scale = fconstant )
					elif fdis_type == 'heavy_tail':
						alpha = 1.0 - (1.0/fconstant)
						f_rate = np.random.pareto(alpha)
					rxn_ID = len(reaction_list)
					reactants = [ molecule_dict[s[0]], molecule_dict[s[1:l]] ]

					reactant_coeff = [1,1]
					product_coeff = [1]
					products = [ molecule_dict[s] ]
					reaction_list.append( Core.Reaction(rxn_ID, reactants = reactants, reactant_coeff = reactant_coeff , products = products, product_coeff = product_coeff, constant = f_rate, prop = 'STD') )
					#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
					rxn_IDs.append(rxn_ID)
					
					# Backward Reaction
					if bdis_type == 'exp':
						b_rate = np.random.exponential(scale = bconstant )
					elif bdis_type == 'heavy_tail':
						alpha = 1.0 - (1.0/bconstant)
						b_rate = np.random.pareto(alpha)
					rxn_ID = len(reaction_list)
					reaction_list.append( Core.Reaction(rxn_ID, products = reactants, product_coeff = reactant_coeff, reactants = products, reactant_coeff= reactant_coeff, constant = b_rate, prop = 'STD') )
					#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
					rxn_IDs.append(rxn_ID)

				
	#print molecule_dict
	newCRS = Core.CRS(molecule_list = molecule_list, molecule_dict = molecule_dict, reactions = reaction_list)
	#print newCRS.molecule_dict
	
	newCRS.savetxt(output_name)
	print "New CRS saved"

####################################################
def generate_uniform_monomers(CRS, N_L, total_mass):
	import itertools
	concentrations = np.zeros((N_L, N_L, len(CRS.molecule_list))  )
	num_sites = N_L**2
	per_site_mass = math.floor(float(total_mass)/num_sites)
	per_monomer_per_site_mass = math.floor(per_site_mass/2.0)

	for x in range(N_L):
		for y in range(N_L):
			for m in range(2):
				concentrations[x,y,m] = per_monomer_per_site_mass
	
	#concentrations = np.ascontiguousarray(concentrations, np.int32)
	return concentrations 

####################################################
def generate_uniform_monomers_dimers(CRS, N_L, total_mass):
	import itertools

	concentrations = np.zeros((N_L, N_L, len(CRS.molecule_list))  )
	num_sites = N_L**2
	per_site_concentration = math.floor(float(total_mass)/(10*num_sites))
	
	for x in range(N_L):
		for y in range(N_L):
			for m in range(6):
				concentrations[x,y,m] = per_site_concentration
	return concentrations 
