import numpy as np
########################################################################################
def output_concentrations(concentrations, prefix, time = None):
	import pickle
	'''Outputs an .dat file

	Arguements:
		- concentrations: a numpy array which contains the concentrations of all molecules indexed by (position, molecule)
		- prefix: a string which will be the prefix to the saved file
		- time (optional): number which will be inserted into the file name '''
	fname = prefix + '_ts.dat'
	if time != None:
		fname =  prefix + '_ts_'+ str(time)+'.dat'
	#np.save(fname, concentrations)
	outfile1 = open(fname, 'w+b')
	pickle.dump(concentrations.tolist(), outfile1)
	outfile1.close()
########################################################################################
def tidy_timeseries(molecules,prefix, delete_dat = True):
	
	''' This function replaces the seperate time-series .dat files with a tidy dataframe containing all the time series data 

	Arguements:
		- prefix: string which is the prefix used to save the time-series data files
		- delete_dat (optional): if False the .npy files will be saved, otherwise they will be deleted, default: True
		'''
	import pandas as pd 
	import glob
	import pickle
	import os

	# Get the moleucles list 
	# with open(prefix+ '_molecules.txt', 'rb') as f:
	# 	molecules = pickle.load(f)
	num_molecules = len(molecules)

	# Initialize the tidy dataframe
	features = ['time', 'position', 'molecule', 'abundance']
	
	# Get all the time series files
	ts_prefix = prefix + '_ts_' 
	
	fnames = glob.glob(ts_prefix+'*.dat')
	#print fnames
	index = 0
	tidy_df_dict = {}
	# Get all the data
	for f in fnames:
		#print f
		infile1 = open(f, 'r+b')
		file1 = pickle.load(infile1) # This is a list
		infile1.close()
		concentrations = np.array(file1)
		t =f.replace('.dat', '')
		#print t
		t =t.replace(ts_prefix, '')
		# The time value is embedded in the filename

		time = float(t)
		# Initialize a dummy lattice to make iteration over the indices of the concentration array easier
		lattice_size = np.product(concentrations.shape[:-1])
		lattice_shape = concentrations.shape[:-1]
		dummy_arr = np.zeros(lattice_size).reshape(lattice_shape)
		# Iterate over the dummy array, use only index information
		for position_index, dummy_site in np.ndenumerate(dummy_arr):
			position_index = tuple([int(i) for i in position_index])
			positions = [position_index]*len(molecules)
			times = [time]*len(molecules)
			observations = zip(times, positions, molecules, concentrations[position_index].tolist())
			for m in range(num_molecules):
				
				observation = list(observations[m])
				tidy_df_dict[index] = observation
				index +=1	
				#print observation
				#raw_input("Enter")
		if delete_dat:
			# Delete the File when we're done with it
			os.remove(f)
	tidy_df = pd.DataFrame.from_dict(tidy_df_dict, orient = 'index')
	tidy_df.columns = features
	# Name the dataframe and save it
	df_name = prefix + '_time_series_df.csv'
	tidy_df.to_csv(df_name, index_label = False) # index label = False is better for importing to R
	
########################################################################################
def generate_ts_df(infile, outname):

	# Load Tidy Data File
	tidy_df = pd.read_csv(infile)

	# Get the times
	times = tidy_df['time'].unique()
	# Get Molecules
	molecules  = tidy_df['molecule'].unique()

	timeseries_df  = pd.DataFrame(index = molecules, columns = times)
	#print timeseries_df
		
	#For each time, construct a new entry in the time series df
	for t in times:
		t_df = tidy_df[tidy_df.time == t].filter(items = ['abundance'])
		t_df = t_df.set_index(molecules)
		#print t_df
		timeseries_df[t] = t_df
	# print timeseries_df
	# raw_input("Enter")
	timeseries_df.to_csv(outname)
