import time

class Node:
    def __init__(self, st=[[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,1,2,2]], prt=None, pCost=0):
        self.state = st
        self.parent = prt
        self.action = None
        self.pathCost = pCost # g
        self.h = 160 # initial state

    def __lt__(self, other):
        return self.h < other.h # min heap

goal = [[2,2,0,0,0,2,2],[2,2,0,0,0,2,2],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,2,2],[2,2,0,0,0,2,2]]

def goalTest(state):
    return state == goal

def ED(i, j):
    H = abs(3-j)
    V = abs(3-i)
    return 2 ** max(H, V)

Total_nodes_expanded = 0

def getSuccessors(node):
    ans = []
    dx_2_cell = [0,0,2,-2]
    dy_2_cell = [-2,2,0,0]
    dx_1_cell = [0,0,1,-1]
    dy_1_cell = [-1,1,0,0]
    for i in range(7):
        for j in range(7):
            if node.state[i][j] == 1:
                for k in range(4):
                    cell2i = i + dy_2_cell[k]
                    cell2j = j + dx_2_cell[k]
                    cell1i = i + dy_1_cell[k]
                    cell1j = j + dx_1_cell[k]
                    if(cell2i<0 or cell2i>=7 or cell2j<0 or cell2j>=7):
                        continue
                    if(node.state[cell1i][cell1j] == 0):
                        continue
                    if(node.state[cell2i][cell2j] == 0):
                        stateCpy = [obj.copy() for obj in node.state]
                        child = Node(stateCpy, node, node.pathCost + 1)
                        child.state[cell2i][cell2j] = 1
                        child.state[cell1i][cell1j] = 0
                        child.state[i][j] = 0
                        child.action = [[i,j],[cell2i,cell2j]]
                        chr = node.h
                        chr -= ED(i, j)
                        chr -= ED(cell1i, cell1j)
                        chr += ED(cell2i, cell2j)
                        child.h = chr
                        ans.append(child)
                        global Total_nodes_expanded
                        Total_nodes_expanded += 1
    return ans

def displayBoard(state):
    for row in state:
        print(row)

def usingBestFirstSearch():
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
        if goalTest(curr.state) == True:
            print("Search ended")
            return curr
        children = getSuccessors(curr)
        for child in children:
            if (child.state in explored) == False:
                frontier.append(child)
        explored.append(curr.state)

print("Search started")
start_node = Node()
print("Initial Matrix:")
displayBoard(start_node.state)
start_time = time.time()
ans = usingBestFirstSearch()
end_time = time.time()
elapsed_time = end_time - start_time
print("Time taken: ", elapsed_time)
print()
displayBoard(ans.state)
