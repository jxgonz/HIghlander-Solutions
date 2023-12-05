import pandas as pd
import numpy as np
from container import Container

class Node:
  def __init__(self, state, parent=None, cost=0, g=0, h=0):
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
  def __init__(self, position):
    self.position = position
    self.empty = True
    self.container_coordinate = ()

class Problem:
  def __init__(self, manifest, offloadShip, loadShip):
    self.manifest = manifest
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    self.cost = 0
    self.g = 0
    self.h = 0
    self.operators = [
      (-1, 0), #move container left
      (1, 0),  #move container right
      (0, -1), #move container down
      (0, 1),  #move container up
      ]
    
  def goal_test(self, state):
    if self.offloadShip in state:
      return False
    else:
      if self.loadShip in state:
        return True
      else:
        return False
      
  def apply_operator(self, state, crane, operator):
    new_x = crane.position[0] + operator[0]
    new_y = crane.position[1] + operator[1]

    # Check if new crane position is invalid
    if state[new_x][new_y].name != "UNUSED" or new_x < 0 or new_x > 38 or new_y < 0 or new_y > 9:
      return None

    crane.position = (new_x, new_y)

  def pick_up(self, crane, coordinate):
    crane.empty = False
    crane.container_coordinate = coordinate

  def drop_off(self, crane):
    crane.empty = True
    crane.container_coordinate = ()

  def column_container_search(self, state):
    for i in range(27,39):
      for container in state[i]:
        if container.name in self.offloadShip:
          return i
        
  def ship_to_ship(self, state, coordinates):
    lhs = coordinates[0] - 1
    rhs = coordinates[0] + 1

    while lhs >= 0 or rhs <= 11:

      for i in range(9):
        if lhs >= 0:
          if state[lhs][i].name == "UNUSED":
            state[lhs][i].name = state[coordinates[0]][coordinates[1]].name
            state[coordinates[0]][coordinates[1]].name = "UNUSED"
            print(state[lhs][i].coordinates)
            return(state[lhs][i].name, state[coordinates[0]][coordinates[1]].name)
        if rhs <= 11:
          if state[rhs][i].name == "UNUSED":
            state[rhs][i].name = state[coordinates[0]][coordinates[1]].name
            state[coordinates[0]][coordinates[1]].name = "UNUSED"
            print(state[rhs][i].coordinates)
            return(state[rhs][i].name, state[coordinates[0]][coordinates[1]].name)

      lhs -= 1
      rhs += 1



def uniform_cost(problem, crane):
  frontier = {}
  visited = {}
  max_frontier_size = 0

  current_node = problem.manifest
  frontier.append(current_node)

  iter = 0
  while True:
    if not frontier:
      print(f"To solve this problem the search algorithm expanded a total of {len(visited)} nodes.")
      print(f"The maximum number of nodes in the queue at any one time: {max_frontier_size}.")
      print()
      return None #problem is impossible to solve

    if (len(frontier) > max_frontier_size):
      max_frontier_size = len(frontier)

    frontier.sort(key = lambda x: x.cost, reverse=True)
    current_node = frontier.pop()

    if problem.goal_test(current_node):
      print()
      print(f"To solve this problem the search algorithm expanded a total of {len(visited)} nodes.")
      print(f"The maximum number of nodes in the queue at any one time: {max_frontier_size}.")

      return current_node
    
    visited.append(current_node)

    for i in range(27, 39):
      new = current_node.apply_operator(problem, crane, problem.operator[1])
      in_lists = False

      if new:
        new.parent = current_node
        new.g = current_node.g + 1
        new.cost = new.g

        in_lists = any(node.state == new.state for node in frontier)
        if not in_lists:
          in_lists = any(node.state == new.state for node in visited)

        if not in_lists:
          frontier.append(new)
        else:
          for i,node in enumerate(frontier):
            if (node.state == new.state) and (new.cost < node.cost):
              frontier[i] = new

      iter += 1

  # maxLength = 0
  # root = Node(problem.manifest, None, 0, 0)
  # tree = Tree(root)
  # frontier = {root}
  # explored = set()

  # while len(frontier) != 0:
  #   current_node = min(frontier, key=lambda node: node.f())
  #   maxLength = max(len(frontier), maxLength)
  #   frontier.remove(current_node)

  #   if problem.goal_test(current_node.state):
  #     path = []
  #     while current_node:
  #       path.append(current_node.state)
  #       current_node = current_node.parent
  #     path.reverse()
  #     print(current_node.state)
  
  #   explored.add(current_node)

  #   for operator in problem.operators:
  #     new_state = problem.apply_operator(current_node.state, crane, operator)

  #     if new_state is None:
  #       continue

  #     new_node = Node(new_state, current_node, 0, 0)

  #     new_node.g = current_node.g + 1

  #     if new_node in explored or new_node in frontier:
  #       continue

  #     frontier.add(new_node)


def driver():
  fileName = "Port_Project/ShipCase1.txt"
  data = pd.read_csv(fileName, header=None)

  data[0] = data[0].str.strip('[')
  data[1] = data[1].str.strip(']')
  data[3] = data[3].str.strip()

  data[0] = pd.to_numeric(data[0])
  data[1] = pd.to_numeric(data[1])

  ship = []
  for r in range(12):
    row = []
    for c in range(9):
      row.append(Container("BLANK",(),False,False))
    ship.append(row)
    row = None

  # SHIP SETUP
  k = 0
  for i in range(0,8):
    for j in range(0,12):
      containerName = data.at[k,3]
      ship[j][i] = Container(containerName, (j,i), False, False)
      # Creates a Container at (i, j) that still needs to be told
      # if needed to be unloaded or loaded (if at all needed)
      k = k + 1
  
  for i in range(0,12):
    ship[i][8] = Container("NAN", (i,8), False, False)

  # ship[8][8] = Container("UNUSED", (8,8), False, False)
  # print(ship[8][8])

  crane = Crane((27,8))
  problem = Problem(ship, ("Cat", "Dog"), ())

  print(problem.ship_to_ship(ship, (1,0)))

driver()