# Bradley Titagwan
import heapq
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# We will just define the goal state as a tuple and rather an array because it is easier to deal with
# and it will reduce the running time.
GOAL_STATE = (8, 1, 6, 3, 5, 7,4, 9, 2)

def get_initial_state():
    # To generate the initial state, we will use numpy to random shuffle a range from 1 to 10 and then
    # arrange it in a 3x3 square and save it as a tuple for easy acess.

    arr = np.arange(1, 10)
    np.random.shuffle(arr)
    return tuple(arr)


def get_successors(state_tuple):
    # The get successor function generates all the possible states by swapping any two adjacent tiles.
    # We use a for loop for generating all these possibilites. We create a list successors to store all
    # the possible states that can be achieved from swapping any two adjacent tiles.
    # We will also need to change the state tuple back into an array to be able to do the changes since
    # a tuple is immutable.
    
    successors = []
    grid = np.array(state_tuple).reshape(3, 3)
    
    # We will use a for loop inside of the for loop to loop through all the various tiles but we will do
    # only two adjacent swaps. The right and bottom because most of the tiles share adjacent neighbors and
    # we do not want duplication.

    for r in range(3):
        for c in range(3):
            # We are swapping with the right neighbor, which is on a different column.
            # We use column less than 2 because the index is 0, 1, 2 and so if c = 2 then c+1 will be 3
            # which will give us an error. Same goes for the row too.
            # We finally add the next_grid into the successors list as a flatten tuple for easier access
            if c < 2:
                next_grid = grid.copy()
                next_grid[r, c], next_grid[r, c+1] = next_grid[r, c+1], next_grid[r, c]
                successors.append(tuple(next_grid.flatten()))
            # We are now swapping with the down neighbor, which is on the adjacent row
            if r < 2:
                next_grid = grid.copy()
                next_grid[r, c], next_grid[r+1, c] = next_grid[r+1, c], next_grid[r, c]
                successors.append(tuple(next_grid.flatten()))
    return successors  

def reconstruct_path(parent_map, current):
    # Traces back from goal to start using the parent dictionary.
    # It will reverse the path list at the end because we want the list starting from the initial state
    # to the goal state but the list is being appended starting from the goal state. 
    path = []
    # We use while current is not none becuase all the child states have a parent state or the state they
    # changed from except the initial state. So the loop will end when it reaches the initial state because
    # the initial state does not have a parent state.
    while current is not None:
        path.append(current)
        current = parent_map[current]
    # Return the path from starting state to goal state by reversing the list.    
    return path[::-1] 

def ucs(start_state, goal_state):
    # This is the uniform cost search implementation
    # We need to get the time at the start so we keep a track of how long the process takes.
    start_time = time.time()

    # The frontier is a list of tuples with the cumulative cost to reach that state and the current state.
    frontier = [(0, start_state)]

    # We have to make a dictionary parent map to keep track of all the states and their parents.
    parent_map = {start_state: None}    

    # We will also make a dictionary visited to keep track of all the states visited and their cost.
    visited = {start_state: 0}

    # We will also have to keep track of the nodes expanded for report purposes.
    nodes_expanded = 0

    # So far as the frontier is not empty the while loop will continue to run
    while frontier:
        # We extract the cost and the currennt state by using heapq
        cost, current = heapq.heappop(frontier)
        # We increment the counter nodes_expanded
        nodes_expanded += 1
        
        # We test if the current state is the goal state and if so, we will calculate the execution time,
        # reconstruct the path using the reconstruction function and return the path, expanded nodes and
        # the execution time.
        if current == goal_state:
            exec_time = time.time() - start_time
            path = reconstruct_path(parent_map, current)
            return path, nodes_expanded, exec_time
        
        # If the current is not the goal state we will place the current into a for loop to generate all 
        # the possible states that can be achieved from the current. 
        for new in get_successors(current):
            new_cost = cost + 1
            
            # If any of the possible states are not in visited or their new cost is less than the one in visited, 
            # we will give the state a new cost in the dictionary and then push it into the frontier
            if new not in visited or new_cost < visited[new]:
                visited[new] = new_cost
                parent_map[new] = current
                heapq.heappush(frontier, (new_cost, new))
    
    # In a situation where no solution is reached and the while loop ends. We want to return number of 
    # expandend nodes and the execution time. 
    exec_time = time.time() - start_time
    return None, nodes_expanded, exec_time

"""
For the astar search we will need a heuristic. My heuristic will be the distance from the initial state
to the goal state. Also known as the manhattan distance. Also since we are moving adjacent tiles, there is
a scenario where swapping both tiles bring both one step to their goal position and so that will be the
ideal move we will try to execute first and therefore we will divide the distance by two to account for this.
"""
# We will need to record the target coordinates of the goal_state magic square
TARGET_POS = {
    8: (0,0), 1: (0,1), 6: (0,2),
    3: (1,0), 5: (1,1), 7: (1,2),
    4: (2,0), 9: (2,1), 2: (2,2)
}

