import matplotlib.pyplot as plt
import random

def load_matrix(filename):
    """Load a text file into a 2D array.

    Args:
        filename (string): Filename in current folder.

    Returns:
        list: 2D list
    """
    # initialise 2D distance list
    matrix = []

    # open file
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip() # gets rid of whitespace and n/ 
            # for every line in the .txt file the values are converted to integers and added to the 2D list, the commas are neglected
            matrix.append(list(int(x) for x in line.split(','))) 
    return matrix

def path_cost(matrix, solution):
    """Calculate the cost of a solution.

    Args:
        matrix (list): Edge cost matrix
        solution (list): Node list

    Returns:
        int: Cost of traversing the solution nodes.
    """
    # initialise cost
    cost = 0

    # finds the distance between each node in the list
    for i in range(0, len(solution)):
        cost += matrix[solution[i]][solution[i - 1]]
    
    return cost

def find_random_neighbour(matrix, solution):
    """Find any random neighbour.

    Args:
        matrix (list): Edge cost matrix
        solution (list): Node list

    Returns:
        list: Neighbour with two adjacent elements swapped.
    """
    # choose a random index of the matrix
    i = random.randint(1, len(matrix)-2)

    # create new copy of the solution
    neighbour = solution.copy()

    # swap the values of the copy at the random index chosen
    neighbour[i] = solution[i+1]
    neighbour[i+1] = solution[i]

    return neighbour, path_cost(matrix, neighbour)

def hill_climbing(matrix):
    """Implement the simple hill climbing algorithm.

    Args:
        matrix (list): Edge cost matrix

    Returns:
        list: Array of all path costs found.
    """
    # initialise costs
    costs = []

    # start with list of indices in random order
    path = list(range(len(matrix)))
    random.shuffle(path)

    # counts the number of iterations where there is no solution improvement in a row
    num_same_cost = 0

    # path cost of the initial solution
    cost = path_cost(matrix, path)

    while num_same_cost < 100:
        new_path, new_cost = find_random_neighbour(matrix, path) # new potential solution
        # check if new potential solution is better than current solution
        if new_cost < cost:
            cost, path = new_cost, new_path
            num_same_cost = 0
        else:
            num_same_cost += 1

        costs.append(cost)

    return costs

matrix = load_matrix('TSP_Matrix.txt')

plt.figure()

tot_final_costs = []
for i in range(10):
    path_costs = hill_climbing(matrix) # run algorithm

    total_iterations = len(path_costs)
    final_cost = path_costs[-1]
    tot_final_costs.append(final_cost)

    print(f"Run {i+1}: path cost = {final_cost}, iterations = {total_iterations}")

    plt.plot(range(len(path_costs)), path_costs, label=f"Run {i+1}")
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.legend()

average_cost = sum(tot_final_costs)/len(tot_final_costs)
min_cost_index = tot_final_costs.index(min(tot_final_costs)) + 1

print(f"The average cost over the runs is {average_cost}")
print(f"The best run was Run {min_cost_index} = {min(tot_final_costs)}")

plt.show()