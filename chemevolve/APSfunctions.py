import CoreClasses as Core
import InitializeFunctions as Initialize

import numpy as np
import time
import re
import random 
import os
import pickle 
import sys
import copy
import math



def check_mass(original_mass, CRS, concentrations):
	''' Checks conservation of mass
	Arguements
		- original_mass: integer mass of the original system
		- CRS: CRS object
		- concentrations: array of molecule abundances

		 '''
	print concentrations
	mass_conserved = False
	test_mass = 0.0
	molecules = CRS.molecule_list
	for m in molecules:
		index =	molecules.index(m)

		molecule_size = len(m)
		molecule_count = np.sum(concentrations[:,:, index])
		mass = molecule_count*molecule_size
		test_mass += mass 
	if test_mass == original_mass:
		mass_conserved = True
	return mass_conserved, test_mass

def calculate_mass_fraction_by_composition(concentrations, CRS, total_mass):
	''' Takes an abundace distribution and returns a mass fraction distribution (which is a dictionary, keys are composition, values are mass_fraction) '''
	
	molecules = CRS.molecule_list
	mass_fraction = {}

	for m in molecules:
			index = molecules.index(m)
			comp = get_composition(m)
			molecule_size = len(m)
			molecule_count = float(np.sum(concentrations[:,:,index]))

			mass = molecule_count*molecule_size

			if comp in mass_fraction.keys():
				mass_fraction[comp] += float(mass)/float(total_mass)
			else:
				mass_fraction[comp] = float(mass)/float(total_mass)

	return mass_fraction

def calculate_molecule_fraction_by_composition(concentrations, CRS, total_mass):
	''' Takes an abundace distribution and returns a mass fraction distribution (which is a dictionary, keys are composition, values are mass_fraction) '''
	
	molecules = CRS.molecule_list
	molecule_fraction = {}
	total_molecules = 0.0
	for m in molecules:
			index = molecules.index(m)
			comp = get_composition(m)
			molecule_size = len(m)
			molecule_count = float(np.sum(concentrations[:,:,index]))
			total_molecules += molecule_count
			#mass = molecule_count

			if comp in molecule_fraction.keys():
				molecule_fraction[comp] += float(molecule_count)
			else:
				molecule_fraction[comp] = float(molecule_count)
	for comp in molecule_fraction.keys():
		molecule_fraction[comp] = float(molecule_fraction[comp])/float(total_molecules)
	return molecule_fraction

def get_aa(comp):
	''' Returns the amino acids in a given composition string '''
	aa = []
	coef = re.findall(r'\d+', comp)
	for i in range(len(coef)):
		 comp = comp.replace(coef[i], ' ')
	aa = comp.split()
	return aa

def get_reaction_constants(CRS):
	''' Returns a list of reaction constants for from a CRS '''
	constants = {}
	for rID in range(len(CRS.reactions)):
		if sum(CRS.reactions[rID].product_coeff) == 1:
			rxn = CRS.reactions[rID]
			constants[rID] = rxn.constant
	
	return constants

def generate_random_distribution(CRS, total_mass, N_L = 1):
	''' Generates a random distribution of molecules for a given CRS '''
	molecules = CRS.molecule_list
	concentrations = np.zeros( (N_L, N_L, len(molecules)) )
	molecule_dict = CRS.molecule_dict
	mass = total_mass
	monomers_in_seqs = {}
	while mass > 0.1*(total_mass):
		m= random.choice(molecules)
		mID = molecule_dict[m]
		concentrations[0,0, mID] += 1
		comp = get_composition(m)
		coef = map(int, re.findall(r'\d+', comp))
		mass -= sum(coef)
		aa = get_aa(comp)
		for a in range(len(aa)):
			if aa[a] in monomers_in_seqs.keys():
				monomers_in_seqs[aa[a]] += coef[a]
			else:
				monomers_in_seqs[aa[a]] = coef[a]
	#print mass
	diff = total_mass- mass 
	monomer_names= monomers_in_seqs.keys()
	concentrations[0,0,0] += int( (monomers_in_seqs[monomer_names[0]] - monomers_in_seqs[monomer_names[1]])/(2.0) + (diff/2.0) )
	concentrations[0,0,1] += int( (monomers_in_seqs[monomer_names[1]] - monomers_in_seqs[monomer_names[0]])/(2.0) + (diff/2.0) )
	
	return concentrations


