from collections import deque
 
def is_valid(state):
    m1, c1, _, m2, c2, _ = state
    if (m1 >= c1 or m1 == 0) and (m2 >= c2 or m2 == 0):
        return True
    return False
 
def get_successors(state):
    successors = []
    m1, c1, b1, m2, c2, b2 = state
   
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
   
    if b1 == 1:
        for m, c in moves:
            new_state = (m1 - m, c1 - c, 0, m2 + m, c2 + c, 1)
            if is_valid(new_state):
                successors.append(new_state)
    else:  
        for m, c in moves:
            new_state = (m1 + m, c1 + c, 1, m2 - m, c2 - c, 0)
            if is_valid(new_state):
                successors.append(new_state)
   
    return successors
 
def bfs(initial_state):
    queue = deque([(initial_state, [])])
    visited = set()
   
    while queue:
        state, path = queue.popleft()
       
        if state in visited:
            continue
       
        visited.add(state)
        path = path + [state]
       
       
        if state == (0, 0, 0, 3, 3, 1):
            return path
        for successor in get_successors(state):
            queue.append((successor, path))
    return None
 
initial_state = (3, 3, 1, 0, 0, 0)
solution = bfs(initial_state)
if solution:
    for step in solution:
        print(step)
else:
    print("No solution found.")
 
