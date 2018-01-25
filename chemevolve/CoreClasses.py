# class definitions for CoreEvolve
from collections import deque, Counter
from copy import copy,deepcopy
import random
        
## Reaction Class        
class Reaction(object):
    '''Reaction object containing an ID and reaction members (IDs not strings) as well as reaction coefficients and rate constants
    reactants, and products lists should contain integers which are the IDs of the reactant molecules and the product molecules
    reactant_coeff and product_coeff contain ints which are the reaction coefficients. The indices must match the corresponding 
    ID lists

    Attributes:
        - ID: unique int which indentifies the reaction
        - reactants: a list of molecule IDs which stores the reactants
        - reactant_coeff: a list of integers which contains the reactant coefficients  (if reactant_coeff is not provided all reactants are assumed to have coefficients of 1)
        - products: a list of molecule IDs which stores the products
        - product_coeff: a list of integers which contains the product_coeff coefficients
        - constant: a floating point number, the reaction rate constant 
        - catalysts: a list of molecule IDs which specify which molecules catalyze this reaction
        - catalyzed_constants: a list of floating point numbers giving the catalytic effect of each molecule

    '''
    def __init__(self, ID, reactants=list(), reactant_coeff = list(), products=list(), product_coeff = list(), constant=1.0, catalysts=list(), catalyzed_constants=list(), prop = str()):
        #initialise reaction 
        # if reactant_coeff == None:
        #     reactant_coeff = [1]*len(reactants)
        # if product_coeff == None:
        #     product_coeff = [1]*len(products)
         
        # Sort of all molecule lists       
        react_tuples = zip(reactants, reactant_coeff)
        prod_tuples = zip(products, product_coeff)
        
        react_tuples = sorted(react_tuples, key=lambda x: x[0])
        prod_tuples = sorted(prod_tuples, key = lambda x: x[0])
        
        reactants, reactant_coeff = zip(*react_tuples)
        products, product_coeff = zip(*prod_tuples)
        
        reactants = list(reactants)
        products = list(products)
        reactant_coeff = list(reactant_coeff)
        product_coeff = list(product_coeff)

        # If the reaction is catalyzed, do the same for the catalysts
        if len(catalysts) != 0:
            cat_tuples = zip(catalysts, catalyzed_constants)
            cat_tuples = sorted(cat_tuples, key = lambda x: x[0])
            catalysts, catalyzed_constants = zip(*cat_tuples)
            catalysts = list(catalysts)
            catalyzed_constants = list(catalyzed_constants)

        # Find duplicates 
        if len(reactants) > 1:
            i =0 
            while (i < len(reactants)-1):
                if reactants[i] == reactants[i+1]:
                    reactant_coeff[i] += reactant_coeff[i+1]
                    del reactant_coeff[i+1]
                    del reactants[i+1]
                else:
                    i += 1
                if len(reactants) == 1:
                    break
        if len(products) > 1:
            i =0 
            while (i< len(products)-1):
                if products[i] == products[i+1]:
                    product_coeff[i] += product_coeff[i+1]
                    del product_coeff[i+1]
                    del products[i+1]
                else:
                    i += 1
                if len(products) == 1:
                    break
        if len(catalysts) > 1:
            i =0 
            while (i< len(catalysts)-1):
                if catalysts[i] == catalysts[i+1]:
                    del catalyzed_constants[i+1]
                    del catalysts[i+1]
                else:
                    i += 1
                if len(catalysts) == 1:
                    break
    
        self.ID = ID
        self.reactants = reactants # List of reactant IDs
        self.reactant_coeff = reactant_coeff # List of reactant stochiometric coefficients
        self.products = products # List of Product IDs
        self.product_coeff = product_coeff # List of product stochiometric coefficients  
        self.catalysts = catalysts # List of catalysts for the reaction
        self.constant = constant
        self.catalyzed_constants = catalyzed_constants
        self.prop = prop #Propensity Str to indicate function 
        
    def __str__(self):
        #returns unique reaction string (without catalysts)
        rep = ''
        # Add reactants
        for i in range(len(self.reactants)):
            rep +=  str(self.reactant_coeff[i]) + '[' + str(self.reactants[i]) + '] + '
        rep = rep[:-2]
        rep += '-- ' + str(self.constant) +' -> '
        # Add products
        for i in range(len(self.products)):
            rep += str(self.product_coeff[i]) + '[' + str(self.products[i]) + '] + '
        rep = rep[:-2]
        return rep

    def __eq__(self, other):
        '''
        Compare two reactions for equality up to reordering of reactants,
        products and catalysts.
        '''
        return self.ID == other.ID and \
            abs(self.constant - other.constant) < 1e-6 and \
            self.prop == other.prop and \
            set(self.catalysts) == set(other.catalysts) and \
            set(self.catalyzed_constants) == set(other.catalyzed_constants) and \
            set(self.reactants) == set(other.reactants) and \
            set(self.reactant_coeff) == set(other.reactant_coeff) and \
            set(self.products) == set(other.products) and \
            set(self.product_coeff) == set(other.product_coeff)
        
