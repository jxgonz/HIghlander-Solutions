import pandas as pd
import numpy as np
from container import Container

class Node:
  def __init__(self, state, parent=None, g=0, h=0):
    self.state = state
    self.parent = parent
    self.g = g
    self.h = h

  def f(self):
    return self.g + self.h



class Tree:
  def __init__(self, root):
    self.root = root

class Crane:
  def __init__(self, position, empty):
    self.position = position
    self.empty = empty

class Problem:
  def __init__(self, manifest, offloadShip, loadShip):
    self.manifest = manifest
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    self.operators = [
      (-1, 0), #move container left
      (1, 0),  #move container right
      (0, -1), #move container down
      (0, 1),  #move container up
      ]
    
  def goal_test(self):
    if self.offloadShip in dict.values():
      return False
    else:
      if self.loadShip in dict.values():
        return True
      else:
        return False
      
  def apply_operator(self, state, crane, operator):
    print(crane.position)

    # vals = []
    # counter = 0
    # for y in range(8):
    #   if state[crane.position[0], y + 1] == "NAN" or state[crane.position[0], y + 1] == "UNUSED":
    #     counter += 1
    #   vals.append(state[crane.position[0], y + 1])
    
    # if counter != 8:
    #   for y in range(8,0,-1):
    #     if state[crane.position[0], y] != "UNUSED" and state[crane.position[0], y] != "NAN":
    #       crane.position = (crane.position[0],y)
    #       crane.empty = False
    #       break

    #
    new_x = crane.position[0] + operator[0]
    new_y = crane.position[1] + operator[1]

    print(state[new_x][new_y])
    # if state[new_x][new_y] == "UNUSED":
    #   print("unused")

    # Check if new crane position is invalid
    if new_x < 0 or new_x > 38 or new_y < 0 or new_y > 9:
      return None
    if state[new_x][new_y] != "UNUSED":
      return None

    crane.position = (new_x, new_y)

    print(crane.position)



# def uniform_cost(problem):
#   maxLength = 0
#   root = Node(problem.initial_manifest, None, 0, 0)
#   tree = Tree(root)
#   frontier = {root}
#   explored = set()

#   while len(frontier) != 0:
#     current_node = min(frontier, key=lambda node: node.f())
#     maxLength = max(len(frontier), maxLength)
#     frontier.remove(current_node)

#     if problem.goal_test(current_node.state):
#       print(current_node.state)
  
#     explored.add(current_node)

#     for operator in problem.operators:
#       new_state = problem.apply_operator(current_node.state, operator)

#       if new_state is None:
#         continue

#       new_node = Node(new_state, current_node, 0, 0)

#       new_node.g = current_node.g
#       # new_node.h = problem

#       if new_node in explored or new_node in frontier:
#         continue

#       frontier.add(new_node)


def driver():
  fileName = "Port_Project/ShipCase1.txt"
  data = pd.read_csv(fileName, header=None)

  data[0] = data[0].str.strip('[')
  data[1] = data[1].str.strip(']')
  data[3] = data[3].str.strip()

  data[0] = pd.to_numeric(data[0])
  data[1] = pd.to_numeric(data[1])

  SHIPHEIGHT = 8
  SHIPWIDTH = 12

  # Rows, Columns
  x,y = (39, SHIPHEIGHT + 1)

# 2D Array for entire layout
  board = []
  for r in range(x):
    row = []
    for c in range(y):
      row.append(Container("BLANK",(),False,False))
    board.append(row)
    row = None

  # print(np.matrix(board))

  # arr = np.ndarray(shape=(39,SHIPHEIGHT+1))
  # arr[0][1] = 3.5
  # print(arr[0][1])

  # x - > column
  # y - > row
  # BUFFER SETUP
  for i in range(24):
    for j in range(9):
      # print(i, j)
      if j < 4:
        board[i][j] = Container("NAN", (i,j), False, False)
      else:
        board[i][j] = Container("UNUSED", (i,j), False, False)
      # Creates a NAN Container at (i,j)
  
  # MIDDLE PSEUDO EMPTY SPACE SETUP
  for i in range(24, 27):
    for j in range(y):
      if j < SHIPHEIGHT:
        board[i][j] = Container("NAN", (i,j), False, False)
      else:
        board[i][j] = Container("UNUSED", (i,j), False, False)
  
  # LOAD CELL
  board[25][y - 1] = Container("LOADBOX", (25,y - 1), False, False)

  # TRANSFER CELL
  board[27][y - 1] = Container("VIRTUALTRANSFER", (27,y - 1), False, False)

  # SHIP SETUP


  k = 0
  for i in range(y - 1):
    for j in range(27, 27 + SHIPWIDTH):
      containerName = data.at[k,3]
      board[j][i] = Container(containerName, (j,i), False, False)
      # Creates a Container at (i, j) that still needs to be told
      # if needed to be unloaded or loaded (if at all needed)
      k = k + 1
  
  for i in range(27, 27 + SHIPWIDTH):
    board[i][8] = Container("UNUSED", (i,9), False, False)

  # print(np.matrix(board))

  # dict = {}
  # for i in data.index:
  #   dict[(data.at[i, 1], data.at[i, 0])] = data.at[i, 3]

  crane = Crane((27,8), True)
  problem = Problem(board, 0, 0)

  problem.apply_operator(board, crane, problem.operators[2])

  # # for x in range(12):
  # #   problem.n_column_container_search(dict, crane)

driver()