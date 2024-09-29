import numpy as np
from copy import deepcopy
import random

# Goal State for the 8-puzzle
GOAL_STATE = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])

def h1(curr_state, goal_state):
    """
    Heuristic for calculating the distance of goal state using Manhattan distance.
    """
    goal_indices = np.argsort(goal_state.reshape(-1, 1), axis=0)
    curr_indices = np.argsort(curr_state.reshape(-1, 1), axis=0)
    
    x = abs(goal_indices // 3 - curr_indices // 3)
    y = abs(goal_indices % 3 - curr_indices % 3)
    h = np.sum(x + y)
    
    return h

def h2(curr_state, goal_state):
    """
    Heuristic for calculating the distance of goal state using number of misplaced tiles.
    """
    return np.sum(curr_state != goal_state)

def generate_instance(goal_state, depth, debug=False):
    """
    Generates a random instance of the 8-puzzle at the given depth from the goal state.
    """
    x_prev, y_prev = np.array(np.where(goal_state == 0)).reshape(-1)
    curr_state = np.copy(goal_state)
    visited = [curr_state.reshape(-1).tolist()]
    n = depth

    if debug:
        print(f"Depth: {depth - n}")
        print(f"h1 value: {h1(curr_state, goal_state)}\th2 value: {h2(curr_state, goal_state)}")
        print(curr_state, end='\n\n')

    while n:
        possible_states = []
        if x_prev > 0:
            possible_states.append([x_prev - 1, y_prev])
        if x_prev < 2:
            possible_states.append([x_prev + 1, y_prev])
        if y_prev > 0:
            possible_states.append([x_prev, y_prev - 1])
        if y_prev < 2:
            possible_states.append([x_prev, y_prev + 1])

        x_new, y_new = random.choice(possible_states)
        curr_state[x_new, y_new], curr_state[x_prev, y_prev] = curr_state[x_prev, y_prev], curr_state[x_new, y_new]

        # Convert the current state to a list
        curr_state_list = curr_state.reshape(-1).tolist()
        
        # Check if current state has been visited
        if curr_state_list not in visited:
            visited.append(curr_state_list)
            n -= 1
            if debug:
                step = "Down" if x_new > x_prev else "Up" if x_new < x_prev else "Right" if y_new > y_prev else "Left"
                print(f"Depth: {depth - n}\tStep taken to reach: {step}")
                print(f"h1 value: {h1(curr_state, goal_state)}\th2 value: {h2(curr_state, goal_state)}")
                print(curr_state, end='\n\n')
            x_prev, y_prev = x_new, y_new
        else:
            curr_state[x_new, y_new], curr_state[x_prev, y_prev] = curr_state[x_prev, y_prev], curr_state[x_new, y_new]

    return curr_state

def get_possible_moves(curr_state):
    """
    Returns a list of possible states after valid moves from current state.
    """
    row, col = np.array(np.where(curr_state == 0)).reshape(-1)
    possible_moves = []
    
    if row > 0:  # Up
        next_state = curr_state.copy()
        next_state[row, col], next_state[row - 1, col] = next_state[row - 1, col], next_state[row, col]
        possible_moves.append(next_state)
    if row < 2:  # Down
        next_state = curr_state.copy()
        next_state[row, col], next_state[row + 1, col] = next_state[row + 1, col], next_state[row, col]
        possible_moves.append(next_state)
    if col > 0:  # Left
        next_state = curr_state.copy()
        next_state[row, col], next_state[row, col - 1] = next_state[row, col - 1], next_state[row, col]
        possible_moves.append(next_state)
    if col < 2:  # Right
        next_state = curr_state.copy()
        next_state[row, col], next_state[row, col + 1] = next_state[row, col + 1], next_state[row, col]
        possible_moves.append(next_state)

    return possible_moves

def solve(curr_state, goal_state, heuristic=1):
    """
    Solves the puzzle by finding a path from current state to the goal state using the specified heuristic.
    """
    visited = []
    frontier = [curr_state.reshape(-1).tolist()]
    parent_map = {tuple(curr_state.reshape(-1).tolist()): None}  # To track the path

    while not np.array_equal(curr_state, goal_state):
        print(curr_state, end="\n\n")
        possible_moves = get_possible_moves(curr_state)

        for move in possible_moves:
            curr_move = move.reshape(-1).tolist()
            if curr_move not in frontier and curr_move not in visited:
                frontier.append(curr_move)
                parent_map[tuple(curr_move)] = tuple(curr_state.reshape(-1).tolist())  # Track parent

        if not frontier:
            print("STRUCK!!!")
            return

        visited.append(curr_state.reshape(-1).tolist())
        
        if heuristic == 1:
            frontier = sorted(frontier, key=lambda x: h1(np.array(x).reshape(3, 3), goal_state))
        elif heuristic == 2:
            frontier = sorted(frontier, key=lambda x: h2(np.array(x).reshape(3, 3), goal_state))

        curr_state = np.array(frontier.pop(0)).reshape(3, 3)

    print("GOAL REACHED!!!")

    # Backtrack to find the path taken
    path = []
    current = tuple(curr_state.reshape(-1).tolist())
    while current is not None:
        path.append(np.array(current).reshape(3, 3))
        current = parent_map[current]
    
    path.reverse()  # Reverse the path to show from initial to goal state
    print("Path to Goal State:")
    for step in path:
        print(step)

# Example usage
depth = 16
curr_state = generate_instance(GOAL_STATE, depth, debug=True)
print("Initial State:\n", curr_state)

# Solve using heuristic 1 (Manhattan distance)
solve(curr_state, GOAL_STATE, heuristic=1)
