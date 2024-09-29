class State:
    def __init__(self, missionaries, cannibals, boat):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat
 
    def is_valid(self):
        if self.missionaries < 0 or self.cannibals < 0 or self.missionaries > 3 or self.cannibals > 3:
            return False
        if self.missionaries > 0 and self.missionaries < self.cannibals:
            return False
        if (3 - self.missionaries) > 0 and (3 - self.missionaries) < (3 - self.cannibals):
            return False
        return True
 
    def is_goal(self):
        return self.missionaries == 0 and self.cannibals == 0 and self.boat == 0
 
    def __eq__(self, other):
        return (self.missionaries == other.missionaries and
                self.cannibals == other.cannibals and
                self.boat == other.boat)
 
    def __hash__(self):
        return hash((self.missionaries, self.cannibals, self.boat))
 
    def __str__(self):
        return f"({self.missionaries}, {self.cannibals}, {self.boat})"
 
def successors(state):
    children = []
    if state.boat == 1:
        new_states = [
            State(state.missionaries - 2, state.cannibals, 0),
            State(state.missionaries, state.cannibals - 2, 0),
            State(state.missionaries - 1, state.cannibals - 1, 0),
            State(state.missionaries - 1, state.cannibals, 0),
            State(state.missionaries, state.cannibals - 1, 0)
        ]
    else:
        new_states = [
            State(state.missionaries + 2, state.cannibals, 1),
            State(state.missionaries, state.cannibals + 2, 1),
            State(state.missionaries + 1, state.cannibals + 1, 1),
            State(state.missionaries + 1, state.cannibals, 1),
            State(state.missionaries, state.cannibals + 1, 1)
        ]
 
    for new_state in new_states:
        if new_state.is_valid():
            children.append(new_state)
    return children
 
def dfs(initial_state):
    stack = [(initial_state, [])]
    visited = set()
 
    while stack:
        current_state, path = stack.pop()
        if current_state.is_goal():
            return path + [current_state]
 
        if current_state in visited:
            continue
 
        visited.add(current_state)
 
        for child in successors(current_state):
            if child not in visited:
                stack.append((child, path + [current_state]))
    return None
initial_state = State(3, 3, 1)
solution = dfs(initial_state)
if solution:
    for state in solution:
        print(state)
else:
    print("No solution found.")
 
