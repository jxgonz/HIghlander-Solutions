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
    
  def goal_test(self, buffer):
    if len(self.loadShip) == 0 and len(self.offloadShip) == 0:
      for i in range(24):
        for container in buffer[i]:
          if container.name != "UNUSED":
            return False
      return True
    else:
      return False
    
  def apply_operator(self, operator, state, buffer, crane):
    if operator == 0:
      result = self.ship_to_ship(state, buffer, crane)
    elif operator == 1:
      result = self.ship_to_truck(state, buffer, crane)
    elif operator == 2:
      result = self.ship_to_buffer(state, buffer, crane)
    elif operator == 3:
      result = self.truck_to_ship(state, buffer, crane)
    elif operator == 4:
      result = self.buffer_to_buffer(state, buffer, crane)
    elif operator == 5:
      result = self.buffer_to_ship(state, buffer, crane)
    elif operator == 6:
      result = self.crane_to_ship(state, buffer, crane)
  
    return result
    
  def container_search(self, state):
    for i in range(12):
      for container in state[i]:
        if container.name in self.offloadShip:
          return container.coordinates
    return None
  
  def heuristic(self, state):
    start = state[0]
    end = state[1]
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

        
  def ship_to_ship(self, state, buffer, crane):
    if crane.empty == False and crane.inBuffer == False and state[crane.coordinates[0]][crane.coordinates[1]].name not in self.offloadShip:
      start = crane.coordinates
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
              return start, crane.coordinates
          if rhs <= 11:
            if state[rhs][i].name == "UNUSED":
              state[rhs][i].name = state[crane.coordinates[0]][crane.coordinates[1]].name
              state[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
              crane.coordinates = state[rhs][i].coordinates
              crane.empty = True
              return start, crane.coordinates
        lhs -= 1
        rhs += 1
    else:
      return None

  def ship_to_truck(self, state, buffer, crane):
    if crane.inBuffer == False and crane.coordinates != (0,8):
      start = crane.coordinates
      if crane.empty:
        if len(self.loadShip) != 0:
          crane.coordinates = (0,8)
          crane.empty = False
          state[0][8].name = self.loadShip[0]
          return start, crane.coordinates
        else:
          return None
      else:
        if state[crane.coordinates[0]][crane.coordinates[1]].name in self.offloadShip:
          self.offloadShip.remove(state[crane.coordinates[0]][crane.coordinates[1]].name)
          state[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
          crane.coordinates = (0,8)
          crane.empty = True
          return start, crane.coordinates
        else:
          return None
    else:
      return None

  def ship_to_buffer(self, state, buffer, crane):
    counter = 0
    full = False
    for i in range(12):
      if state[i][8].name == "UNUSED":
        counter += 1
    if counter <= 1:
      full = True
    if full:
      if crane.coordinates == (0,8) and crane.inBuffer == False:
        start = crane.coordinates
        if crane.empty:
          for i in range(23,0,-1):
            for container in list(reversed(buffer[i])):
              if container.name != "UNUSED":
                crane.coordinates = container.coordinates
                crane.empty = False
                crane.inBuffer = True
                return start, crane.coordinates

          # print(crane.coordinates, crane.empty, crane.inBuffer)
          # print(buffer[crane.coordinates[0]][crane.coordinates[1]])
        else:
          container_name = state[0][8]
          for i in range(23,0,-1):
            for container in buffer[i]:
              if container.name == "UNUSED":
                container.name = container_name.name
                container_name.name = "UNUSED"
                crane.coordinates = container.coordinates
                crane.empty = True
                crane.inBuffer = True
                return start, crane.coordinates
      else:
        return None
    else:
      return None

  def truck_to_ship(self, state, buffer, crane):
    if crane.coordinates == (0,8) and crane.inBuffer == False:
      start = crane.coordinates
      if crane.empty:
        coordinates = self.container_search(state)
        if coordinates != None:
          for container in list(reversed(state[coordinates[0]])):
            if container.name != "UNUSED":
              crane.coordinates = container.coordinates
              crane.empty = False
              crane.inBuffer = False
              return start, crane.coordinates
        else:
          return None
      else:
        for i in range(12):
          for container in state[i]:
            if container.name == "UNUSED" and state[0][8].name in self.loadShip:
              container.name = state[0][8].name
              self.loadShip.remove(state[0][8].name)
              state[0][8].name = "UNUSED"
              crane.coordinates = container.coordinates
              crane.empty = True
              return start, crane.coordinates
        return None
    else:
      return None

  def buffer_to_buffer(self, state, buffer, crane):
    if crane.inBuffer == True and crane.empty == False:
      start = crane.coordinates
      lhs = crane.coordinates[0] - 1
      rhs = crane.coordinates[0] + 1

      while lhs >= 0 or rhs <= 23:
        for i in range(4):
          if lhs >= 0:
            if buffer[lhs][i].name == "UNUSED":
              buffer[lhs][i].name = buffer[crane.coordinates[0]][crane.coordinates[1]].name
              buffer[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
              crane.coordinates = buffer[lhs][i].coordinates
              crane.empty = True
              return start, crane.coordinates

          if rhs <= 23:
            if buffer[rhs][i].name == "UNUSED":
              buffer[rhs][i].name = buffer[crane.coordinates[0]][crane.coordinates[1]].name
              buffer[crane.coordinates[0]][crane.coordinates[1]].name = "UNUSED"
              crane.coordinates = buffer[lhs][i].coordinates
              crane.empty = True
              return start, crane.coordinates

        lhs -= 1
        rhs += 1
    else:
      return None

  def buffer_to_ship(self, state, buffer,crane):
    if crane.inBuffer == True:
      start = crane.coordinates
      container_name = buffer[crane.coordinates[0]][crane.coordinates[1]]
      if crane.empty:
        coordinates = self.container_search(state)
        for container in list(reversed(state[coordinates[0]])):
          if container.name != "UNUSED":
            crane.coordinates = container.coordinates
            crane.empty = False
            crane.inBuffer = False
            return start, crane.coordinates
      else:
        for i in range(12):
          for container in state[i]:
            if container.name == "UNUSED":
              container.name = container_name.name
              container_name.name = "UNUSED"
              crane.coordinates = container.coordinates
              crane.inBuffer = False
              crane.empty = True
              return start, crane.coordinates
    else:
      return None
    
  def crane_to_ship(self, state, buffer, crane):
    if crane.empty and crane.inBuffer == False and crane.coordinates != (0,8):
      start = crane.coordinates
      if self.container_search(state) != None:
        column = self.container_search(state)[0]
        for container in list(reversed(state[column])):
          if container.name != "UNUSED":
            crane.coordinates = container.coordinates
            crane.empty = False
            crane.inBuffer = False
            return start, crane.coordinates
      else:
        return None
    else:
      return None



def uniform_cost(problem, crane):
  maxLength = 0
  root = Node(((0,8),(0,8)), None, 0, 0)
  tree = Tree(root)
  frontier = {root}
  explored = set()

  while len(frontier) != 0:
    current_node = min(frontier, key=lambda node: node.f())
    maxLength = max(len(frontier), maxLength)
    frontier.remove(current_node)

    if problem.goal_test(problem.buffer):
      # print(np.matrix(current_node.state))
      path=[]
      while current_node:
        path.append(current_node.state)
        current_node = current_node.parent
      path.reverse()
      for state in path:
        print(state)
        print()
      return path, maxLength
  
    explored.add(current_node)

    for i in range(7):
      new_state = problem.apply_operator(i, problem.manifest, problem.buffer, crane)

      if new_state is None:
        continue

      new_node = Node(new_state, current_node, 0, 0)

      new_node.g = current_node.g
      new_node.h = problem.heuristic(new_state)

      if new_node in explored or new_node in frontier:
        continue
      
      # print(np.matrix(new_node.state))
      # print()

      frontier.add(new_node)
  return None, maxLength

def a_star(problem, crane):
  maxLength = 0
  root = Node(((0,8), (0,8)), None, 1, 1)
  tree = Tree(root)
  frontier = {root}
  explored = set()
  
  while frontier:
    current_node = min(frontier, key=lambda node: node.f())
    frontier.remove(current_node)
    maxLength = max(len(frontier), maxLength)
    
    explored.add(current_node)
    
    for i in range(7):
      new_state = problem.apply_operator(i, problem.manifest, problem.buffer, crane)
      
      if new_state is None:
        continue
      
      new_node = Node(new_state, current_node, 1, 1)
      
      new_node.g = current_node.g + 1
      new_node.h = problem.heuristic(new_state)
      
      if new_node in explored:
        continue
      
      if problem.goal_test(problem.buffer):
      # print(np.matrix(current_node.state))
        path=[]
        while current_node:
          path.append(current_node.state)
          current_node = current_node.parent
        path.reverse()
        for state in path:
          print(state)
          print()
        return path, maxLength
    
      if new_node in frontier:
        frontier_node = next(node for node in frontier if node.state == new_node.state)
        if new_node.f() < frontier_node.f():
          frontier.remove(frontier_node)
          frontier.add(new_node)
      else:
        frontier.add(new_node)
        
  return None, maxLength          
  


def driver():
  fileName = "ShipCase1.txt"
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
    
  # print(np.matrix(ship))
  # print()
  
  crane = Crane()
  problem = Problem(ship, buffer, ["Cat"], ["BRO"])
  
  # uniform_cost(problem, crane)
  a_star(problem, crane)
  # print()
  # print(np.matrix(ship))

driver()