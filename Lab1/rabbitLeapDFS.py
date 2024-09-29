def is_valid_move(state, i, j):
    if i < j and state[i] == 'W' and state[j] == '_':  # Correcting space to '_'
        return True
    if i > j and state[i] == 'E' and state[j] == '_':  # Consistently checking for '_'
        return True
    return False

def get_neighbors(state):
    neighbors = []
    index = state.index('_')  # Fixing the typo here
    for step in [-2, -1, 1, 2]:
        new_index = index + step
        if 0 <= new_index < len(state) and is_valid_move(state, new_index, index):
            new_state = list(state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append("".join(new_state))
    return neighbors

def dfs_recursive(current_state, target_state, visited, path):
    if current_state == target_state:
        return path + [current_state]

    visited.add(current_state)

    for neighbor in get_neighbors(current_state):
        if neighbor not in visited:
            result = dfs_recursive(neighbor, target_state, visited, path + [current_state])
            if result:
                return result

    return None

start_state = "WWW_EEE"  # Initial configuration
target_state = "EEE_WWW"  # Corrected target configuration with consistent '_'
visited = set()
solution_path = dfs_recursive(start_state, target_state, visited, [])

if solution_path:
    print("Solution path:")
    for state in solution_path:
        print(state)
    print(f"Number of steps: {len(solution_path) - 1}")
else:
    print("No solution found.")
