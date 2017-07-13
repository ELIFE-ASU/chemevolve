#include <math.h>
#include <stdio.h>
#include <stdlib.h>
//#include "SSA.h"

#define INDEX3(L,M,N, i,j,k) ((N) * ((M) * (i) + (j)) + (k))
#define INDEX2(L,M, i,j) ( ((M) * (i)) + (j) )

unsigned long long choose(unsigned long long n, unsigned long long k) {
    if (k > n) {
        return 0;
    }
    unsigned long long r = 1;
    for (unsigned long long d = 1; d <= k; ++d) {
        r *= n--;
        r /= d;
    }
    return r;
}

double r2()
{  
    double a = 0.0;
    while (a == 0.0 || a == 1.0) a = (double)rand() * (1.0 / (double)RAND_MAX);
    return a;
}

double SSA_update(double current_t, double  next_t, int const r_seed, const int max_x, const int max_y, const int num_molecules, const int num_reactions, double *concentrations, const double  *reaction_constants, const int  *rxn_props, const int  *reaction_arr, const double  *catalyst_arr){
	double current_Ap = 0.0;
	double cat_enhance = 0.0;
	double* Ap_arr = malloc(max_x*max_y * sizeof(double));
	double Ap_tot = 0.0;
	double checkpoint = 0.0; 
	double dice_roll = 0.0;
	int x;
	int y;
	int r;
	int m;
	int picked_x;
	int picked_y;
	int picked_r;
	double tau_step;

	int evolve = 1;
	int time_evolve = 1;
	int rxn_count = 0;

	if (next_t < current_t){
		//printf("Next time is less than current time, assuming next is a number of reactions\n");
		time_evolve = 0;
		next_t = abs(next_t);
	}
	srand(r_seed);
	// Initialize Random Number generator
	
	/* ########  Initialize Propensities ######## */
	// Iterate over all lattice sites and all reactions at each site
	//printf("Begin Initialize Propensities \n");
  	for (x = 0; x< max_x; ++x){
  		for ( y = 0; y<max_y; ++y){
  			Ap_arr[INDEX2(max_x, max_y, x,y)] = 0.0;
  			//printf("%f \n", current_Ap);
  			for ( r = 0; r< num_reactions; ++r){
  				current_Ap =reaction_constants[r];
  				cat_enhance = 0.0;
  				// 0 corresponds to Standard propensity
  				// printf("Current Reaction %d \n", r);
  				if (rxn_props[r] == 0) {
  					// The reaction has a standard propensity 

  					for ( m = 0; m< num_molecules; ++m){
  						//printf("Molecule %d coefficient %d \n", m, -reaction_arr[INDEX2(num_reactions, num_molecules,r,m)]);
  						// See if molecule is a reactant
  						if (reaction_arr[INDEX2(num_reactions, num_molecules,r,m)] < 0){
  							// If molecule is a reactant add concentration^coefficient to current_Ap
  							current_Ap =  current_Ap*pow(concentrations[INDEX3(max_x, max_y, num_molecules,x,y,m)], -reaction_arr[INDEX2(num_reactions, num_molecules,r,m)]);
  						} 
  						if (catalyst_arr[INDEX2(num_reactions, num_molecules,r,m)]> 0){
  							// If the molcule is a catalsyt, include its effect
  							//printf("Molecule %d catayltic Effect %f \n", m, catalyst_arr[INDEX2(num_reactions, num_molecules,r,m)]);
  						
  							cat_enhance += catalyst_arr[INDEX2(num_reactions, num_molecules,r,m)]*concentrations[INDEX3(max_x, max_y, num_molecules,x,y,m)];
  						}
  					}
  					// printf("Cat Enhance is %f \n", cat_enhance);
  					current_Ap = current_Ap*(1.0 + cat_enhance);
  					

  				}

  		// 		else if (propensity_function == 'RCM'){ //Only works for binary sequences
				// 	int nA = -reaction_arr[r][0];
				// 	double num_A = concentrations[x][y][0];
				// 	int nB = -reaction_arr[r][1];
				// 	double num_B = concentrations[x][y][1];
				// 	for (int m = 0; m< num_molecules; ++m ){
				// 		if (reaction_arr[r][m] > 0){
				// 			double num_replicator = concentrations[x][y][m];
				// 		}
				// 	}
				// 	checkpoint += replicator_composition_propensity_envMutation(constant, mu, num_replicator, num_A, num_B, nA, nB);
			
				// }


  				Ap_arr[INDEX2(max_x, max_y, x,y)] += current_Ap;
  				//printf("%f \n", current_Ap);
  				Ap_tot += current_Ap;

  			}
  		}
  	}
  	//printf("Done with Initialize \n");
	
		
	/* ######## Main Loop ######## */ 
	while (evolve == 1){

		// Pick Reaction //
		// Pick the Lattice site first
		//printf("Pick Reaction \n");
		dice_roll = Ap_tot*r2();
		checkpoint = 0.0;
		//printf("Total Propensity is %f \n", Ap_tot);
		//printf("Dice Roll is %f \n", dice_roll);
		for ( x = 0; x < max_x; ++x){
			//printf("Current x is %d \n",x );
			if (checkpoint >= dice_roll) {
				break;
			}
			for ( y = 0; y <max_y; ++y){
				//printf("Current y is %d \n",x );
				checkpoint += Ap_arr[INDEX2(max_x, max_y, x,y)];
				if (checkpoint >= dice_roll) {
					picked_x = x;
					picked_y = y;
					break;
				}
			}
		}
		//printf("Picked x and y are (%d, %d) \n",picked_x, picked_y );
		// Decide the reaction at that lattice site
		dice_roll = Ap_arr[INDEX2(max_x, max_y, picked_x,picked_y)]*r2();
		checkpoint = 0.0;
		//printf("Total Propensity is %f \n", Ap_arr[INDEX2(max_x, max_y, picked_x,picked_y)]);
		//printf("Dice Roll is %f \n", dice_roll);
		//printf("Picking Reaction \n");
		for ( r = 0; r < num_reactions; ++r){
			//printf("Current reaction is %d \n", r );
			current_Ap =reaction_constants[r];
  			cat_enhance = 0.0;
  			if (rxn_props[r] == 0){
  				// The reaction has a standard propensity 
				for ( m = 0; m< num_molecules; ++m){
					// See if molecule is a reactant
					if (reaction_arr[INDEX2(num_reactions, num_molecules,r,m)] < 0){
						//printf("Molecule %d coefficient %d, abundance %d \n", m, -reaction_arr[INDEX2(num_reactions, num_molecules,r,m)], concentrations[INDEX3(max_x, max_y,num_molecules,picked_x,picked_y,m)]);
							
						// If molecule is a reactant add concentration^coefficient to current_Ap
						current_Ap =  current_Ap*pow(concentrations[INDEX3(max_x, max_y, num_molecules,picked_x,picked_y,m)], -reaction_arr[INDEX2(num_reactions, num_molecules,r,m)]); // Power is expensive 
					} 
					if (catalyst_arr[INDEX2(num_reactions, num_molecules,r,m)]> 0){
						// If the molcule is a catalsyt, include its effect
						cat_enhance += catalyst_arr[INDEX2(num_reactions, num_molecules,r,m)]*concentrations[INDEX3(max_x, max_y, num_molecules,picked_x,picked_y,m)];
					}
				}
				current_Ap = current_Ap*(1.0 + cat_enhance);
				////printf("	The propensity is %f  \n", current_Ap);
				

			}

  		// 		else if (propensity_function == 'RCM'){ //Only works for binary sequences
				// 	int nA = -reaction_arr[r][0];
				// 	double num_A = concentrations[x][y][0];
				// 	int nB = -reaction_arr[r][1];
				// 	double num_B = concentrations[x][y][1];
				// 	for (int m = 0; m< num_molecules; ++m ){
				// 		if (reaction_arr[r][m] > 0){
				// 			double num_replicator = concentrations[x][y][m];
				// 		}
				// 	}
				// 	checkpoint += replicator_composition_propensity_envMutation(constant, mu, num_replicator, num_A, num_B, nA, nB);
			
				// }

			checkpoint += current_Ap;
			//printf("Dice Roll is %f, checkpoint is %f\n", dice_roll, checkpoint  );
			if (checkpoint >=  dice_roll){
				picked_r = r;
				break;
			}

		}
		
		// Execute Reaction // 
		for ( m = 0; m< num_molecules; ++m){
			//printf("Current Concenration of molecule %d at lattice site (%d,%d), is %d \n", m, picked_x,picked_y,concentrations[INDEX3(max_x, max_y, num_molecules,picked_x,picked_y,m)]);
			concentrations[INDEX3(max_x, max_y, num_molecules,picked_x,picked_y,m)] += reaction_arr[INDEX2(num_reactions, num_molecules,picked_r,m)];
			//printf("updated Concenration of molecule %d at lattice site (%d,%d), is %d \n ", m, picked_x,picked_y,concentrations[INDEX3(max_x, max_y, num_molecules,picked_x,picked_y,m)]);
			
		}

		// Iterate over all lattice sites and all reactions at each site
		//printf("Updating Propensities \n");
		Ap_tot = 0.0;
		for ( x = 0; x< max_x; ++x){
			//printf("Current x is %d \n",x );
			for ( y = 0; y<max_y; ++y){
				//printf("Current y is %d \n",y );
				Ap_arr[INDEX2(max_x, max_y, x,y)] = 0.0;
				for ( r = 0; r< num_reactions; ++r){
					//printf("Current Reaction %d \n", r);
					current_Ap =reaction_constants[r];
					cat_enhance = 0.0;
					if (rxn_props[r] == 0){
						// The reaction has a standard propensity 
						for ( m = 0; m< num_molecules; ++m){
							// See if molecule is a reactant
							if (reaction_arr[INDEX2(num_reactions, num_molecules,r,m)] < 0){
								//printf("Molecule %d coefficient %d, abundance %d \n", m, -reaction_arr[INDEX2(num_reactions, num_molecules,r,m)], concentrations[INDEX3(max_x, max_y,num_molecules,x,y,m)]);
							
								// If molecule is a reactant add concentration^coefficient to current_Ap
								current_Ap =  current_Ap*pow(concentrations[INDEX3(max_x, max_y, num_molecules,x,y,m)], -reaction_arr[INDEX2(num_reactions, num_molecules,r,m)]);
							} 
							if (catalyst_arr[INDEX2(num_reactions, num_molecules,r,m)]> 0){
								// If the molcule is a catalsyt, include its effect
								cat_enhance += catalyst_arr[INDEX2(num_reactions, num_molecules,r,m)]*concentrations[INDEX3(max_x, max_y, num_molecules,x,y,m)];
							}
						}
						current_Ap = current_Ap*(1.0 + cat_enhance);
						

					}

			// 		else if (propensity_function == 'RCM'){ //Only works for binary sequences
				// 	int nA = -reaction_arr[r][0];
				// 	double num_A = concentrations[x][y][0];
				// 	int nB = -reaction_arr[r][1];
				// 	double num_B = concentrations[x][y][1];
				// 	for (int m = 0; m< num_molecules; ++m ){
				// 		if (reaction_arr[r][m] > 0){
				// 			double num_replicator = concentrations[x][y][m];
				// 		}
				// 	}
				// 	checkpoint += replicator_composition_propensity_envMutation(constant, mu, num_replicator, num_A, num_B, nA, nB);
			
				// }

					//printf("Current_Ap: %f \n", current_Ap );
					Ap_arr[INDEX2(max_x, max_y, x,y)] += current_Ap;
					Ap_tot += current_Ap;

				}
			}
		}
		
		if (time_evolve == 1) { // Time measure
			// Calculate next t	//
			double dice_roll = r2();
			if (Ap_tot == 0){
				current_t = next_t;
				}
			tau_step = -(log(dice_roll)/Ap_tot);
			// printf("Dice Roll %f \n", dice_roll);
			// printf("Time Step %f\n", tau_step );
			// printf("Ap_tot %f \n", Ap_tot );
			current_t += tau_step;
			if (tau_step < 0){
				exit(0);
				}
			if (current_t >= next_t){
				evolve = 0;
			}
			//printf("Time: %f \n", current_t);
		}
		if (time_evolve == 0) { // Reaction counting
			rxn_count += 1;
			//printf("%d \n", rxn_count );
			if (rxn_count >= next_t){
				evolve = 0;
			}


		}	
	}
	
	return current_t;
}

// int main()
// {
//   return 0;}

