#import TreeNode
import heapq as min_heap_esque_queue
import numpy as np

depth0 = [[],[],[]]

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

    print(entries)

    entered = list(map(int, entries.split()))
    initial_State = np.array(entered).reshape(3,3)
    print(initial_State)

if puzzle == "1":






