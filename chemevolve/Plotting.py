import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import seaborn as sns

def plot_length_distribution(filename, savename = None):
	'''Plots the time averaged length distribution of molecules in the entire system. Shows plot unless a savename is specified '''
	ts_df = pd.read_csv(filename)

	static_df = ts_df.filter(items = ['molecule', 'abundance'])

	lengths_lists = [list() for x in range(0,7)]
	
	for index, row in static_df.iterrows():
		lengths_lists[len(row['molecule'])].append(float(row['abundance']))

	length_averages = [0.0 for x in range(0,7)]
	length_var = [0.0 for x in range(0,7)]
	for l in range(1,7):
		length_averages[l] = np.mean(lengths_lists[l])
		length_var[l] = np.std(lengths_lists[l])


	plt.bar( [x for x in range(1,7)]   ,length_averages[1:], yerr = length_var[1:])
	plt.ylabel('Molecule Count')
	plt.xlabel('Molecule Size/Length')
	plt.title('Time averaged length abundances')
	plt.ylim(ymin=0)
	if savename != None:
		plt.savefig(savename)
	else:
		plt.show()
	plt.close()


def plot_molecule_distribution(filename, savename = None):
	'''Plots the time averaged molecule distribution of molecules in the entire system. Shows plot unless a savename is specified '''
	ts_df = pd.read_csv(filename)
	max_length = 0
	static_df = ts_df.filter(items = ['molecule', 'abundance'])

	molecules = list(static_df['molecule'].unique() )
	reduced_molecules = [m for m in molecules if len(m) <= 4]
	molecules = reduced_molecules
	
	molecule_dict = dict()
	for m in molecules:
		molecule_dict[m] = list()
		if len(m) > max_length:
			max_length = len(m)
	nM = len(molecules)
	
	color_palette = sns.color_palette("husl", max_length)
	for index, row in static_df.iterrows():
		if row['molecule'] in molecules:
			lm = len(row['molecule'])
			molecule_dict[row['molecule']].append(float(lm*row['abundance']))

	molecule_abundances = [0.0 for x in range(0,nM)]
	molecule_std = [0.0 for x in range(nM)]
	colors = [None for x in range(nM)]
	labels = [None for x in range(nM)]
	lengths = [None for x in range(nM)]
	for i in range(nM):
		m = molecules[i]
		colors[i] = color_palette[len(m)-1]
		molecule_abundances[i] = np.mean(molecule_dict[m])
		molecule_std[i] = np.std(molecule_dict[m])
		labels[i] = "length %i"  %len(m)
		lengths[i] = len(m)
	current_x = 0
	
	for i in range(1,max_length+1):
		indices_used = []
		for j in range(nM):
			if lengths[j] == i:
				indices_used.append(j)
		current_molecules = [molecule_abundances[m] for m in indices_used]
		current_std  = [molecule_std[m] for m in indices_used]
		label = "length %i" % i
		plt.bar( [x for x in range(current_x, current_x +len(indices_used))]   ,current_molecules, yerr = current_std, color = color_palette[(i-1)], ecolor= color_palette[(i-1)], label= label)
		current_x += len(indices_used)
	
	plt.legend(fontsize = 40)

	ax = plt.gca()
	ax.set_ylim(ymin=0)
	ax.set_ylabel('Molecule Count', fontsize  = 30, position = (-0.2, 0.5))
	#ax.tick_params(axis='both', which='major', pad=)
	plt.xticks([x for x in range(current_x)], molecules, rotation = 'vertical', fontsize = 30)
	plt.yticks(fontsize = 20)
	ax.xaxis.set_ticks([x + 0.35 for x in range(0, nM)])
	
	fig = plt.gcf()
	fig.set_size_inches(18, 18)
	plt.title('Molecule Distribution', fontsize = 50)
	if savename != None:
		plt.savefig(savename)
	else:
		plt.show()
	plt.close()

def plot_time_series(filename, print_molcules, savename = None):
	'''Plot the time series of molecule names in print_molcules, if savename provide figure will be saved '''
	
	import random
	color_palette = sns.color_palette("husl", len(print_molcules))
	colorindex = [x for x in range(len(print_molcules))]
	generate_ts_df(filename, 'temp_TS.csv')
	ts_df = pd.read_csv('temp_TS.csv', index_col = 0)
	ts_df = ts_df.T
	
	for i in range(len(print_molcules)):
		m = print_molcules[i]
		abundances = list(ts_df[m])
		
		#mass_fraction = [float(x)/10000 for x in abundances]
		time = list(np.array(ts_df.index.values, dtype = float))
		z = zip(abundances, time)
		z = sorted(z, key = lambda x: x[1])
		abundances, time = zip(*z)
		[ci1]  = random.sample(colorindex,1)
		colorindex.remove(ci1)
		plt.plot(time, abundances, color = color_palette[ci1])
	# plt.xticks(fontsize = 30)
	# plt.yticks(fontsize = 30)
	# # plt.ylabel('Mass Fraction', fontsize = 30)
	# # plt.xlabel('Time', fontsize = 30)
	# fig = plt.gcf()
	# fig.set_size_inches(18, 18)
	plt.legend(print_molcules)
	plt.xlabel('Time')
	plt.ylabel('abundances')
	#[ymin, ymax] = plt.ylim()
	plt.ylim(ymin = 0.0)
	if savename != None:
		plt.savefig(savename)
	else:
		plt.show()
	plt.close()
	
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
