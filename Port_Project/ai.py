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
  def __init__(self):
    self.coordinates = (0,8)
    self.empty = False
    self.inBuffer = False
    # self.container_coordinate = (0,8)

class Problem:
  def __init__(self, manifest, buffer, offloadShip, loadShip):
    self.manifest = manifest
    self.buffer = buffer
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    self.cost = 0
    self.g = 0
    self.h = 0
    
  def goal_test(self, state):
    if self.offloadShip in state:
      return False
    else:
      if self.loadShip in state:
        return True
      else:
        return False

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
        
  def ship_to_ship(self, state, crane):
    lhs = crane.coordinates[0] - 1
    rhs = crane.coordinates[0] + 1

    while lhs >= 0 or rhs <= 11:
      for i in range(9):
        if lhs >= 0:
          if state[lhs][i].name == "UNUSED":
            state[lhs][i].name = state[crane.coordinates[0]][crane.coordinates[1]].name
            state[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
            crane.coordinates = state[lhs][i].coordinates
            crane.empty = True
            return(crane.coordinates, crane.empty)
            # print(state[lhs][i].coordinates)
            # return(state[lhs][i].name, state[coordinates[0]][coordinates[1]].name)
        if rhs <= 11:
          if state[rhs][i].name == "UNUSED":
            state[rhs][i].name = state[crane.coordinates[0]][crane.coordinates[1]].name
            state[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
            crane.coordinates = state[lhs][i].coordinates
            crane.empty = True
            return(crane.coordinates, crane.empty)
            # print(state[rhs][i].coordinates)
            # return(state[rhs][i].name, state[coordinates[0]][coordinates[1]].name)
      lhs -= 1
      rhs += 1

  def ship_to_truck(self, state, crane):
    if crane.empty:
      if len(self.loadShip) != 0:
        crane.coordinates = (0,8)
        crane.empty = False
        state[0][8].name = self.loadShip[0]
        self.loadShip.remove(self.loadShip[0])
        print(self.loadShip)
        print(state[crane.coordinates[0]][crane.coordinates[1]])
        print(crane.coordinates)
      else:
        print('No containers to add')
      # print("EMPTY!", crane.coordinates)
    else:
      if state[crane.coordinates[0]][crane.coordinates[1]].name in self.offloadShip:
        self.offloadShip.remove(state[crane.coordinates[0]][crane.coordinates[1]].name)
        state[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
        crane.coordinates = (0,8)
        crane.empty = True
        print(self.offloadShip)
        print(state[crane.coordinates[0]][crane.coordinates[1]])
        print(crane.coordinates)
      else:
        print('Container "', state[crane.coordinates[0]][crane.coordinates[1]].name, '" does not need to be removed')

  def ship_to_buffer(self, state, buffer, crane):
    if crane.coordinates == (0,8) and crane.inBuffer == False:
      if crane.empty:
        for i in range(23,0,-1):
          for container in list(reversed(buffer[i])):
            if container.name != "UNUSED":
              crane.coordinates = container.coordinates
              crane.empty = False
              crane.inBuffer = True

        print(crane.coordinates, crane.empty, crane.inBuffer)
        print(buffer[crane.coordinates[0]][crane.coordinates[1]])
      else:
        for i in range(23,0,-1):
          for container in buffer[i]:
            if container.name != "UNUSED":
              container.name = state[0][8].name
              state[0][8].name = "UNUSED"
              crane.coordinates = container.coordinates
              crane.empty = True
              crane.inBuffer = True

        print(crane.coordinates, crane.empty, crane.inBuffer)
        print(buffer[crane.coordinates[0]][crane.coordinates[1]])
    else:
      print("Move crane to transfer cell")

  def truck_to_ship(self, state, crane, coordinates=()):
    if crane.empty:
      crane.coordinates = coordinates
      crane.empty = False
    else:
      for i in range(12):
        for container in state[i]:
          if container.name == "UNUSED" and state[0][8].name in self.loadShip:
            container.name = state[0][8].name
            self.loadShip.remove(state[0][8].name)
            state[0][8].name = "UNUSED"
            print(self.loadShip)
            print(state[0][8])
            print(container.coordinates)
          else:
            print("No containers to add")

  def buffer_to_buffer(self, state, crane):
    lhs = crane.coordinates[0] - 1
    rhs = crane.coordinates[0] + 1

    while lhs >= 0 or rhs <= 23:
      for i in range(4):
        if lhs >= 0:
          if state[lhs][i].name == "UNUSED":
            state[lhs][i].name = state[crane.coordinates[0]][crane.coordinates[1]].name
            state[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
            crane.coordinates = state[lhs][i].coordinates
            crane.empty = True
            print(crane.coordinates, crane.empty)
            # print(state[lhs][i].coordinates)
            # return(state[lhs][i].name, state[crane.coordinates[0]][crane.coordinates[1]].name)
        if rhs <= 23:
          if state[rhs][i].name == "UNUSED":
            state[rhs][i].name = state[crane.coordinates[0]][crane.coordinates[1]].name
            state[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
            crane.coordinates = state[lhs][i].coordinates
            crane.empty = True
            print(crane.coordinates, crane.empty)
            # print(state[rhs][i].coordinates)
            # return(state[rhs][i].name, state[crane.coordinates[0]][crane.coordinates[1]].name)
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
      row.append(Container("BLANK",()))
    ship.append(row)
    row = None

  # SHIP SETUP
  k = 0
  for i in range(0,8):
    for j in range(0,12):
      containerName = data.at[k,3]
      ship[j][i] = Container(containerName, (j,i))
      # Creates a Container at (i, j) that still needs to be told
      # if needed to be unloaded or loaded (if at all needed)
      k = k + 1
  
  for i in range(0,12):
    ship[i][8] = Container("UNUSED", (i,8))

  buffer = []
  for r in range(24):
    ro = []
    for c in range(4):
      ro.append(Container("UNUSED", (r,c)))
    buffer.append(ro)
    ro = None

  # ship[8][8] = Container("UNUSED", (8,8))
  # print(ship[8][8])

  buffer[10][0].name = "WALMART"
  ship[0][8].name = "GROW"
  crane = Crane()
  problem = Problem(ship, buffer, ["Cat"], ["Frog", "Blog"])

  # shiplist = buffer[10]
  # print(list(reversed(shiplist)))

  problem.ship_to_buffer(ship, buffer, crane)



  # print(problem.buffer_to_buffer(buffer, crane))

  # problem.ship_to_ship(ship, crane, (1,0))
  # problem.ship_to_truck(ship, crane)
  # print(problem.ship_to_ship(ship, crane, (2,0)))
  # problem.ship_to_truck(ship, crane)

driver()