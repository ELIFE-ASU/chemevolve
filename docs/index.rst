======================================
ChemEvolve
======================================
ChemEvolve is a Python package which provides a suite of chemical evolution tools. ChemEvolve is designed to allow for the rapid development and exploration of a chemical reaction systems with standardized input and outputs. CoreEvolve (currently) utilizes the `Simplified Stochastic or Gillispie Algorithm <https://en.wikipedia.org/wiki/Gillespie_algorithm>`_ to exactly simulate chemical systems.  

ChemEvolve provides a standard format to specify chemical reaction systems (including the rate constants, catalytic effects, and a choice of propensity functions). It also allows users to simulate these reaction systems in spatially explicit models (e.g. solve Reaction-Diffusion Equations). All ouptut files are saved in `Tidy Data <http://vita.had.co.nz/papers/tidy-data.pdf>`_  format, to allow for easy plotting using standard data visualization tools ( e.g. `Seaborn <http://seaborn.pydata.org/>`_ , or `R <https://www.r-project.org/>`_ )

Requirements
------------
ChemEvolve requires Python 2.7.x, with `NumPy <http://www.numpy.org/>`_, `pandas <http://pandas.pydata.org/>`_, and both `matplotlib <https://matplotlib.org/>`_ and  `Seaborn <http://seaborn.pydata.org/>`_ for plotting and visualization. 


Installation
--------------
To install, first download and install the package using pip, 


      .. code-block:: bash 

         $ pip install chemevolve   

Then just throw this import line into the top of your python script:

   .. code-block:: python
   
      import chemevolve as ce

That's it! You should be good to go!


