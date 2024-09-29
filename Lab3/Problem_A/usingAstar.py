import time

class Node:
    def __init__(self, st=[[2,2,1,1,1,2,2],[2,2,1,1,1,2,2],[1,1,1,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,1,1,1],[2,2,1,1,1,2,2],[2,2,1,1,1,2,2]], prt=None, pCost=0):
        self.state = st
        self.parent = prt
        self.action = None
        self.pathCost = pCost # g
        self.h = 88 # initial state
        self.f = self.pathCost + self.h

    def __lt__(self, other):
        return self.f < other.f # min heap

goal = [[2,2,0,0,0,2,2],[2,2,0,0,0,2,2],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,2,2],[2,2,0,0,0,2,2]]

def goalTest(state):
    return state == goal

def MD(i,j):
    return abs(3-i) + abs(3-j)

Total_nodes_expanded = 0

def getSuccessors(node):
    ans = []
    dx2 = [0,0,2,-2]
    dy2 = [-2,2,0,0]
    dx1 = [0,0,1,-1]
    dy1 = [-1,1,0,0]
    for i in range(7):
        for j in range(7):
            if node.state[i][j]==1:
                for k in range(4):
                    c2i = i+dy2[k]
                    c2j = j+dx2[k]
                    c1i = i+dy1[k]
                    c1j = j+dx1[k]
                    if(c2i<0 or c2i>=7 or c2j<0 or c2j>=7):
                        continue
                    if(node.state[c1i][c1j]==0):
                        continue
                    if(node.state[c2i][c2j]==0):
                        stateCpy = [obj.copy() for obj in node.state]
                        child = Node(stateCpy, node, node.pathCost+1)
                        child.state[c2i][c2j]=1
                        child.state[c1i][c1j]=0
                        child.state[i][j]=0
                        child.action = [[i,j],[c2i,c2j]]
                        chr = node.h
                        chr -= MD(i,j)
                        chr -= MD(c1i,c1j)
                        chr += MD(c2i,c2j)
                        child.h = chr
                        child.f = child.pathCost + child.h
                        ans.append(child)
                        global Total_nodes_expanded
    return ans

def displayBoard(state):
    for row in state:
        print(row)

def aStar():
    start_node = Node()
    frontier = [] # keep nodes
    explored = [] # keep states which are explored
    frontier.append(start_node)
    while True:
        if len(frontier)==0:
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
ans = aStar()
end_time = time.time()
elapsed_time = end_time - start_time
print("Time taken: ",elapsed_time)
print()
displayBoard(ans.state)
