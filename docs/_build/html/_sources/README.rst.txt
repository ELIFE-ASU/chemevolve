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


