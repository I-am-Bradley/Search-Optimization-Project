# Titagwan Bradley
import heapq
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# The function read 3sat file is used to read the 3sat file and extract the variables
# and their clauses from the various files
def read_3sat(filename):
    """Parses the CNF file into a list of clauses."""
    clauses = []
    # Use the function try to open the files.
    try:
        with open(filename, "r") as f:
            # We will go through every line and parse it. Extract all the clauses and
            # append the variables to their various lists.
            for line in f:
                # Create the clause list
                clause = []
                # Split each line so we can get the variables and the clauses
                parts = line.split()
                # Loop through all the various parts in parts
                for p in parts:
                    # Extracts variable index. Example: 'x12_pos' -> 12
                    var_idx = int(p.split('_')[0][1:])
                    # We store literals as (index, boolean_is_positive)
                    is_pos = "_pos" in p
                    # We append the various parts i.e the variables and their positions
                    # into the clause list.
                    clause.append((var_idx, is_pos))
                # Filtering empty lines. If we have an empty line, we will append the clause
                # to the clauses list.
                if clause:
                    clauses.append(clause)
    
    # If there is an error, we print the error.
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return clauses

# FITNESS FUNCTION
# THe function checks the fitness score of the individual and returns it.
def get_fitness(individual, clauses):
    """Counts how many clauses are satisfied by the current bit-string."""
    satisfied_count = 0
    for clause in clauses:
        for var_idx, is_pos in clause:
            # Check if the variable's value in 'individual' satisfies the literal
            # individual[var_idx] is 1 (pos) or 0 (neg)
            if (is_pos and individual[var_idx] == 1) or (not is_pos and individual[var_idx] == 0):
                satisfied_count += 1
                # Clause is True, move to next clause
                break 
    # Returns a count of the satisfied count.
    return satisfied_count

# GA OPERATORS
# The Selection process for the parents based on fitness score
def selection_tournament(scored_pop, k=3):
    """Selects the best individual from a random sample of size k."""
    # We randomly pick 3 digits from the range of the length of the scored population
    # (A scored population simply means their fitness level has been checked) and 
    # store them in a list called indices. We loop through the list of indices to pick
    # cities that are found in indexes in the list and append to the selection list
    selection = []
    indices = np.random.choice(len(scored_pop), k, replace=False)
    for i in indices:
        select = scored_pop[i]
        selection.append(select)
    # From the selection list, noting that the individuals are tuples with fitness
    # scores, we sort the list according to their fitness score and we are telling
    # python to look at their fitness scores at x[1] and reverse the list because
    # the highest score is the best score.(Python sorts in ascending order)
    selection.sort(key=lambda x: x[1], reverse=True)
    # We return the first individual by extracting their bit string only which will
    # be the first tuple in the selection list and the first in the tuple.
    return selection[0][0]

