# TItagwan Bradley
import random
import time
import numpy as np
import heapq
import os
import matplotlib.pyplot as plt

# The function read tsp file is to read the gps file and extract the coordinates
# from the various files
def read_tsp_file(filename):
    # We create a list of cities so that we can store the various coordinates
    # in it
    cities = []
    # We use with open command to open the file, parse through it and extract
    # the information we need.
    with open (filename, 'r') as f:
        for line in f:
             # For each line in the file, we strip its ends and slice it so we
             # can get the x and y coordinates then store is as a tuple to prevent
             # mutabaility.
             parts = line.strip().split()

             if len(parts) >= 2:
                 x = float(parts[0])
                 y = float(parts[1])
                 cities.append((x,y))

    return cities



# The function distance is used to calculate the euclidian distance
# between two cities.
def distance(p1, p2):
    # the formula is the square root of the difference between the x- coordinates
    # squared added to the difference between the y-coordinates squared.
    x = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    return x

# The function total distance is used to calculate the total cost of the entire
# tour.
def total_distance(tour):
    total = 0
    # we are loop through all the cities in the tour list to get the distance from
    # one city to another then returning the total
    for i in range(len(tour)):
        # We are calculating the distance to next city (looping back to start at the end)
        total += distance(tour[i], tour[(i + 1) % len(tour)])
    return total

def get_permutations(lst):
    if len(lst) == 0:
        return[[]]
    
    res = []
    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i+1:]
        for p in get_permutations(remLst):
            res.append([m] + p)
    return res

# The function brute force tsp is one of the algorithms and it is
# used to check all possible permutations for the tour
# that will give us the best tour back to the starting city.
def brute_force_tsp(cities):
    # Once we start the function, we also want to start the time so as to measure
    # how long the operation runs for.

    start_time = time.time()

    # We have a fixed starting city and then the rest come in any other.
    start_city = cities[0]
    other_city = cities[1:]

    # we have to keep track of the minimum distance so that we can be able to
    # determine at the end of the iterations which tout has the smallest
    # distance and thus the best tour because we are using distance to determine
    # that
    min_dist = float('inf')
    best_tour = None

    # Manually generated permutations
    all_perms = get_permutations(other_city)
    # We are going to do a permutation of the other city and go through all of
    # them so as to be sure that we have absolutely checked all possibilities of
    # a tour and we have determined the best.
    for p in all_perms:
        # We have a list of the current tour we are going to check.
        current_tour = [start_city] + list(p)
        # We are going to check the total distance of the current tour using the 
        # total distance function
        current_dist = total_distance(current_tour)

        # We will compare the distance of the current tour to the minimum distance
        # and if it is less than it, we make it the new distance and make its tour
        # the best tour.
        if current_dist < min_dist:
            min_dist = current_dist
            best_tour = current_tour
    
    # We end the timer because the algorithm is over.
    finished_time = time.time()

    # We calculate the execution time by substracting the start time from the
    # finished time
    exec_time = finished_time - start_time
    return best_tour, min_dist, exec_time

# The simulated annealing tsp function is the second and the more efficient 
# algorithm used to determine the best tour with less execution time and optimality
def simulated_annealing_tsp(cities, temp, cooling_rate):
    current_tour = list(cities)
    # We randomly shuffle the list of the cities so that we can start from any city
    # then we calculate the distance of the tour.
    np.random.shuffle(current_tour)
    
    current_dist = total_distance(current_tour)

    # We append the fist list of the current tour and the current distance to the
    # list of best tour and best distance so we can have a reference and because the 
    # first is technically the best at that point in time.
    best_tour = list(current_tour)
    best_dist = current_dist

    # We want to keep history of how the temperature and cost changed and what the 
    # random walks were
    history_temp = []
    history_cost = []
    history_random_walk = []

    t = temp

    # As far as the temp is greater than 0.001, we means we are setting our stopping point
    # or what we call freezing point. This is to prevent infinite looping and reduce
    # execution time.
    while t > 0.001:
        # We attempt several moves at this specific temperature
        for _ in range(len(cities)):
            # We equate the list of the current tour to the new tour
            new_tour = list(current_tour)
            # We use the len of the new list as the range of numbers to choose from, select
            # two digits and the numbers are chosen only once.
            # The sorted always makes sure i is smaller than j.
            i, j = sorted(np.random.choice(len(new_tour), 2, replace=False))
            # Reverse the entire segment between i and j
            new_tour[i:j] = reversed(new_tour[i:j])

            # Now we calculate the total distance of the new tour.
            new_dist = total_distance(new_tour)

            # We calcualate delta e by substracting the current distance from the new distance.
            delta_e = new_dist - current_dist
            
            
            # Delta e being less than zero means it was less than the current distance and so
            # a better tour than the current want and so we want to append to the new current
            # tour and distance so that can be used in the next comparison with the new tour 
            # and distance.
            if delta_e < 0:
                current_tour = new_tour
                current_dist = new_dist
                # A better tour is not considered a random walk and so we equate random
                # walk equal to 0
                random_walk = 0

            else:
                # We use random.random to act like our judge to determine if we should take 
                # the risk. It produces a float between 0.0 and 1.0 and if the exponent of
                # negative delta e divided by t is greater than it, we wouldn't take the risk
                # and vice versa. If it is less than the random float, the new tour will be 
                # turned into our current tour and then it will be used to compare to the
                # new tour.
                if np.random.random() < np.exp(-delta_e / t):
                    current_tour = new_tour
                    current_dist = new_dist
                    # We equate the random walk to 1 because we accepted the worser tour
                    random_walk = 1

                # We equate the random walk to 0 because we did not accept the worser tour
                else:
                    random_walk = 0
        
            # If the current dist is less than the best dist, then it is the best dist and
            # will be updated as such.
            if current_dist < best_dist:
                best_dist = current_dist
                best_tour = list(current_tour)
        
        # We want to log the current distance, randow walk and temp to the cost, random 
        # walk and temperature history
        # # A better tour is not considered a random walk and so we append 0s.
        history_random_walk.append(random_walk)
        history_temp.append(t)
        history_cost.append(current_dist)

        # the temperature will be changed everytime we run the while loop and the
        # temperatured lowered using the cooling rate.
        # Temperature follows geometric cooling: T_k = T_0 * (cooling_rate ** k)
        t *= cooling_rate

    return best_tour, best_dist, history_temp, history_cost, history_random_walk