Tutorial
------------
This tutorial is intended to provide some basic instruction for using ChemEvolve to evaluate Chemical Reaction Systems. For clarity this tutorial is seperated into three sections: 1) setting up a chemical reaction system, 2) specifying some initial conditions, 3) time evolving the system, and 4) plotting the output. 


   1) Setting up a chemical reaction system (CRS)

      This is the most conceptually important part of using ChemEvolve. Setting up the CRS involves specifying the molecules which can exist in the system as well as the reactions the molecules are involved in. Each molecule must be given an ID numer (which is just an integer), as well as a name (which is a string). Each reaction must be assigned a set of reactants, reactant coefficients, products, product coefficients, a rate constant, any catalysts, and a propensity function. 

      ChemEvolve has three important objects: Reactions, which contain information about an individual chemical reaction, and CRS which contain lists of reactions as well as information about the molecules involved in those reactions, and an array which contains the abundance of each molecule. First lets think about Reaction and CRS objects.

      As an illustrative example, let's consider a system where all the molcules are made up of strings of As and Bs. Let's consider all possible strings of As and Bs up to length 6. Let's say all strings can form by concatenating smaller strings, and all strings can fragment at any location. Let's say that the concatenation reactions happen with a propensity proportional to :math:`k_l [x_i][x_j]`, where :math:`[x_i]` is the concentration of one of the reactants and :math:`k_l` is the rate constant associated with concatanation reactions. We can also say that dissocation reactions happen with a propensity proportional to :math:`k_d [x_i]`, where :math:`k_d` is now the rate constant associated with dissocation reactions. For simplicity let's assume that :math:`k_d`, is the same for all molecules, and :math:`k_l` is the same for all assoication reactions. 

      How do we make this reaction system? Luckily ChemEvolve has a function to do it for us! It's called :code:`generate_all_binary_reactions`.You can check out the details of the function if you want, but using it is fairly simple, it's under the :code:`BinaryPolyer` module, so we'll import that. The propensities described above are what ChemEvolve considers 'standard' propensity functions, e.g. the reaction propensity depends linearly on the reactants involved and needs only one postive real valued rate constant. So for our example, let's assume :math:`k_l = 0.001`, and :math:`k_d = 1.0`. Then generating a CRS for this system is as easy as 

      .. code-block:: python 

         import chemevolve as ce
         from chemevolve import BinaryPolymer as BinPoly
         max_length = 6 # Maximum Length of binary polymers
         k_l = 0.001 # Forward (ligation) Reaction Rate constant
         k_d = 1.0   # Backward (degradation) Reaction Rate constant
         CRS = BinPoly.generate_all_binary_reactions(max_length, fconstant = k_l, bconstant = k_d)



   2) Specifying initial conditions 

      Once you've generated a CRS (either from a file or a function), you'll need to specify the initial concentrations of molecules. ChemEvolve stores abundance information in a 3D array. The first two indicies are used to indicate spatial positions, x and y. The third index specifies the molecule of interest. For now, let's just consider a well mixed system, so that all molecules are located in the same position. It makes sense to call the array storing concentration information, :code:`concentrations`, but you could make it something different if you wanted. 


      .. code-block:: python 

         N_L = 1 # Size of the lattice (diffusion not yet implemented, fix at 1)
         total_mass = 10000
         num_molecules = len(CRS.molecule_list)
         # Initialize array
         concentrations = np.zeros( (N_L, N_L, num_molecules), dtype = np.float64 ).

      We'll assume that we start with an equal abundance of monomers in the system and nothing else. Since this is a binary polymer model, there's only two monomer types and they'll always be stored in the first two indices of the molecule list. However, we can always find the indices of a molecule, from the :code:`molecule_dict` dictionary assoicated with the CRS. To find the indices of the monomers and the initial conditions to be half of the total mass we'll do

      .. code-block:: python 

         Aindex = CRS.molecule_dict['A']
         Bindex = CRS.molecule_dict['B']
         # Set monomer values
         concentrations[0,0,Aindex] = total_mass/2.0
         concentrations[0,0,Bindex] = total_mass/2.0.

      Remember, even though we don't have any spatial extant in this model, we need to index the position, which is :code:`x= 0, y = 0`.

   3) Time Evolving and Outputting Data

      Now that we've got the :code:`CRS` and the initial conditions set, we can time evolve the system using the Gillispie Algorithm! To do this we'll use a function called :code:`SSA_evolve`. In order to use this functions, we'll need to know who long we want the system to evolve for, the simulation will run between times :code:`tau` and :code:`tau_max`. We'll also need to set the random number generator seed, this is important for making sure different realizations of the time evolution are actually different. Even though the Gillispie Algorithm is stochasitic, it's powered by pseudo random number generators and we should make sure they are seeded differently, which is why you have to provide it to :code:`SSA_evolve`. If we just want to update the :code:`concentrations` array due to the time evolution, that's all we'll need. However, if we want :code:`SSA_evolve` to output time series data (and who wouldn't want that!?) we'll need to provide it with two more parameters, a string called :code:`output_prefix`:, and a float called :code:`t_out`. The string tells :code:`SSA_evolve` where to save our data and what to call it, your time series data will be saved as: :code:`output_prefix+ '_time_series_df.csv'`, so you can include any path or naming scheme you want. :code:`t_out` specifies how frequently the data should be output. Keep in mind due to the stochastic nature of the Gillispie Algorithm you'll only output data approximately that frequently. Here's an example of using this all together. 

      .. code-block:: python 

         ### Time Evolve
         tau = 0.0 # Set current time
         tau_max = 1.0 # Total Integration Interval
         t_output = 0.1 # How frequently should data be output
         freq_counter = 0.0 # Counts which output is coming next
         rand_seed = 1337 # Seed for random number generator
         output_prefix = 'tutorial_data' # This is a string that will procceed all file names assoicated with the outputs of this simulation
         concentrations = ce.SSA_evolve(tau, tau_max, concentrations, CRS, rand_seed, output_prefix = output_prefix, t_out = t_output)

      During the computation :code:`SSA_evolve` will save temporary files in your directory, when it is done with the time evolution it will automatically save your data in the file 'tutorial_data_time_series_df.csv', since we provided it with the output prefix 'tutorial_data'. 


   4) Plotting the output

      All the outputs of ChemEvolve come in Tidy Data formats. This is done after the simulation is completed, so if you termiated the computation early the data will not be in the correct format. ChemEvolve has a few functions built in to plot the data, including looking at the molecule distribution, length distribution, and the time series of particular molcules. They are included in the :code:`Plotting module`. Here's an example of plotting the length distribution, then the molecule distribution, and then the time series abundance of the monomers:

      .. code-block:: python

         from chemevolve import Plotting as Plots
         Plots.plot_length_distribution(output_prefix + '_time_series_df.csv')
         Plots.plot_molecule_distribution(output_prefix + '_time_series_df.csv')
         Plots.plot_time_series(output_prefix + '_time_series_df.csv', ['A', 'B'])




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. automodule:: InitializeFunctions
   :members:
.. automodule:: ReactionFunctions
   :members:
.. automodule:: PropensityFunctions
   :members:
.. automodule:: OutputFunctions
   :members:
.. automodule:: CoreClasses
   :members:
.. automodule:: Plotting
   :members:
.. automodule:: BinaryPolymer
   :members:


-------------
Grant Support
-------------
This project is supported in part by a grant provided by the Templeton World Charity Foundation as part of the `Power Of Information Initiative <http://www.templetonworldcharity.org/what-we-fund/themes-of-interest/power-of-information>`_.
