#import TreeNode
import heapq as min_heap_esque_queue
import numpy as np

depth2 = [[1,2,3],[4,5,6],[0,7,8]]
depth4 = [[1,2,3],[5,0,6],[4,7,8]]
depth8 = [[1,3,6],[5,0,2],[4,7,8]]
depth12 = [[1,3,6],[5,0,7],[4,8,2]]
depth16 = [[1,6,7],[5,0,3],[4,8,2]]
depth20 = [[7,1,2],[4,8,5],[6,3,0]]
depth24 = [[0,7,2],[4,6,1],[3,5,8]]
# depth4 = [[],[],[]]
# depth4 = [[],[],[]]
# depth4 = [[],[],[]]
# depth4 = [[],[],[]]
# depth4 = [[],[],[]]


initial_State = []
goal_State = [[1,2,3],
                [4,5,6],
                [7,8,0]]

print("Welcome to Ramya's 8-Puzzle. ")
puzzle = input("Type \'1\' to use a default puzzle, or \'2\' to create your own.\n")

if puzzle == "2":
    print("Enter your puzzle, using a zero to represent the blank.", end="") 
    print("Please only enter valid 8-puzzles. Enter the puzzle demilimiting", end="")
    print("the numbers with a space. Type RETURN only when finished.")

    entries = ""
    entries += input("Enter first row: ") + " "
    entries += input("Enter second row: ") + " "
    entries += input("Enter third row: ")

    #print(entries)

    entered = list(map(int, entries.split()))
    initial_State = np.array(entered).reshape(3,3)
    #print(initial_State)

depth_map = {
        "2": depth2,
        "4": depth4,
        "8": depth8,
        "12": depth12,
        "16": depth16,
        "20": depth20,
        "24": depth24
    }

if puzzle == "1":
    start = input("Enter # 0, 2, 4, 8, 12, 16, 20, or 24 for depth: \n")
    initial_State = np.array(depth_map.get(start))

print(initial_State)