# The CROSSOVER operation
# we crossover the two parents to come out with two children. Creating two children
# is to keep the population size stable.
def crossover(p1, p2, method):
    """Recombines two parents into two children."""
    # The size of the dna is determined by the parents. This is to make sure the 
    # crossover works regardless of the size
    size = len(p1)
    # We have two methods. The single slicing and the two point slicing.
    # For the single slicing, we will obtain a random integer between 1 and the
    # size of dna minus 1. For indexing, we start at zero and go up to size minus 1
    # We cannot start at zero because then we are just getting the exact copy of one
    # parent and nothing from the other parent but even if the algorithm chooses 
    # size - 1 then we will just have the last bit to copy so there is still a 
    # crossover.
    if method == "single":
        # Chooses a random number between 1 and the size of parent minus 1
        cp = np.random.randint(1, size)
        # Child one is the bit string of parent 1 from the first bit to the cut of
        # bit and the bit string of parent 2 from the cut of bit to the end.
        c1 = p1[:cp] + p2[cp:]
        # Child two is the bit string of parent 2 from the first bit to the cut of
        # bit and the bit string of parent 1 from the cut of bit to the end.
        c2 = p2[:cp] + p1[cp:]
  
    # For the double slicing, we will obtain two random integers. The first one between
    # 1 and size of dna minus 2 and the second one between the first random integer plus
    # one and the size of the dna minus one. We do this so as to get two distinct
    # parts of the dna for both parents so as not to end up with a mix in the dna.
    elif method == "two_point":
        # Choose two random numbers between the range 1 and the length of the parent.
        pts = sorted(np.random.choice(range(1, size), 2, replace=False))
        cp1, cp2 = pts[0], pts[1]
        # Child one is the beginning and the ending bit srting of parent 1 and the
        # middle bit string of parent 2.
        c1 = p1[:cp1] + p2[cp1:cp2] + p1[cp2:]
        # Child two is the beginning and the ending bit srting of parent 2 and the
        # middle bit string of parent 1.
        c2 = p2[:cp1] + p1[cp1:cp2] + p2[cp2:]

    # This method is the most aggressive method of crossover where each bit is examined
    # independently. For each bit there is a fifth percent chance it gets it from parent 1 or 
    # parent 2.
    elif method == "uniform":
        c1, c2 = [], []
        # We create a list of random floats
        mask = np.random.random(size)
        # We create a loop so as to create a child with the same size as the parents.
        for i in range(size):
            # For any digit chosen in the range, we choose a float in mask at the index
            # equal to the digit so as to prevent repetition.
            # 0.5, c1 gets the bit from p1 and c2 gets the bit from p2. If the float
            # is greater than 0.5, c1 gets the bit from p2 and c2 gets the bit from p1
            if mask[i] < 0.5:
                c1.append(p1[i])
                c2.append(p2[i])
            else:
                c1.append(p2[i])
                c2.append(p1[i])

    return c1, c2


# The MUTATION operation
# we create new bit combinations that might never have existed before based on the 
# mutation rate that is given.
def mutate(individual, rate):
    """Guarantees at least one flip if the rate is met."""
    # We create a for loop that goes through every bit in the individual, if the 
    # random float generated is less the the mutation rate, we flip the bit. After 
    # going through every bit, we return the new individual.
    
    mutated = False
    for i in range(len(individual)):
        if np.random.random() < rate:
            individual[i] = 1 - individual[i]
            mutated = True
    
    # If the probability missed every bit, we choose a random bit and flip to
    # prevent exact clones of their parents.
    if not mutated:
        idx = np.random.randint(0, len(individual) - 1)
        individual[idx] = 1 - individual[idx]
    return individual