# First Heuristic for A*
# Calculating the Manhattan distance
def heuristic1(initial_state):
    total_distance = 0

    # We are using a for loop to go through the entire initial state and calculate each tile's distance from
    # it's goal position
    for i, value in enumerate(initial_state):

        # The line below is to get the position of a tile in the array. The variable i is the index since the initial
        # state is a flat tuple
        # Since it is a 3x3 array, dividing by three gives you the row and the remainder gives you the column.
        row, col = i // 3, i % 3
        target_r, target_c = TARGET_POS[value]
        # To get the distance, we substract the distance between the row and target row, the column and target
        # column, add their absolute value and then add to the value of total distance to get the new distance.
        total_distance += abs(row - target_r) + abs(col - target_c)

    # Dividing by two makes it admissable for adjacent swaps
    return total_distance / 2       

# Second Heuristic for A*
def heuristic2(initial_state):
    """Counts how many tiles are not in their goal position."""
    # GOAL_STATE = (8, 1, 6, 3, 5, 7, 4, 9, 2)
    misplaced_count = 0
    
    # Pair up the current state and goal state
    zipped_states = zip(initial_state, GOAL_STATE)
    
    # We go through the initial state and Goal state list to compare if
    # the tile in the initial state is in the goal state.
    for s, g in zipped_states:
        if s != g:
            # Add 1 to the total for every mismatch
            misplaced_count += 1
            
    return misplaced_count



def a_star(start_state, goal_state, heuristic_func):
    # This is the A star search implementation
    # We need to get the time at the start so we keep a track of how long the process takes.
    start_time = time.time()
    
    # The frontier is gotten from by returning a list of tuples from the heuristic function, with the cumulative cost to reach that state and the current state.
    frontier = [(heuristic_func(start_state), start_state, 0)]

    # We have to make a dictionary parent map to keep track of all the states and their parents.
    parent_map = {start_state: None}
    
    # We will also make a dictionary visited to keep track of all the states visited and their cost.
    visited = {start_state: 0}
    

    # We will also have to keep track of the nodes expanded for report purposes.
    nodes_expanded = 0

    # So far as the frontier is not empty the while loop will continue to run
    while frontier:
        # We extract the heuristic, the cost and the currennt state by using heapq
        f, current, g = heapq.heappop(frontier)
        # We increment the counter nodes_expanded
        nodes_expanded += 1

        # We test if the current state is the goal state and if so, we will calculate the execution time,
        # reconstruct the path using the reconstruction function and return the path, expanded nodes and
        # the execution time.
        if current == goal_state:
            exec_time = time.time() - start_time
            path = reconstruct_path(parent_map, current)
            return path, nodes_expanded, exec_time
        
        # If the current is not the goal state we will place the current into a for loop to generate all 
        # the possible states that can be achieved from the current. 
        for new in get_successors(current):
            new_g = g + 1

            # If any of the possible states are not in visited or their new cost is less than the one in visited, 
            # we will calculate a new cost new_f by adding the new_g to the heuristic of the new state then 
            # give the state a new cost in the dictionary and then push it into the frontier
            if new not in visited or new_g < visited[new]:
                visited[new] = new_g
                parent_map[new] = current
                #Note that f = g + h
                new_f = new_g + heuristic_func(new)
                heapq.heappush(frontier, (new_f, new,new_g))
    
    # In a situation where no solution is reached and the while loop ends. We want to return number of 
    # expandend nodes and the execution time. 
    exec_time = time.time() - start_time
    return None, nodes_expanded, exec_time


