#import TreeNode
import heapq
import numpy as np
import copy

initial_State = []
goal_State = [[1,2,3],
              [4,5,6],
              [7,8,0]]

#Definition for a tree node.
class Node:
    def __init__(self, parent=None, board = None, cost = 0, depth = 0):
        self.board = board
        self.parent = parent
        self.cost = cost 
        self.depth = depth #f(n) = g(n) + h(n)
    # compare nodes based on cost for heapq
    def __lt__(self, other):
        return self.depth < other.depth
    def children(self):
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        childrn_nodes = []
        # find the coordinates for 0, (i, j)
        x = 0
        y = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    x = i
                    y = j
        for d in directions:
            new_i = x + d[0]
            new_j = y + d[1]
            #check if new_i, new_j is in the matrix
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                #deep copy the board
                new_board = copy.deepcopy(self.board)
                #swap the 0 with the new_i, new_j
                new_board[x][y], new_board[new_i][new_j] = new_board[new_i][new_j], new_board[x][y]
                #make a node from the matrix
                child_node = Node(self, new_board, 0, self.depth+1)
                print("child cost: ", child_node.depth)
                #append the new board to the result
                childrn_nodes.append(child_node)
                print(new_i, new_j, x, y)
                print("child")
                child_node.print_puzzle()
        return childrn_nodes
    #converts board to tuple to put into dict()
    def board_to_tuple(self): 
        return tuple(tuple(row) for row in self.board)
    def print_puzzle(self):
        print(np.array(self.board), "\n")
    def misplaced_count(self):
        sum = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    if self.board[i][j] != goal_State[i][j]:
                        sum += 1
        self.depth+=sum
        print("misplaced = ", sum)
        return sum
    #def manhattan_count(self):

# directions = [(0,1), (0,-1), (1,0), (-1,0)]
# find the coordinates for 0, (i, j)
# for d in directions:
# new_i = i + d[0]
# new_j = j + d[1]
# check if new_i, new_j is in the matrix
# generate the new board
#     deep copy the board
#     swap the 0 with the new_i, new_j
#     make a node from the matrix
#     append the new board to the result

def general_search(puzzle, heuristic):
    #make initial state a board, then make it a node, then push into queue 
    repeat_states = dict()
    priority_queue = []
    curr_node= Node(None, puzzle, 0, 0)
    if heuristic == 1:
        curr_node.misplaced_count()
    # if heuristic == 2:
    #     curr_node.manhattan_count()
    heapq.heappush(priority_queue, curr_node)
    #priority_queue.append(curr_node) #push into queue

    num_expanded_nodes = 0
    max_queue_size = 0
    repeat_states[curr_node.board_to_tuple()] = "repeat"

    #loop
    while len(priority_queue):
        #if theres nothing in the queue return failure
        #pop first node in the queue
        curr_node = heapq.heappop(priority_queue)#priority_queue.pop(0)
        curr_node.print_puzzle()
        print("\n", curr_node.depth, "\n")
        #if popped node is goal state return the node 
        if curr_node.board == goal_State:
            print("goal state")
            return
        #expand the children, put them into queue
        children = curr_node.children() #is a list of nodes
        #   iterate through list of nodes
        #if its in repeat, dont add to queue
        #its not in repeat, add to queue and add to repeat
        for c in children:
            if c.board_to_tuple() not in repeat_states:
                print("added to queue")
                #if heuristic == 0:
                if heuristic == 1: #misplaced tile
                    c.misplaced_count()
                # or you need to push into queue based on least miisplaced tiles 
                # if heuristic == 2:
                #     c.manhattan_count()
                heapq.heappush(priority_queue, c)#priority_queue.append(c)
                repeat_states[c.board_to_tuple()] = "repeat"
            else:
                print("its a repeat")

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


    print("Welcome to Ramya's 8-Puzzle. ")
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
        # initial_State = np.array(entered).reshape(3,3)
        #print("initial_State = ", initial_State)

    depth_map = {
            "2": depth2,
            "4": depth4,
            "8": depth8,
            "12": depth12,
            "16": depth16,
            "20": depth20,
            "24": depth24
        }

    if choose == "1":
        start = input("Enter # 0, 2, 4, 8, 12, 16, 20, or 24 for depth: \n")
        initial_State = depth_map.get(start)

    print(initial_State)
    select_init_alg(initial_State)

main()