# MAIN Genetic Algorithm
# This is the main operator. We have an input file containing our clauses and we have
# to return a population that satisfies a conditions given. In my case, I have defined
# it as a fitness level.
def solve_3sat_ga(filename, pop_size, generations, mut_rate):
    # We call the read_3sat function to open the file and return us the clauses.
    clauses = read_3sat(filename)
    if not clauses: 
        return None

    # We go through all the clauses to determine the number of variables and determine
    # the highest index.
    num_vars = 0
    for c in clauses:
        for var_idx, _ in c:
            num_vars = max(num_vars, var_idx + 1)

    # Initialize Population
    population = []

    # We create a for loop that will run as many times as the population size because
    # we want to create a number of individuals equal to the population size as required.
    for _ in range(pop_size):
        
        # Create a random array of 0s and 1s of length 'num_vars'
        # We use 0, 2 because the high bound is exclusive in numpy
        random_bits = np.random.randint(0, 2, size=num_vars)
        
        # Convert the numpy array to a standard Python list
        individual = random_bits.tolist()
        
        # Add the completed individual to our population
        population.append(individual)

    
    # We are creating data storage for plotting
    history_max = []
    history_min = []
    history_avg = []
    
    # --- STAGNATION TRACKING VARIABLES ---
    # We want to keep track how the fitness changes through out the generations and
    # we want to use it to prevent stagnation between the generations for too long.
    best_ever_fitness = -1
    stagnation_counter = 0
    base_mut_rate = mut_rate 

    print(f"\n--- Solving {filename} ({num_vars} vars, {len(clauses)} clauses) ---")

    # We create a for loop that will run as many times as the generation because
    # we want to go up to the required generation.
    for gen in range(generations):
        # We initialize the parents and the fitness value list
        scored_pop = []
        fitness_values = []
        
       # We run the for loop for all the individuals in the population so as to get 
        # the fitness level of everyone.
        for ind in population:
            # 1. Run the fitness function for this specific bit-string to get the score
            score = get_fitness(ind, clauses)
            
            # 2. Store the pair (individual, score)
            scored_pop.append((ind, score))
            
            # 3. Keep a separate list of just scores for math/stats
            fitness_values.append(score)
        
        # --- RECORD STATS ---
        # Find the best, worst, and average scores in this generation
        # We find the max fitness values in the list and set it as the current max fitness
        # then we append the current max to the history of maxes, the current min to
        # the history of mins and the average to the list of averages.
        current_max = max(fitness_values)
        history_max.append(current_max)
        history_min.append(min(fitness_values))
        history_avg.append(sum(fitness_values) / pop_size)

        # --- MUTATION BURST LOGIC ---
        # If the current max fitness is better than the best ever fitness then we have
        # progress and so we reset the stagnation counter and maintain the mutation rate.
        if current_max > best_ever_fitness:
            best_ever_fitness = current_max
            # Reset counter: we made progress!
            stagnation_counter = 0 
            current_mut_rate = base_mut_rate
            is_stagnant = False
        # Each time we will increment the stagnation counter
        else:
            stagnation_counter += 1

        # If we are stuck for more than 50 generations, we will boost the mutation rate
        # by 15%
        # --- MUTATION BURST LOGIC ---
        if stagnation_counter > 75:
            # 1. Start with a high 'initial' burst (e.g., 0.20)
            # 2. Reduce it by 10% for every generation past the trigger point
            # Calculation: 0.20 * (0.90 ^ (stagnation_counter - 50))
            decay_steps = stagnation_counter - 75
            decay_rate = base_mut_rate * (0.90 ** decay_steps)
            
            # We use max() to ensure it never falls below your 0.05 base rate
            current_mut_rate = max(decay_rate, base_mut_rate)
                
            is_stagnant = True
        else:
            current_mut_rate = base_mut_rate
            is_stagnant = False

    
        if gen % 10 == 0: print(f"Gen {gen} Best: {current_max}")

        # Sort to find the best for Elitism
        # We are sorting the entire popluation so we can have the fittest individuals
        # at the beginning of the list so we can assure mating.
        scored_pop.sort(key=lambda x: x[1], reverse=True)
        
        # 2. Check for 100% solution early
        if scored_pop[0][1] == len(clauses):
            print(f"Perfect solution found at Generation {gen}!")
            # We update history one last time so the graph shows the 100% mark
            history_max.append(scored_pop[0][1])
            history_min.append(min(fitness_values))
            # the average is skewed at exit, but that's okay
            history_avg.append(scored_pop[0][1]) #
            break 

        # Create the next generation
        # We calculate the elite size by taking 10% of the population.
        # The new population will retain that 10% so as to retain the level of fitness
        # and also give room for a greater possibility to reach 100% 
        elite_count = int(pop_size * 0.10)
        new_pop = []
        # We want to keep a set called seen so we can track the individuals we have seen
        # and prevent duplicates in the new population
        seen = set()
        
        # We go through all the individuals in the scored population and take the top
        # 10% to start our new population.
        for i in range(elite_count):
            # We take the bit-string (index 0) of the i-th best individual
            elite_individual = list(scored_pop[i][0])
            new_pop.append(elite_individual)
            seen.add(tuple(elite_individual))

        # We add a timeout counter to prevent infinite loops if mutation is 0
        attempts = 0
        # We run a while loop so that we can create a new population of the required size.
        while len(new_pop) < pop_size:
            # Selection
            # Selecting new parents
            p1 = selection_tournament(scored_pop)
            p2 = selection_tournament(scored_pop)
            
            
            # Conditional Crossover
            # The crossover is conditional because we are trying to fight against stagnation
            # in multiple generations. Some of the cross over methods are less aggressince
            # than others so we have to take that inot account and not do random selection
            # for all crossover methods.
            # We are performing the crossover of the parents to get the children
            if is_stagnant:
                # We use the uniform crossover if there is stagnation because it is more 
                # aggressive.
                c1, c2 = crossover(p1, p2, method="uniform")
            else:
                # Use standard blocks during normal progress because there are less aggressive.
                methods = ["single", "two_point"]
                chosen_method = np.random.choice(methods)
                c1, c2 = crossover(p1, p2, method=chosen_method)
            
            # Mutation & Adding to new population
            # We will perform mutation and keep adding the children to the new population
            # until we reach the required size.
            for child_raw in [c1, c2]:
                child = mutate(list(child_raw), current_mut_rate)
                child_tuple = tuple(child)
                
                if child_tuple not in seen and len(new_pop) < pop_size:
                    new_pop.append(child)
                    seen.add(child_tuple)
            
            attempts += 1

        # OVERWRITE the old population with the new generation
        population = new_pop

       
    # We want to be able to find out what our highest fitness achieved was through out
    # the various generations.
    best_fit = max(history_max)
    
    print(f"Final Results for {filename}:")
    print(f"  - Clauses Satisfied: {best_fit}")
    print(f"  - Total Clauses:     {len(clauses)}")
    print(f"  - Accuracy:          {(best_fit/len(clauses))*100:.2f}%")

    
    if filename == "3SAT_100_100.txt":
        # Plotting
        plt.figure(figsize=(10, 6))
        gens = range(len(history_max))
        plt.plot(gens, history_max, label="Max Fitness", color='green', linewidth=2)
        plt.plot(gens, history_avg, label="Average Fitness", color='blue', linestyle='--')
        plt.plot(gens, history_min, label="Min Fitness", color='red', alpha=0.5)
            
        plt.title(f"GA Performance on {filename}")
        plt.xlabel("Generation Index")
        plt.ylabel("Fitness (Satisfied Clauses)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    return scored_pop[0][0]

def main():
    # List of files to run normally without plotting
    other_files = ["3SAT_4_6.txt", "3SAT_24_100.txt"]
    
    # 1. Run standard files first
    for f in other_files:
        print(f"\n--- Processing {f} ---")
        # Standard GA solver (no plotting)
        solution = solve_3sat_ga(f, pop_size=100, generations=500, mut_rate=0.05)
        if solution:
            # Only print first 10 bits of solution for long files to save space
            display = solution[:10] if len(solution) > 10 else solution
            print(f"Result for {f}: {display}...")

    # 2. Run the Plotting Analysis ONLY for the 100_100 file
    target_file = "3SAT_100_100.txt"
    print("\n" + "="*50)
    print(f"GENERATING REQUIRED PLOTS FOR: {target_file}")
    print("="*50)
    
    # Call the version that records history and calls plt.show()
    solution = solve_3sat_ga(target_file, pop_size=150, generations=1000, mut_rate=0.050)
    if solution:
            # Only print first 10 bits of solution for long files to save space
            display = solution[:10] if len(solution) > 10 else solution
            print(f"Result for {target_file}: {display}...")

  
    # 2. Run the 100_500 file
    target_file = "3SAT_100_500.txt"
    print("\n" + "="*50)
    print(f"\n--- Processing {target_file} ---")
    print("="*50)
    
   
    # Call the version that records history and calls plt.show()
    solution = solve_3sat_ga(target_file, pop_size=300, generations=1500, mut_rate=0.010)
    if solution:
            # Only print first 10 bits of solution for long files to save space
            display = solution[:10] if len(solution) > 10 else solution
            print(f"Result for {target_file}: {display}...")

if __name__ == "__main__":
    main()