def set_reaction_constants(original_CRS, new_constants ):
	''' Sets the reaction constants in the CRS to new_constants 
		Returns the CRS with updated constants'''
	newCRS = copy.deepcopy(original_CRS)
	for rID in new_constants.keys():
		rxn = newCRS.reactions[rID]
		rxn.constant = copy.deepcopy(new_constants[rID])
		newCRS.reactions[rID] = rxn
		
	return newCRS

def get_composition(seq):
	'''Gets the composition of the seq. Returns a string which contains the stoichimetry of the seq. Monoomers are sorted alphabetically. '''
	comp = ''
	monomers = sorted(list(set(seq)))

	for m in monomers:
		comp+= m +str(seq.count(m)) 
	return comp

def mutate(float_vec, mu, epsilion, as_percentage = True, targets = None):
	''' Mutates a vector of floating point numbers. Mu is the fraction of numbers to be changed. 
		Half of the changes result in the number being replaced by another number in the vector
		The remaining half of changes will cause small change to the number
		if as_percentage is True, the change will be scaled by the size of the original number '''
	if targets ==None:
		new_vec = {}
		nV = len(float_vec.values())
		
		nR = int(np.floor(0.25*nV*mu))
		nM = nV - nR

		mutations = np.random.choice(float_vec.keys(), size= (nM), replace = False)
		replacements = np.random.choice(float_vec.keys(), size= (nR), replace = False)
		for i in mutations:
			# Mutate
			if as_percentage == True:
				delta = np.random.normal(0,float_vec[i]*epsilion)
				new_vec[i] = float_vec[i] + delta
				new_vec[i] = abs(new_vec[i])
			else:
				new_vec[i] = float_vec[i] + np.random.normal(0, epsilion)
				new_vec[i] = abs(new_vec[i])
		for i in replacements:
				# Replace
				new_vec[i] = float_vec[np.random.choice(list(float_vec.keys()), size = 1)[0]]
		return new_vec
	else:
		new_vec = {}
		nV = len(targets)
		nR = int(np.floor(0.5*nV))
		nM = nV - nR
		mutations = np.random.choice(float_vec.keys(), size= (nM), replace = False)
		replacements = np.random.choice(float_vec.keys(), size= (nR), replace = False)
		for i in mutations:
			# Mutate
			if as_percentage == True:
				delta = np.random.normal(0,float_vec[i]*epsilion)
				new_vec[i] = float_vec[i] + delta
				new_vec[i] = abs(new_vec[i])
			else:
				new_vec[i] = float_vec[i] + np.random.normal(0, epsilion)
				new_vec[i] = abs(new_vec[i])
		for i in replacements:
				# Replace
				new_vec[i] = float_vec[np.random.choice(list(float_vec.keys()), size = 1)[0]]
		return new_vec


def generate_concentrations_from_data(mass_fraction, CRS, total_mass, monomer_fraction = 0.25, N_L = 1):
	''' Generates a concentration array from a given mass fraction  
		Assumes that the mass of a given composition is distributed evenly 
		Assumes that the mass of monomers is monomer_fraction of the total_mass'''
	# Determine the fraction of the system in monomers	
	monomer_mass = np.floor(total_mass*monomer_fraction)
	#print "Monomer Mass", monomer_mass
	oligmer_mass = total_mass - monomer_mass
	#print 'oligmer Mass', oligmer_mass

	nM = len(CRS.molecule_list)
	concentrations = np.zeros((N_L, N_L, nM), dtype = int)
	m_dict = CRS.molecule_dict
	molecules = CRS.molecule_list
	new_mass = 0.0
	comp_dict = {} # Maps compositions to lists of molecules
	num_monomers = 0

	### Iterate over all molecules
	for m in molecules:
		## If it's a monomer take note
		if len(m) == 1:
			num_monomers += 1
		# Get the composition, and record which molecules are associated with that composition
		comp = get_composition(m)
		#print comp
		if comp in comp_dict.keys():
			comp_dict[comp].append(m)
		else:
			comp_dict[comp] = [m]
	#raw_input("Enter to continue, The composition of All molecules has been recorded")
	### For all compositions distribute the mass equally 
	monomers_in_seqs = [0,0]
	for comp in comp_dict.keys():
		
		nM = len(comp_dict[comp])
		frac = 1.0/float(nM)
		### If the composition was contained in the data
		if comp in mass_fraction.keys():
			comp_mass = mass_fraction[comp] # Determine the mass of that compostion
			coef = map(int, re.findall(r'\d+', comp)) # Determine the length
			l = sum(coef)
			particles_per_sequence = frac*float(oligmer_mass*comp_mass)/float(l)
			for m in comp_dict[comp]:
				## FOr each molecule with that composition
				#print m
				index = CRS.molecule_dict[m]
				concentrations[0,0, index] = int(particles_per_sequence)
				for c in range(len(coef)):
					monomers_in_seqs[c] += int(coef[c]*particles_per_sequence)
				
				new_mass += int(particles_per_sequence)*int(l)
		
	
	oligomer_mass = sum(monomers_in_seqs)
	diff = int(total_mass - oligmer_mass)
	monomers = [total_mass/2.0, total_mass/2.0]
	monomers = np.array(monomers)- np.array(monomers_in_seqs)
	
	for i in range(2):
		concentrations[0,0,i] += monomers[i]

	
	return concentrations