## Reaction System Class     
class CRS(object):
    """ A chemical reaction system comprising a list of molecules, and allowed reactions
    molecule_list contains strings, indexing molecules by their ID
    molecule_dict maps molecule strings to IDs (indices)
    reactions contains a list of reaction objects

    Attributes:
            - molecule_list: a list of molecule strings, indexed by their ID (which is an int)
            - molecule_dict: a dictionary that maps molecule strings to IDs 
            - reactions: a list of all reaction objects allowed in the Reaction System, indexed by their ID
    """
    #molecules and reactions are implemented as sets.
    def __init__(self, molecule_list=list(), molecule_dict = dict(), reactions=list()):
        self.molecule_list = molecule_list #list of molecules indexed by ID| molecule_list[ID] = m
        self.molecule_dict = molecule_dict # Maps molecule strings to IDs| {'string': ID}
        self.reactions = reactions #List of reactions to iterate over 
       
        
    # def __str__(self):
    #     rep = "Reaction set containing:\n"
    #     for r in self.reaction_dict:
    #         rep += self.reaction_dict[r].__str__()+"\n"
    #     return rep

    def __eq__(self, other):
        '''
        Compare two CRS objects for ordered equality, i.e. the molecule lists
        and reaction lists must have the same values in the same order.
        '''
        return self.molecule_list == other.molecule_list and \
               self.reactions == other.reactions
        
    def savetxt(self, file_name):
        """Writes CRS to textfile"""
        #open text file and write header
        text_file = open(file_name, "w")
        text_file.write("<meta-data>\n")
        text_file.write("nrMolecules = "+str(len(self.molecule_list))+"\n")
        text_file.write("nrReactions = "+str(len(self.reactions))+"\n\n<molecules>\n")
        #write molecule entries
        for ID,molecule in enumerate(self.molecule_list):
            #print ID, molecule
            text_file.write("["+str(ID)+"] "+str(molecule)+"\n")
        
        #write reactions
        text_file.write("\n<reactions>\n")

        for rxn in self.reactions:
            line = "["+str(rxn.ID)+"] "

            num_reactants = len(rxn.reactants)
            num_products = len(rxn.products)
            # Write Reactants
            for i in range(num_reactants): 
                molecule = self.molecule_list[rxn.reactants[i]]
                line += str(rxn.reactant_coeff[i]) + '['+str(molecule) + '] + '
            line = line[:-2]
            # Write Constant
            line += '-- ' + str(rxn.constant) + ' -> '
            # Write Products
            for i in range(num_products):
                molecule = self.molecule_list[rxn.products[i]]
                line += str(rxn.product_coeff[i]) + '['+str(molecule) + '] + '
            line = line[:-2]
            # Write Propensity
            line += ' ' + rxn.prop + ' '
            # Write catalysts
            if rxn.catalysts != []:
                num_catalysts = len(rxn.catalysts)
                line += ' ('
                for i in range(num_catalysts):
                    molecule = self.molecule_list[rxn.catalysts[i]]
                    line += str(rxn.catalyzed_constants[i]) +'[' + str(molecule) +']' + ','
                line = line[:-1]
                line += ')'
            line += '\n'
            text_file.write(line)

        text_file.close()
        
    def readtxt(self, file_name):
        """Reads from text file. The current data is discarded."""
        def read_m(s):
            #subfunction to read molecule entry
            s = s.replace('\n', '')
            s = s.split(' ')
            IDstr = s[0]
            IDstr = IDstr[:-1]
            IDstr = IDstr[1:]
            ID = int(IDstr)
            m = s[-1]
            return ID, m

        def read_r(s):
            #subfunction to read reaction entry

            # Initialize lists
            reactants = []
            reactant_coeff = []
            products = []
            product_coeff = []
            catalysts = []
            catalyzed_constants = []
            constant = None

            # Clear some newlines split by whitespace
            s = s.strip('\n')
            s = s.rstrip()
            s = s.split(' ')
            #print s
            # The first element contains the reaction ID
            IDstr = s[0]
            s.remove(IDstr)
            IDstr = IDstr[:-1]
            IDstr = IDstr[1:]
            ID = int(IDstr)
            #print ID
            
            # Seperate everything else into reactants or product-propensity-catalysts
            split_r = s.index('--')
            split_psc = s.index('->')
            constant = float(s[split_r+1])
            r = s[:split_r]

            psc = s[split_psc+1:]
            #print "Reactants: ", r
            #print "product-catalysts: ", psc
            # Get the reactants and their coefficients
            for item in r:
                if item != '+':
                    coef, molecule = item.split('[')
                    molecule = molecule[:-1]
                    reactants.append(molecule)
                    reactant_coeff.append(int(coef))

            # Get the catalyst IDs
            catStr = psc[-1]
            #print catStr
            if '(' in catStr and ')' in catStr: 
                cats = catStr.split(',')
                #print cats
                for c in cats:
                    c = c.strip('(')
                    c = c.strip(')')
                    const, molecule = c.split('[')
                    molecule = molecule[:-1]
                    catalysts.append(molecule)
                    catalyzed_constants.append(float(const))
                #print 'Catalysts: ', catalysts, ' Constants: ', catalyzed_constants
                del psc[-1]
                del psc[-1]
               
            # Get the propensity string
            propStr = psc[-1]
            #print propStr
            del psc[-1]
            del psc[-1]
            #print psc
            # Get the products and their coefficients
            for item in psc:

                if item != '+' and item != ' ':
                    #print item
                    coef, molecule = item.split('[')
                    molecule = molecule[:-1]
                    products.append(molecule)
                    product_coeff.append(int(coef))
            #print ID, constant, reactants, reactant_coeff, products, product_coeff, catalyzed_constants, catalysts
            #raw_input("Enter")         
            return ID, constant, reactants, reactant_coeff, products, product_coeff, catalysts, catalyzed_constants, propStr

        #open text file and read in all lines    
        text_file = open(file_name, "r")
        l = text_file.readlines()
        text_file.close()
        
        #use deque instead of list because we are looking at the first element
        l = deque(l)
        #print l.popleft()
        #check and read header
        if l.popleft() == "<meta-data>\n":
            s=l.popleft()
            num_M=s[s.rfind(' '):len(s)-1]
            s=l.popleft()
            num_R=s[s.rfind(' '):len(s)-1]
            l.popleft()
            l.popleft()
            
            m_list = [None]*int(num_M) # This maps molecule IDs to molecule objects
            r_list = [None]*int(num_R) # This maps reaction IDs to reaction objects
            m_dict = dict() # This maps molecule strings to IDs
            #read molecules
            for i in range(int(num_M)):
                ID, m=read_m(l.popleft() )
                m_list[ID] =  m
                #print "Molecule: ", m, 'ID: ', ID
                m_dict[m] = ID
            l.popleft()
            l.popleft()
             
            #read reactions
            for i in range(int(num_R)):
                # Read Line
                rID, rconstant, reactant_molecules, reactant_coeff, product_molecules, product_coeff, catalyst_molecules, catalyzed_constants, propStr = read_r(l.popleft() )
                
                # Convert molecule strings to IDs
                reactant_IDs = []
                product_IDs = []
                catalyst_IDs = []
                # Get reactant IDs
                for r in reactant_molecules:
                    reactant_IDs.append(m_dict[r])
                # Get Product IDs
                for p in product_molecules:
                    product_IDs.append(m_dict[p])
                # Get Catalyst IDs
                for c in catalyst_molecules:
                    catalyst_IDs.append(m_dict[c])
                #print rID, rconstant, reactant_molecules, reactant_coeff, product_molecules, product_coeff, catalyst_molecules, catalyzed_constants, propStr
                r_list[rID] = Reaction(rID, constant= rconstant, reactants = reactant_IDs, reactant_coeff = reactant_coeff, products = product_IDs, product_coeff = product_coeff, catalysts = catalyst_IDs, catalyzed_constants = catalyzed_constants, prop = propStr)
                # print r_list[rID].catalysts
                # raw_input("Enter")
                # print 'Reactants: ', reactant_molecules,'Reactant IDs: ', reactant_IDs, ' Coefficients: ', reactant_coeff
                # print 'Products: ', product_molecules, 'Product IDs: ', product_IDs, ' Coefficients: ', product_coeff
                # print 'Catalysts: ', catalyst_IDs
            self.reactions = r_list
            self.molecule_dict = m_dict
            self.molecule_list = m_list
            #self.update_molecules()
        else:
            
            print("invalid file")