def plot_results(tour, temp_hist, cost_hist, walk_hist):
    # We use the len of the temperature histore list to get the range of the number
    # of iterations.
    iterations = range(len(temp_hist))
    
    # We are definig the size of the figure. (width and height)
    plt.figure(figsize=(12, 10))

    # Plot 1: Temperature vs number of iterations
    plt.subplot(2, 2, 1)
    plt.plot(iterations, temp_hist, color='red')
    plt.title("Iteration vs Temperature")
    plt.xlabel("Iteration")
    plt.ylabel("Temp")

    # Plot 2: Cost (Distance) vs number of iterations
    plt.subplot(2, 2, 2)
    plt.plot(iterations, cost_hist, color='blue')
    plt.title("Iteration vs Tour Cost")
    plt.xlabel("Iteration")
    plt.ylabel("Distance")

    # Plot 3: Random Walk Occurrence vs number of iterations
    plt.subplot(2, 2, 3)
    plt.scatter(iterations, walk_hist, alpha=0.1, s=1, color='green')
    plt.title("Random Walk (1=Yes, 0=No)")
    plt.xlabel("Iteration")
    plt.ylabel("Walk Event")

    # Plot 4: The Final Tour Map
    plt.subplot(2, 2, 4)
    x = [c[0] for c in tour] + [tour[0][0]]
    y = [c[1] for c in tour] + [tour[0][1]]
    plt.plot(x, y, 'o-r')
    plt.title("Final Output Tour")
    
    plt.tight_layout()
    plt.show()

def main():
    # 1. Configuration
    # Change to "TSP2.txt", "TSP3.txt", etc.
    files = ["TSP1.txt", "TSP2.txt", "TSP3.txt", "TSP4.txt"]
    
    # We want the main function to be able to go through all the files in
    # the file list.
    for file in files:
        
        # We ran 10 trials to measure the stability and reliability of the
        # sa algorithm
        number_sa_trials = 10     
        
        # We load the data from the files. If we do not return cities,
        # then we know we have a problem reading the files.
        cities = read_tsp_file(file)
        if not cities:
            print(f"Error: Could not load {file}.")
            return

        print(f"{'='*50}")
        print(f"TSP COMPARISON: {file} ({len(cities)} Cities)")
        print(f"{'='*50}")

        # Brute Force Execution (The Baseline)
        # We run this once because it is deterministic (always gives the same answer)
        # We display the best distance and execution time.
        print("Calculating Brute Force (Optimal)...")
        bf_tour, bf_dist, bf_time = brute_force_tsp(cities)
        print(f"  [BF] Best Distance: {bf_dist:.4f}")
        print(f"  [BF] Execution Time: {bf_time:.6f}s")
        print("-" * 50)

        # Simulated Annealing Execution
        # We run this multiple times because it is probabilistic (results may vary)
        print(f"Executing Simulated Annealing ({number_sa_trials} trials)...")
        sa_results = []
        
        # These parameters can be tuned for larger files
        initial_temp = 100
        cooling_rate = 0.999
       
        start_time = time.time()

        for i in range(number_sa_trials):
            # Even though we only care about the distance for the stability check, we need
            # all the return so that we can plot a graph down the line.
            best_tour, best_dist, history_temp, history_cost, history_random_walk = simulated_annealing_tsp(cities, initial_temp, cooling_rate)
            # Since we get the best distance every time we run the program, we append it
            # to the sa results list so as to compare the different results produced each
            # trial since the algorithm is probabilistic.
            sa_results.append(best_dist)
            print(f"  Trial {i+1}: {best_dist:.4f}")

        # We end the timer here and get the average time of execution since it runs a numnber
        # of times.
        end_time = time.time()
        avg_time = (end_time - start_time) / number_sa_trials


        # Stability & Optimality Analysis
        best_sa = min(sa_results)
        # Count how many times SA matched the Brute Force result by going through the list of
        # sa results and substraction the bf distance from each and if the absolute of the 
        # difference is less than 0.000001 which is what le-6 stands for then we know it is 
        # approximately equal to zero and thus successful.
        success_count = 0
        for d in sa_results:
            if abs(d - bf_dist) < 1e-6:
                success_count += 1

        print("-" * 50)
        print(f"FINAL METRICS:")
        print(f"  Optimal Distance: {bf_dist:.4f}")
        print(f"  SA Best Found:    {best_sa:.4f}")
        print(f"  SA Stability:     {success_count}/{number_sa_trials} runs reached optimal")
        print(f"  SA Execution Time: {avg_time:.6f}s")
        print(f"{'='*50}")

        # We want to plot a graph for the fourth text.
        if file == "TSP4.txt":
            plot_results(best_tour, history_temp, history_cost, history_random_walk)


if __name__ == "__main__":
    main()