def generate_seq_peptides_CRS(amino_acids, max_length, kl = 0.0001, kd = 1.0, catalysts = False):

	''' Generates all possible reactions between peptide molecules up to size max_length assigns all reactions the same constant and standard prorpenisty
	Arguements:
		- amino_acids: the amino acids used in the peptides
		- max_length: the maximum length of peptides
		- kl: reaction rate constant for forward reactions
		- kd: reaction rate constant for reverse reactions, if None given, it will be assigned to be equal to kl
		- catalysts: Boolean, whether or not catalysts should be included 
	 '''
	
	import itertools
	rxn_IDs = []
	reaction_list = []
	molecule_list = []
	molecule_dict = {}
	rxn_ID = 0
	#molecule_ID = 0
	
	# If the backward constant is not specified, make it equal the forward constant
	if kd == None:
		kd = kl
	for l in range(1,max_length+1):
		# Generate all sequences of length l+1
		sequences = itertools.product(amino_acids, repeat = l)
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
				reaction_list.append( Core.Reaction(rxn_ID, reactants = reactants, reactant_coeff = reactant_coeff , products = products, product_coeff = product_coeff, constant = np.random.normal(kl, 0.05*kl), prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)
				
				# Backward Reaction
				rxn_ID = len(reaction_list)
				reaction_list.append( Core.Reaction(rxn_ID, products = reactants, product_coeff = reactant_coeff, reactants = products, reactant_coeff= reactant_coeff, constant = kd, prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)
				
	#print molecule_dict
	newCRS = Core.CRS(molecule_list = molecule_list, molecule_dict = molecule_dict, reactions = reaction_list)
	#print newCRS.molecule_dict
	

	return newCRS

def compare_distributions(target, current):
	''' Compares two different mass distributions based on their euclidean distance '''

	t = []
	c = []
	for i in current.keys():
		
		t.append(target[i])
		c.append(current[i])

	dist = 0.0
	
	for i in range(len(c)):
		dist += (c[i]- t[i])**2
	return np.sqrt(dist)

def compare_distributions_AE(target, current):
	''' Compares two different mass distributions based on their Absolute difference '''

	t = []
	c = []
	dist = 0.0
	diffs = []
	for i in current.keys():
		diffs.append ( (i, target[i]-current[i] )  )
		#if target[i] != 0.0 and current[i] != 0.0:
		dist += abs(target[i]-current[i]) 
	
	
	
	return dist

def compare_distributions_AE_targeted(target, current):
	''' Compares two different mass distributions based on their Absolute difference, weighted by the value of the target '''

	dist = 0.0
	for i in current.keys():
		#if target[i] != 0.0 and current[i] != 0.0:
		dist += target[i]*abs(target[i]-current[i]) 
		
	return dist

def mass_fraction_to_length_distribution(mass_fraction):
	'''Converts a mass fraction dictionary to a length dictionary '''
	length_dist = {}
	for comp in mass_fraction.keys():
		coef = map(int, re.findall(r'\d+', comp))
		l = sum(coef)
		if l in length_dist.keys():
			length_dist[l] += mass_fraction[comp]
		else:
			length_dist[l] = mass_fraction[comp]
	return length_dist

def plot_length_dist(length_dist):
	import matplotlib.pylab as plt
	import scipy.stats as stats
	l = []
	f = []

	max_l = max(length_dist.keys())
	for i in range(1,max_l+1):
		l.append(i)
		f.append(length_dist[i])
	(m,b, r, p, std) = stats.linregress(l,np.log(f))
	test_line = [np.exp(m*i + b) for i in l]
	plt.plot(l, f)
	plt.plot(test_line)
	#plt.yscale('log')
	print m, b
	plt.show()



def EICname_to_composition(name):
	s = re.split('-', name)
	comp = get_composition(s[0])
	return comp

def load_affinity_data_normalized(fname, max_length):
	import pandas as pd
	### Read File
	affinity = {}
	affinity_df = pd.read_csv(fname, index_col = 0)
	### Drop peptides that were never observed

	header_names = list(affinity_df)
	molecule_dict= {} ### This will map the values from the EIC data to composition codes
	molecule_names = list(affinity_df[header_names[1]])## Names of molecules from EIC data
	total_intensity = 0.0
	for index, row in affinity_df.iterrows():
		comp = EICname_to_composition(row[header_names[1]])
		coef = map(int, re.findall(r'\d+', comp))
		l = sum(coef)
		if l <= max_length:
			molecule_dict[row[header_names[1]]] = comp	
			if comp in affinity.keys():
				affinity[comp] += (row['A.RT'])
			else:
				affinity[comp] = (row['A.RT'])

			total_intensity += (row['A.RT'])
	for comp in affinity.keys():
		affinity[comp] = affinity[comp]/float(total_intensity)
	# print sum(mass_fraction.values())
	# print mass_fraction.keys()
	return affinity

def load_EIC_data_as_composition_data(fname, max_length):
	''' Load EIC data from APS system into a mass fraction dictionary
		This process contains LOTS OF ASSUMPTIONS
		ASSUMPTION LIST:
			- Hydrated/ cyclic peptides are the same as linear '''

	import pandas as pd
	mass_fraction = {}

	### Read File
	EIC_df = pd.read_csv(fname)
	### Drop peptides that were never observed
	EIC_df = EIC_df[EIC_df['EIC integral'] != 0.0]
	header_names = list(EIC_df)

	molecule_dict= {} ### This will map the values from the EIC data to composition codes
	molecule_names = list(EIC_df[header_names[0]])## Names of molecules from EIC data
	
	total_intensity = 0.0
	for index, row in EIC_df.iterrows():
		# if 'H2O' not in row[header_names[0]]:
			comp = EICname_to_composition(row[header_names[0]])
			coef = map(int, re.findall(r'\d+', comp))
			l = sum(coef)
			if l <= max_length:
				molecule_dict[row[header_names[0]]] = comp	
				if comp in mass_fraction.keys():
					mass_fraction[comp] += row['EIC integral']
				else:
					mass_fraction[comp] = row['EIC integral']

				total_intensity += row['EIC integral']
	for comp in mass_fraction.keys():
		mass_fraction[comp] = mass_fraction[comp]/float(total_intensity)
	# print sum(mass_fraction.values())
	# print mass_fraction.keys()
	return mass_fraction

def find_rxns(target, CRS):
	rIDs = []
	for t in target:
		for rxn in CRS.reactions:
			products = rxn.products
			if len(products) == 1:
				seqs = [CRS.molecule_list[p] for p in products]
				comps = [get_composition(s) for s in seqs]
				if t in comps:
					rIDs.append(rxn.ID)

	return rIDs

def update_temp(Tmax, t):
	return Tmax*(1.0 - np.sqrt(t))

def generate_flat_mass_frac(target):
	''' Generate a flat mass distribution of the same dimensions as the target '''
	flat = {}
	num_comps = len(target.keys())
	flat_value = 1.0/num_comps
	for comp in target.keys():
		flat[comp] = flat_value
	return flat


def load_integrated_EIC_heatmap(fname):
	import pandas as pd

	input_df =pd.read_csv(fname)
	header_names = list(input_df)
	(aa1, aa2, EICintensity) = (header_names[0], header_names[1], header_names[-1])
	heatmap_df =  input_df[[aa1,aa2,EICintensity]]
	#print np.array(heatmap_df[EICintensity])
	#heatmap_df[[EICintensity]] =pd.to_numeric(heatmap_df[[EICintensity]])#.astype(float)
	normalization =  sum(heatmap_df[EICintensity])
	
	aa = list(set(list(input_df[aa1] ) ))
	out_df = pd.DataFrame(index = aa, columns = aa)
	
	for index, row in heatmap_df.iterrows():
		#heatmap_df.loc[index,EICintensity] = heatmap_df.loc[index,EICintensity]/ normalization
		out_df.loc[row[aa1], row[aa2]] =  heatmap_df.loc[index,EICintensity]/ normalization
	
	return out_df

def generate_CRS_from_AA_intensities(fname, amino_acids, max_length, beta, kd= 1.0):
	import itertools
	aa_binding_df = load_integrated_EIC_heatmap(fname)
	Z = 0.0
	for a1 in amino_acids:
		for a2 in amino_acids:
			Z += np.exp(-beta*aa_binding_df.loc[a1,a2])

	rxn_IDs = []
	reaction_list = []
	molecule_list = []
	molecule_dict = {}
	rxn_ID = 0
	
	
	for l in range(1,max_length+1):
		# Generate all sequences of length l+1
		sequences = itertools.product(amino_acids, repeat = l)
		for seq in sequences:
			s = ''.join(seq)
			molecule_list.append(s)
			molecule_dict[s] = molecule_list.index(s)
			
			for i in range(1,l):
				# Forward Reaction
				rxn_ID = len(reaction_list)
				reactants = [ molecule_dict[s[:i]], molecule_dict[s[i:]] ]
				
				kl = np.exp(-beta*aa_binding_df.loc[s[i-1], s[i]])/Z
				
				reactant_coeff = [1,1]
				product_coeff = [1]
				products = [ molecule_dict[s] ]
				reaction_list.append( Core.Reaction(rxn_ID, reactants = reactants, reactant_coeff = reactant_coeff , products = products, product_coeff = product_coeff, constant = kl, prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)
				
				# Backward Reaction
				rxn_ID = len(reaction_list)
				reaction_list.append( Core.Reaction(rxn_ID, products = reactants, product_coeff = reactant_coeff, reactants = products, reactant_coeff= reactant_coeff, constant = kd, prop = 'STD') )
				#print 'Reaction List index: ', rxn_ID, 'Reaction ID: ', reaction_list[rxn_ID].ID 
				rxn_IDs.append(rxn_ID)
				
	
	newCRS = Core.CRS(molecule_list = molecule_list, molecule_dict = molecule_dict, reactions = reaction_list)
	
	return newCRS


def plot_mass_distributions(mass_fraction1, mass_fraction2):
	import matplotlib.pylab as plt
	y1 = []
	y2 = []
	lengths = []
	for k in mass_fraction1.keys():
		#print k
		coef = map(int, re.findall(r'\d+', k))
		l = sum(coef)
		lengths.append(l)
		y1.append(mass_fraction1[k])
		y2.append(mass_fraction2[k])
	x1 = zip(y1,lengths)
	x1 = sorted(x1, key=lambda tup: tup[1])
	x2 = zip(y2,lengths)
	x2 = sorted(x2, key = lambda tup: tup[1])

	y1, l = zip(*x1)
	y2, l = zip(*x2)
	# print sum(y1)
	# print sum(y2)
	plt.plot(y1, label = 'First')
	plt.plot(y2, label = 'Second')
	
	plt.legend()
	plt.show()
	plt.close()

def anneal_rate_constants(target, original_CRS, total_mass = 20000):

	### Set some parameter
	seed = 100
	evolution_time = 1.0
	repeats = 10
	random.seed(seed)
	mu = 0.1 # Fraction of vector to update each time
	epsilion = 0.0001 # scale factor in mutation noise
	num_trials = 2000

	r_seed = random.randint(0, sys.maxint)
	#### Get the target concentrations from the data
	target_concentrations = generate_concentrations_from_data(target, original_CRS, total_mass)

	target_mass_fraction = calculate_molecule_fraction_by_composition(target_concentrations, original_CRS, total_mass)
	# length_dist = mass_fraction_to_length_distribution(target_mass_fraction)
	# plot_length_dist(length_dist)
	molecules = original_CRS.molecule_list

	#### Determine reasonable Tmax by running for 10X evolution iterations
	original_constants, propensity_ints, reaction_arr, catalyst_arr = Initialize.convert_CRS_to_npArrays(original_CRS)
	original_concentrations = generate_concentrations_from_data(target, original_CRS, total_mass)
	original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr= Initialize.get_c_pointers(original_concentrations, original_constants, propensity_ints, reaction_arr, catalyst_arr)
	c_tau = _SSA_LIB.SSA_update(c_double(0.0), c_double(10*evolution_time),r_seed, c_int(1),c_int(1), c_int(len(molecules)), c_int(len(original_constants)), original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr )
	original_mass_fraction = calculate_molecule_fraction_by_composition(original_concentrations, original_CRS, total_mass)

	#plot_mass_distributions(target_mass_fraction, original_mass_fraction)
	Tmax = 1.0*compare_distributions_AE_targeted(target_mass_fraction, original_mass_fraction)
	# plot_mass_distributions(target_mass_fraction, original_mass_fraction)
	### Generate Initial Concentration File
	molecules = original_CRS.molecule_list
	T = Tmax

	for t in range(num_trials):
		start_time = time.time()
		r_seed = random.randint(0, sys.maxint)
		
		############################################################################################################################################
		################ time evolve step
		############################################################################################################################################
		### Evolve Original
		#original_ds = []
		original_constants, propensity_ints, reaction_arr, catalyst_arr = Initialize.convert_CRS_to_npArrays(original_CRS)
		#original_concentrations = generate_concentrations_from_data(target, original_CRS, total_mass)
		original_constants_dict = get_reaction_constants(original_CRS)
		#new_ds = []
		#new_concentrations = generate_concentrations_from_data(target, new_CRS, total_mass)	
		original_concentrations = generate_random_distribution(original_CRS, total_mass)
		new_concentrations = copy.deepcopy(original_concentrations)
		
		original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr= Initialize.get_c_pointers(original_concentrations, original_constants, propensity_ints, reaction_arr, catalyst_arr)
		c_tau = _SSA_LIB.SSA_update(c_double(0.0), c_double(evolution_time),r_seed, c_int(1),c_int(1), c_int(len(molecules)), c_int(len(original_constants)), original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr )
		
		#print check_mass(total_mass, original_CRS, original_concentrations)	
		original_mass_fraction = calculate_molecule_fraction_by_composition(original_concentrations, original_CRS, total_mass)
		#plot_mass_distributions(target_mass_fraction, original_mass_fraction)
		original_d= compare_distributions_AE_targeted(target_mass_fraction, original_mass_fraction)
		
		#original_ds.append(original_d)
		new_constants_dict = mutate(original_constants_dict, mu, epsilion, as_percentage = False)
		new_CRS = set_reaction_constants(original_CRS, new_constants_dict)
		new_constants, propensity_ints, reaction_arr, catalyst_arr = Initialize.convert_CRS_to_npArrays(new_CRS)
		#### Evolve new
		
		new_concentrations_ptr, new_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr= Initialize.get_c_pointers(new_concentrations, new_constants, propensity_ints, reaction_arr, catalyst_arr)
		c_tau = _SSA_LIB.SSA_update(c_double(0.0), c_double(evolution_time),r_seed, c_int(1),c_int(1), c_int(len(molecules)), c_int(len(new_constants)), new_concentrations_ptr, new_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr )
		
		new_mass_fraction = calculate_molecule_fraction_by_composition(new_concentrations, new_CRS, total_mass)
		new_d = compare_distributions_AE_targeted(target_mass_fraction, new_mass_fraction)
		#new_ds.append(new_d)

		#print new_KL
		
		############################################################################################################################################
		################ Comparison Step
		############################################################################################################################################
		D = new_d - original_d
		#Dmin = (np.mean(new_ds) - np.std(new_ds)) -(np.mean(original_ds) + np.std(original_ds)) 
		
		overlap = False
		if D  < 0.0:
			p = 1.0
		elif D == 0.0: 
			p = 0.5
		elif D > 0.0:
			p = np.exp(-D/T)
		
		print 'Current D: %.5f  Delta: %.6f  T: %.5f  P: %.2f' %(original_d, D, T, p)
		dice_roll = random.random()
		
		if dice_roll <= p:
			print 'Update Accepted'
			#plot_mass_distributions(target_mass_fraction, new_mass_fraction)
			original_CRS = set_reaction_constants(original_CRS, new_constants_dict)
		else:
			original_CRS = copy.deepcopy(original_CRS)	
		T = update_temp(Tmax, float(t)/num_trials)
		print time.time() -start_time	
	
	original_constants, propensity_ints, reaction_arr, catalyst_arr = Initialize.convert_CRS_to_npArrays(original_CRS)
	original_concentrations = generate_concentrations_from_data(target, original_CRS, total_mass)
	original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr= Initialize.get_c_pointers(original_concentrations, original_constants, propensity_ints, reaction_arr, catalyst_arr)
	c_tau = _SSA_LIB.SSA_update(c_double(0.0), c_double(evolution_time),r_seed, c_int(1),c_int(1), c_int(len(molecules)), c_int(len(original_constants)), original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr )
	original_mass_fraction = calculate_mass_fraction_by_composition(original_concentrations, original_CRS, total_mass)
		
	#plot_mass_distributions(target, original_mass_fraction)
	original_CRS.savetxt('AD_annealedCRS.txt')
	

def compare_affinity_mass(affinity, mass_fraction):
	import matplotlib.pylab as plt
	import scipy.stats as stats


	a = []
	m = []
	for comp in mass_fraction.keys():
		a.append(affinity[comp])
		m.append(mass_fraction[comp])
	slope, intercept, r_value, p_value, std_err = stats.linregress(a,m)
	print slope, p_value, r_value**2
	plt.scatter(np.log(m), np.log(a))
	plt.ylabel('log(predicted CHNOSZ)')
	plt.xlabel('log(abundace data)')
	plt.show()
	plt.close()

def get_all_EIC_comp_data():
	import pandas as pd
	amino_acids = ['A', 'D', 'E', 'G', 'H' , 'K' , 'L' , 'P' , 'T', 'V']
	acidlist= ['HCl', 'H2SO4', 'H3PO4']
	for acid in acidlist:

	
		for aa1 in amino_acids:
			for aa2 in amino_acids:

				fname = '060916_new_matrices/%s/integrated_eics_%s%s.csv' % (acid, aa1, aa2)
				if  os.path.isfile(fname):
					target =load_EIC_data_as_composition_data(fname, max_length =15)
					target_df = pd.DataFrame(target.items(), columns = ['peptides', 'abundace'])#, index = index)
					target_df.to_csv('%s_%s%s.csv' % (acid, aa1, aa2), index = False)



def check_CRS(fname, target, total_mass = 10000):
    from Parser import Parser

	evolution_iterations = 10
	CRS = Parser().parse_file(fname)
	r_seed = random.randint(0, sys.maxint)
	#### Get the target concentrations from the data
	target_concentrations = generate_concentrations_from_data(target, CRS, total_mass)
	target_mass_fraction = calculate_mass_fraction_by_composition(target_concentrations, CRS, total_mass)
	molecules = CRS.molecule_list

	#### Determine reasonable Tmax by running for 10X evolution iterations
	original_constants, propensity_ints, reaction_arr, catalyst_arr = Initialize.convert_CRS_to_npArrays(CRS)
	original_concentrations = generate_concentrations_from_data(target, CRS, total_mass)
	original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr= Initialize.get_c_pointers(original_concentrations, original_constants, propensity_ints, reaction_arr, catalyst_arr)
	c_tau = _SSA_LIB.SSA_update(c_double(0.0), c_double(-100*evolution_iterations),r_seed, c_int(1),c_int(1), c_int(len(molecules)), c_int(len(original_constants)), original_concentrations_ptr, original_constants_ptr, propensity_ints_ptr, reaction_arr_ptr, catalyst_arr_ptr )
	original_mass_fraction = calculate_mass_fraction_by_composition(original_concentrations, CRS, total_mass)

	plot_mass_distributions(target_mass_fraction, original_mass_fraction)


