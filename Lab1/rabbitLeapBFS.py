from collections import deque

def is_valid_move(state, i, j):
    if i < j and state[i] == 'W' and state[j] == '_':
        return True
    if i > j and state[i] == 'E' and state[j] =='_':
        return True
    return False

def get_neighbors(state):
    neighbors = []
    index = state. index('_')
    for step in [-2, -1, 1, 2]:
        new_index = index + step
        if 0 <= new_index < len(state) and is_valid_move(state, new_index, index):
            new_state = list(state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append("".join(new_state))
    return neighbors

def bfs(start, target):
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)
    while queue:
        current_state, path = queue. popleft()
        if current_state == target:
            return path + [current_state]

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue. append((neighbor, path + [current_state]))

    return None

start_state = "WWW_EEE"
target_state = "EEE_WWW"

solution_path = bfs(start_state, target_state)

print("Solution path:")
for state in solution_path:
    print(state)
print(f"Number of steps: {len(solution_path)-1}")