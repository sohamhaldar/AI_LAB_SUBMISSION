import numpy as np
import random
import math


def calculate_cost(piece1, piece2, direction):
    """
    Calculate the mismatch cost between two pieces based on their edge pixels.
    Direction can be "right" (piece2 is to the right of piece1) or "down" (piece2 is below piece1).
    """
    if direction == 'right':
        return np.sum(np.abs(piece1[:, -1] - piece2[:, 0]))  
    elif direction == 'down':
        return np.sum(np.abs(piece1[-1, :] - piece2[0, :]))  
    return 0


def compute_total_cost(arrangement, puzzle_pieces):
    total_cost = 0
    rows, cols = arrangement.shape
    for i in range(rows):
        for j in range(cols):
            if j < cols - 1:  
                total_cost += calculate_cost(puzzle_pieces[arrangement[i, j]], puzzle_pieces[arrangement[i, j + 1]], 'right')
            if i < rows - 1:  
                total_cost += calculate_cost(puzzle_pieces[arrangement[i, j]], puzzle_pieces[arrangement[i + 1, j]], 'down')
    return total_cost


def generate_neighbor(arrangement):
    neighbor = arrangement.copy()
    rows, cols = arrangement.shape
    i1, j1 = random.randint(0, rows - 1), random.randint(0, cols - 1)
    i2, j2 = random.randint(0, rows - 1), random.randint(0, cols - 1)
   
    neighbor[i1, j1], neighbor[i2, j2] = neighbor[i2, j2], neighbor[i1, j1]
    return neighbor

def simulated_annealing(puzzle_pieces, initial_temp, cooling_rate, max_iterations):
    rows, cols = int(np.sqrt(len(puzzle_pieces))), int(np.sqrt(len(puzzle_pieces)))
    
    current_arrangement = np.random.permutation(rows * cols).reshape(rows, cols)
    
    current_cost = compute_total_cost(current_arrangement, puzzle_pieces)
    best_arrangement = current_arrangement.copy()
    best_cost = current_cost
    
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        new_arrangement = generate_neighbor(current_arrangement)
        new_cost = compute_total_cost(new_arrangement, puzzle_pieces)
        
        if new_cost < current_cost:
            current_arrangement = new_arrangement
            current_cost = new_cost
            if new_cost < best_cost:
                best_arrangement = new_arrangement.copy()
                best_cost = new_cost
        else:
            acceptance_probability = math.exp((current_cost - new_cost) / temperature)
            if random.random() < acceptance_probability:
                current_arrangement = new_arrangement
                current_cost = new_cost
        
        temperature *= cooling_rate
        
        if temperature < 1e-3:
            break
    
    return best_arrangement, best_cost


puzzle_pieces = np.random.randint(0, 255, (9, 28, 28)) 


initial_temp = 100.0  
cooling_rate = 0.95   
max_iterations = 10000 


best_arrangement, best_cost = simulated_annealing(puzzle_pieces, initial_temp, cooling_rate, max_iterations)

print("Best arrangement found:")
print(best_arrangement)
print("Best cost:", best_cost)