def run_final_evaluation():
    """
    The function run_final_evaluation is to compare the two programs ucs and a_star search.
    We want to compare how many nodes where expanded, time to execute and the costs.
    Also we will be comparing two heuristics which are the total misplaced tiles divided by 2 and the
    total misplaced tiles. 
    """
    # Data storage for all metrics
    # This is a dictionary that will store all the results from the three alternative programs
    results = {
        'UCS': {'nodes': [], 'times': [], 'costs': []},
        'A* Manhattan': {'nodes': [], 'times': [], 'costs': []},
        'A* Misplaced': {'nodes': [], 'times': [], 'costs': []}
    }

    print(f"{'Run':<4} | {'Algo':<15} | {'Nodes':<8} | {'Time (s)':<10} | {'Cost'}")
    print("-" * 55)

    # We will run the programs ten times and get an average so that we can come to an appropriate
    # conclusion. We will put the programs in a for loop for that.
    for i in range(10):
        start = get_initial_state()
        
        # 1. We will call the UCS program.
        # If a path is returned, it means a solution was reached and it's results will be added to the
        # dictionary for results.
        path1, nodes_expanded1, exec_time1 = ucs(start, GOAL_STATE)
        if path1:
            results['UCS']['nodes'].append(nodes_expanded1)
            results['UCS']['times'].append(exec_time1)
            results['UCS']['costs'].append(len(path1) - 1)

        # 2. We will call the A* program and use the second heuristic function.
        # The second heuristic function uses the total misplaced tiles as its heuristic.
        # If a path is returned, it means a solution was reached and it's results will be added to the
        # dictionary for results.
        path2, nodes_expanded2, exec_time2 = a_star(start, GOAL_STATE, heuristic2)
        if path2:
            results['A* Manhattan']['nodes'].append(nodes_expanded2)
            results['A* Manhattan']['times'].append(exec_time2)
            results['A* Manhattan']['costs'].append(len(path2) - 1)

        # 3. We will call the A* program and use the first heuristic function.
        # The first heuristic function uses the total misplaced tiles divided by two as its heuristic.
        # If a path is returned, it means a solution was reached and it's results will be added to the
        # dictionary for results.
        path, nodes_expanded, exec_time = a_star(start, GOAL_STATE, heuristic1)
        if path:
            results['A* Misplaced']['nodes'].append(nodes_expanded)
            results['A* Misplaced']['times'].append(exec_time)
            results['A* Misplaced']['costs'].append(len(path) - 1)

        # We will print out the standard output for each run
        print(f"#{i+1:<3} | UCS             | {nodes_expanded1:<8} | {exec_time1:.4f}     | {len(path1)-1}")
        print(f"          | A* Manhattan    | {nodes_expanded2:<8} | {exec_time2:.4f}     | {len(path2)-1}")
        print(f"          | A* Misplaced    | {nodes_expanded:<8}  | {exec_time:.4f}     | {len(path)-1}")
        print("-" * 55)

    # At the end we will call the plot results function to give us a graphical representation of comparisons.
    plot_results(results)

def plot_results(results):
    # The labels are the key values in the dictionary which are the list of nodes expanded, execution time and cost.
    labels = list(results.keys())
    avg_nodes = [np.mean(results[k]['nodes']) for k in labels]
    avg_times = [np.mean(results[k]['times']) for k in labels]
    avg_costs = [np.mean(results[k]['costs']) for k in labels]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    
    # Chart 1: Nodes
    # We will plot the various nodes expanded for the different type of searches
    ax1.bar(labels, avg_nodes, color=['#e74c3c', '#3498db', '#2ecc71'])
    ax1.set_title('Avg Nodes Expanded')
    ax1.set_ylabel('Nodes')

    # Chart 2: Time
    # We will plot the various execution times for the different type of searches
    ax2.bar(labels, avg_times, color=['#e74c3c', '#3498db', '#2ecc71'])
    ax2.set_title('Avg Execution Time')
    ax2.set_ylabel('Seconds')

    # Chart 3: Path Cost
    # We will plot the various path cost for the different type of searches
    ax3.bar(labels, avg_costs, color=['#e74c3c', '#3498db', '#2ecc71'])
    ax3.set_title('Avg Solution Path-Cost')
    ax3.set_ylabel('Moves')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
        
    # 1. Single Run Demonstration (Visualizing the steps)
    print("-------------------------- SINGLE RUN DEMO --------------------------")
    
    demo_start = get_initial_state()
    print("Initial State:")
    # We want to display the initial state as a 3x3 array
    print(np.array(demo_start).reshape(3, 3))
    print("\nGoal State:")
    # We want to display the goal state as a 3x3 array
    print(np.array(GOAL_STATE).reshape(3, 3))
    print("-" * 30)

    # We will call the A star function to execute the program
    path, nodes, exec_time = a_star(demo_start, GOAL_STATE, heuristic2)
    
    # How the print results will look like.
    # If a path list is returned, then there is a solution. If not we return no solution
    # for the initial state could not be attained. The problem is some randomized 3x3 magic
    # cube are insolvable.
    if path:
        print(f"\nDemo Success! Path-Cost: {len(path)-1} moves.")
        print(f"Nodes Expanded: {nodes} | Time: {exec_time:.4f}s")
        # We are transforming the first state and a few with the last state if the states are too many
        # in the path. They are being printed for easier visibility and understanding to the user.
        for i, state in enumerate(path):
            print(f"Step {i}:")
            print(np.array(state).reshape(3, 3))
    else:
        print("Initial demo state was unsolvable.")
    
    print("\n" + "="*60)
    print("-------------------- STARTING 10-RUN EVALUATION --------------------")
    print("="*60)

    # 2. Execute the Final Evaluation (10 Runs + Comparison + Plotting)
    # This function uses the code we built in the previous step
    run_final_evaluation()