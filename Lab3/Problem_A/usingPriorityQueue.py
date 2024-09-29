import time

class Node:
    def __init__(self, st=[[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,
    1,2,2]], prt=None, pCost=0):
        self.state = st
        self.parent = prt
        self.pathCost = pCost # g
        
    def __lt__(self, other):
        return self.pathCost < other.pathCost 

goal = [[2,2,0,0,0,2,2],[2,2,0,0,0,2,2],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,2,2],[2,2,0,0,0,2,2]]

def checkIfFinal(state):
    return state == goal

def getSuccessors(node):
    ans = []
    # Define possible moves: up, down, right, left
    dx_2_cell = [0, 0, 2, -2]
    dy_2_cell = [-2, 2, 0, 0]
    dx_1_cell = [0, 0, 1, -1]
    dy_1_cell = [-1, 1, 0, 0]
    for i in range(7):
        for j in range(7):
            if node.state[i][j] == 1: # Check if the cell contains the movable object
                for k in range(4):
                    cell2i = i + dy_2_cell[k]
                    cell2j = j + dx_2_cell[k]
                    cell1i = i + dy_1_cell[k]
                    cell1j = j + dx_1_cell[k]
                    # Check if the new positions are within the bounds of the board
                    if cell2i < 0 or cell2i >= 7 or cell2j < 0 or cell2j >= 7:
                        continue
                    # Check if the adjacent cell is empty
                    if node.state[cell1i][cell1j] == 0:
                        continue
                    # Check if the destination cell is empty
                    if node.state[cell2i][cell2j] == 0:
                        # Create a copy of the current state to avoid modifying the original state
                        stateCpy = [obj.copy() for obj in node.state]
                        # Create a new child node
                        child = Node(stateCpy, node, node.pathCost + 1)
                        # Move the object to the new position
                        child.state[cell2i][cell2j] = 1
                        child.state[cell1i][cell1j] = 0
                        child.state[i][j] = 0
                        # Store the action taken to reach this state
                        # Add the child node to the list of successors
                        ans.append(child)
    return ans

def displayBoard(state):
    for row in state:
        print(row)

def UsingPiorityQueue():
    start_node = Node()
    frontier = [] # keep nodes
    explored = [] # keep states which are explored
    frontier.append(start_node)
    while True:
        if len(frontier) == 0:
            return None
        curr = frontier.pop()
        if curr.state in explored:
            continue
        if checkIfFinal(curr.state) == True:
            print("Search ended")
            return curr
        children = getSuccessors(curr)
        for child in children:
            if (child.state in explored) == False:
                frontier.append(child)
        explored.append(curr.state)

start_node = Node()
print("Initial Matrix:")
displayBoard(start_node.state)
start_time = time.time()
ans = UsingPiorityQueue()
end_time = time.time()
elapsed_time = end_time - start_time
print("Goal Matrix:")
displayBoard(ans.state)
print()
print("Time taken: ", elapsed_time)