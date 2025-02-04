import heapq
import numpy as np
import copy

initial_State = []
goal_State = [[1,2,3],
              [4,5,6],
              [7,8,0]]
goal_coor = {}
for r in range (len(goal_State)):
    for c in range (len(goal_State[0])):
        goal_coor[goal_State[r][c]] = (r,c)

#print('goal_coor', goal_coor)
class Node:
    def __init__(self, parent=None, board = None, cost = 0, depth = 0):
        self.board = board
        self.parent = parent
        self.cost = cost #g(n)
        self.depth = depth #f(n) = g(n) + h(n)

    def __lt__(self, other): # compare nodes based on cost for heapq
        return self.depth < other.depth
    
    def children(self):
        directions = [(-1,0), (1,0), (0,1), (0,-1)]
        childrn_nodes = []
        x = 0
        y = 0
        for i in range(3): # find the coordinates for 0, (i, j)
            for j in range(3):
                if self.board[i][j] == 0:
                    x = i
                    y = j
        for d in directions:
            new_i = x + d[0]
            new_j = y + d[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3: #check if new_i, new_j is in the matrix
                new_board = copy.deepcopy(self.board) #deep copy the board
                #swap the 0 with the new_i, new_j
                new_board[x][y], new_board[new_i][new_j] = new_board[new_i][new_j], new_board[x][y]
                child_node = Node(self, new_board, self.cost+1, self.depth+1)  #make a node from the matrix
                #print("child depth: ", child_node.cost)
                
                childrn_nodes.append(child_node) #append the new board to the result
                # print(new_i, new_j, x, y)
                # child_node.print_puzzle()
        return childrn_nodes
    
    def board_to_tuple(self):  #converts board to tuple to put into dict()
        return tuple(tuple(row) for row in self.board)
    
    def print_puzzle(self):
        print("g(n) = ", self.cost, ", h(n) = ", self.depth - self.cost)
        print("f(n) = ", self.depth)
        print(np.array(self.board), "\n")

    def misplaced_count(self):
        sum = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    if self.board[i][j] != goal_State[i][j]:
                        sum += 1
        return sum
    
    def manhattan_count(self):
        sum_distance = 0
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x1, y1 =  goal_coor[self.board[i][j]]
                    distance = abs(i - x1) + abs(j - y1) #sum abs diff in row and col
                    sum_distance += distance
                    #print(f"Tile {self.board[i][j]}: Current ({i},{j}), Goal ({x1},{y1}), Distance = {distance}")
        #print("manhattan: ", sum_distance)
        self.depth = self.cost + sum_distance
        return sum_distance

def general_search(puzzle, heuristic):
    repeat_states = dict()
    priority_queue = []
    curr_node= Node(None, puzzle, 0, 0) #make initial state a board, then make it a node, then push into queue
    if heuristic == 1:
        curr_node.depth = curr_node.cost + curr_node.misplaced_count()
    if heuristic == 2:
        curr_node.manhattan_count()
    heapq.heappush(priority_queue, curr_node) #push into queue 

    num_pops = 0 #time
    max_queue_size = 0 #memory
    repeat_states[curr_node.board_to_tuple()] = "repeat"

    #loop
    while len(priority_queue):
        max_queue_size = max(max_queue_size, len(priority_queue))
        curr_node = heapq.heappop(priority_queue) #pop first node in the queue
        num_pops += 1

        #print("\npop")
        #curr_node.print_puzzle()
        #print("\nDepth:", curr_node.cost, "\n")

        if curr_node.board == goal_State:  #if popped node is goal state return the node 
            solution_path = []
            node = curr_node  
            while node: 
                solution_path.append(node)
                node = node.parent  # Move to parent
            for step, node in enumerate(reversed(solution_path)): # print path in correct order from start to goal
                #print(f"Step {step}:")
                #node.manhattan_count()
                node.print_puzzle()

            print("Goal state!\n")
            print("Solution depth: ", curr_node.cost)
            print("Time (number of nodes expanded): ", num_pops)
            print("Memory (Max queue size): ", max_queue_size)
            return
        #expand the children, put them into queue
        children = curr_node.children() #is a list of nodes
        #   iterate through list of nodes
        #if its in repeat, dont add to queue, so do nothing
        #its not in repeat, add to queue and add to repeat
        for c in children:
            if c.board_to_tuple() not in repeat_states:
                #print("added to queue")
                if heuristic == 1: #misplaced tile
                    c.depth = c.cost + c.misplaced_count()
                    # print("current depth: ", c.cost)
                    # print("misplace = ", c.misplaced_count())
                    # print("f(n): ", c.depth)
                elif heuristic == 2:
                    #c.depth = c.cost + c.manhattan_count()
                    c.manhattan_count()
                    #print("current depth: ", c.cost)
                    #print("f(n): ", c.depth)
                heapq.heappush(priority_queue, c)
                repeat_states[c.board_to_tuple()] = "repeat"
                #print("-" * 30)
            # else:
            #     print("its a repeat")

    print("failure")
    return

    #end

def select_init_alg(puzzle):
    alg = input("(1) Uniform Cost Search\n"
                "(2) A* with Misplaced Tile heuristic\n"
                "(3) A* with Manhattan Distance heuristic\n")
    if alg == "1":
        general_search(puzzle, 0)
    elif alg == "2":
        general_search(puzzle, 1)
    elif alg == "3":
        general_search(puzzle, 2)

def main():
    depth0 = goal_State
    easy = [[1,2,0],
            [4,5,3],
            [7,8,6]]
    very_easy = [[1,2,3],
                 [4,5,6],
                 [7,0,8]]
    doable = [[0,1,2],
              [4,5,3],
              [7,8,6]]
    oh_boy = [[8,7,1],
              [6,0,2],
              [5,4,3]]
    depth2 = [[1,2,3],
              [4,5,6],
              [0,7,8]]
    depth4 = [[1,2,3],
              [5,0,6],
              [4,7,8]]
    depth8 = [[1,3,6],
              [5,0,2],
              [4,7,8]]
    depth12 = [[1,3,6],
               [5,0,7],
               [4,8,2]]
    depth16 = [[1,6,7],
               [5,0,3],
               [4,8,2]]
    depth20 = [[7,1,2],
               [4,8,5],
               [6,3,0]]
    depth24 = [[0,7,2],
               [4,6,1],
               [3,5,8]]
    bonus = [[1,6,7],
             [5,0,3],
             [4,8,2]]


    print("Welcome to Ramya's 8-Puzzle.")
    choose = input("Type \'1\' to use a default puzzle, or \'2\' to create your own.\n")

    if choose == "2":
        print("Enter your puzzle, using a zero to represent the blank.", end=" ") 
        print("Enter valid 8-puzzles. Enter the puzzle demilimiting", end=" ")
        print("the numbers with a space.")

        entries = ""
        entries += input("Enter first row: ") + " "
        entries += input("Enter second row: ") + " "
        entries += input("Enter third row: ")

        #print(entries)

        numbers = list(map(int, entries.split()))
        entered = [numbers[i:i+3] for i in range(0, 9, 3)] #make the list a 3x3 array
        #print(entered)
        initial_State = entered
        #print("initial_State = ", initial_State)

    depth_map = {
            "a" : easy,
            "b": very_easy,
            "c": doable,
            "d": oh_boy,
            "0": depth0,
            "2": depth2,
            "4": depth4,
            "8": depth8,
            "12": depth12,
            "16": depth16,
            "20": depth20,
            "24": depth24,
            "bonus": bonus
        }

    if choose == "1":
        start = input("Enter # 0, 2, 4, 8, 12, 16, 20, or 24 for depth: You can also enter a, b, c, d, bonus\n")
        initial_State = depth_map.get(start)

    #print(initial_State)
    select_init_alg(initial_State)

main()