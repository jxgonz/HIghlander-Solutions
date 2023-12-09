import pandas as pd
import numpy as np
from container import Container
import copy

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
    self.empty = True
    self.inBuffer = False

class Problem:
  def __init__(self, ship, buffer, crane, offloadShip, loadShip):
    self.ship = ship
    self.buffer = buffer
    self.crane = crane
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    self.parent = None
    self.g = 0
    self.h = 0
    self.cost = 0
  
  def f(self):
    return self.g + self.h
    
  def goal_test(self, state):
    if len(state.loadShip) == 0 and len(state.offloadShip) == 0 and state.ship[state.crane.coordinates[0]][state.crane.coordinates[1]].name == "UNUSED":
      for i in range(24):
        for container in state.buffer[i]:
          if container.name != "UNUSED":
            return False
      return True
    else:
      return False
    
  def apply_operator(self, operator, state):
    copy_node = copy.deepcopy(state)
    if operator == 0:
      result = state.ship_to_ship(copy_node)
    elif operator == 1:
      result = state.ship_to_truck(copy_node)
    elif operator == 2:
      result = state.ship_to_buffer(copy_node)
    elif operator == 3:
      result = state.truck_to_ship(copy_node)
    elif operator == 4:
      result = state.buffer_to_buffer(copy_node)
    elif operator == 5:
      result = state.buffer_to_ship(copy_node)
    elif operator == 6:
      result = state.crane_to_ship(copy_node)
  
    return result
    
  def container_search(self, state, offload):
    for i in range(12):
      for container in state[i]:
        if container.name in offload:
          return container.coordinates
    return None
  
  def heuristic(self, node):
    start = node.parent.state.crane.coordinates
    end = node.state.crane.coordinates
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

        
  def ship_to_ship(self, state):
    if state.crane.empty == False and state.crane.inBuffer == False and state.ship[state.crane.coordinates[0]][state.crane.coordinates[1]].name not in state.offloadShip:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      lhs = newCrane.coordinates[0] - 1
      rhs = newCrane.coordinates[0] + 1
      while lhs >= 0 or rhs <= 11:
        for i in range(9):
          if lhs >= 0:
            if newShip[lhs][i].name == "UNUSED":
              newShip[lhs][i].name = newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newShip[lhs][i].coordinates
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
          if rhs <= 11:
            if newShip[rhs][i].name == "UNUSED":
              newShip[rhs][i].name = newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newShip[rhs][i].coordinates
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        lhs -= 1
        rhs += 1
    else:
      return None

  def ship_to_truck(self, state):
    if state.crane.inBuffer == False:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      if newCrane.empty:
        if len(newLoad) != 0:
          newCrane.coordinates = (0,8)
          newCrane.empty = False
          newShip[0][8].name = newLoad[0]
          return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        else:
          return None
      else:
        if newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name in newOffload:
          newOffload.remove(newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name)
          newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
          newCrane.coordinates = (0,8)
          newCrane.empty = True
          return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        else:
          return None
    else:
      return None

  def ship_to_buffer(self, state):
    counter = 0
    full = False
    for i in range(12):
      if state.ship[i][8].name == "UNUSED":
        counter += 1
    if counter <= 1:
      full = True
    if full:
      if state.crane.coordinates == (0,8) and state.crane.inBuffer == False:
        newCrane = state.crane
        newOffload = state.offloadShip
        newLoad = state.loadShip
        newShip = state.ship
        newBuffer = state.buffer
        if newCrane.empty:
          for i in range(23,0,-1):
            for container in list(reversed(newBuffer[i])):
              if container.name != "UNUSED":
                newCrane.coordinates = container.coordinates
                newCrane.empty = False
                newCrane.inBuffer = True
                return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)

          # print(newCrane.coordinates, newCrane.empty, newCrane.inBuffer)
          # print(buffer[newCrane.coordinates[0]][newCrane.coordinates[1]])
        else:
          container_name = newShip[0][8]
          for i in range(23,0,-1):
            for container in newBuffer[i]:
              if container.name == "UNUSED":
                container.name = container_name.name
                container_name.name = "UNUSED"
                newCrane.coordinates = container.coordinates
                newCrane.empty = True
                newCrane.inBuffer = True
                return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
      else:
        return None
    else:
      return None

  def truck_to_ship(self, state):
    if state.crane.coordinates == (0,8) and state.crane.inBuffer == False:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      if newCrane.empty:
        coordinates = state.container_search(newShip, newOffload)
        if coordinates != None:
          for container in list(reversed(newShip[coordinates[0]])):
            if container.name != "UNUSED":
              newCrane.coordinates = container.coordinates
              newCrane.empty = False
              newCrane.inBuffer = False
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        else:
          return None
      else:
        for i in range(12):
          for container in newShip[i]:
            if container.name == "UNUSED" and newShip[0][8].name in newLoad:
              container.name = newShip[0][8].name
              newLoad.remove(newShip[0][8].name)
              newShip[0][8].name = "UNUSED"
              newCrane.coordinates = container.coordinates
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        return None
    else:
      return None

  def buffer_to_buffer(self, state):
    if state.crane.inBuffer == True and state.crane.empty == False:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      lhs = newCrane.coordinates[0] - 1
      rhs = newCrane.coordinates[0] + 1

      while lhs >= 0 or rhs <= 23:
        for i in range(4):
          if lhs >= 0:
            if newBuffer[lhs][i].name == "UNUSED":
              newBuffer[lhs][i].name = newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newBuffer[lhs][i].coordinates
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)

          if rhs <= 23:
            if newBuffer[rhs][i].name == "UNUSED":
              newBuffer[rhs][i].name = newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newBuffer[lhs][i].coordinates
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)

        lhs -= 1
        rhs += 1
    else:
      return None

  def buffer_to_ship(self, state):
    if state.crane.inBuffer == True:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      container_name = newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]]
      if newCrane.empty:
        coordinates = state.container_search(newShip, newOffload)
        for container in list(reversed(newShip[coordinates[0]])):
          if container.name != "UNUSED":
            newCrane.coordinates = container.coordinates
            newCrane.empty = False
            newCrane.inBuffer = False
            return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
      else:
        for i in range(12):
          for container in newShip[i]:
            if container.name == "UNUSED":
              container.name = container_name.name
              container_name.name = "UNUSED"
              newCrane.coordinates = container.coordinates
              newCrane.inBuffer = False
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
    else:
      return None
    
  def crane_to_ship(self, state):
    if state.crane.empty and state.crane.inBuffer == False and state.crane.coordinates != (0,8):
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      if state.container_search(newShip, newOffload) != None:
        column = state.container_search(newShip, newOffload)[0]
        for container in list(reversed(newShip[column])):
          if container.name != "UNUSED":
            newCrane.coordinates = container.coordinates
            newCrane.empty = False
            newCrane.inBuffer = False
            return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
      else:
        return None
    else:
      return None



# def uniform_cost(problem):
#   maxLength = 0
#   root = problem
#   tree = Tree(root)
#   frontier = {root}
#   explored = set()

#   while len(frontier) != 0:
#     current_node = min(frontier, key=lambda node: node.f())
#     maxLength = max(len(frontier), maxLength)
#     frontier.remove(current_node)

#     if problem.goal_test(current_node.buffer):
#       # print(np.matrix(current_node.state))
#       path=[]
#       while current_node:
#         path.append(current_node.ship)
#         current_node = current_node.parent
#       path.reverse()
#       # for state in path:
#       #   print(np.matrix(state))
#       #   print()
#       return path, maxLength
  
#     explored.add(current_node)
#     # print(explored)

#     for i in range(7):
#       # print(current_node.coordinates)
#       # print()
#       new_node = problem.apply_operator(i, current_node.ship, current_node.buffer)

#       # print(new_state)

#       if new_node is None:
#         continue

#       print(np.matrix(new_node.ship))
#       print()
#       print()

#       new_node.parent = current_node
#       new_node.g = current_node.g + 1
#       # new_node.h = problem.heuristic(new_state)

#       if new_node in explored or new_node in frontier:
#         continue
      
#       # print(new_node.state)
#       # print()
#       # print(np.matrix(new_node.ship))
#       # print()
#       # print()

#       frontier.add(new_node)
#       # print(frontier)
#   return None, maxLength

def uniform_cost(problem):
  frontier = []
  visited = []

  current_node = problem
  frontier.append(current_node)

  iter = 0
  while True:
    if not frontier:
      print("Not possible")
      return None
    
    frontier.sort(key = lambda x: x.g, reverse=True)
    current_node = frontier.pop()

    if problem.goal_test(current_node):
      # print(np.matrix(current_node.state))
      path=[]
      while current_node:
        path.append(current_node.ship)
        current_node = current_node.parent
      path.reverse()
      for state in path:
        print(np.matrix(state))
        print()
      return path
    
    visited.append(current_node)
    # print()
    # for node in visited:
    #   print(node.state)
    # print()

    for i in range(7):
      # print(current_node.crane.coordinates)
      # print()
      new = problem.apply_operator(i, current_node)
      in_lists = False

      # if new:
      #   print(current_node.crane.coordinates, new.crane.coordinates)
      # else:
      #   print(None)

      if new:
        new.parent = current_node
        new.g = current_node.g + 1
        new.cost = new.g

        in_lists = any(node == new for node in frontier) #check if already in frontier or visited
        if not in_lists:
          in_lists = any(node == new for node in visited)

        if not in_lists:
          frontier.append(new)
        else:
          for i,node in enumerate(frontier):
            if (node == new) and (new.cost < node.cost):
              frontier[i] = new

      iter += 1
        
      # print()
      # for node in frontier:
      #   print(node.newCrane.coordinates)
      # print()

def a_star(problem):
  maxLength = 0
  root = Node(problem, None, 1, 1)
  tree = Tree(root)
  frontier = {root}
  explored = set()
  
  while frontier:
    current_node = min(frontier, key=lambda node: node.f())
    frontier.remove(current_node)
    # maxLength = max(len(frontier), maxLength)

    if problem.goal_test(current_node.state):
        # print(np.matrix(current_node.ship))
        path=[]
        while current_node:
          path.append(current_node.state)
          current_node = current_node.parent
        path.reverse()
        for state in path:
          print(np.matrix(state.ship))
          print(state.h)
          print()
        return path, maxLength
    
    explored.add(current_node)
    # for node in explored:
    #   print(node.state)
    
    # print()
    
    for i in range(7):
      # print(current_node.state.crane.coordinates)
      # print()
      new_state = problem.apply_operator(i, current_node.state)
      
      if new_state is None:
        continue
      
      # print(np.matrix(new_node.ship))
      # print()
      new_node = Node(new_state, current_node, 1, 1)
      new_node.g = current_node.g + 1
      new_node.h = problem.heuristic(new_node)
      
      if new_node in explored:
        continue
      
      # print(new_node.state)
      # print()
      # print(new_node.h)
      # print()
      # print(np.matrix(new_node.ship))
      # print()
      # print()
    
      if new_node in frontier:
        frontier_node = next(node for node in frontier if node.state == new_node.state)
        if new_node.f() < frontier_node.f():
          frontier.remove(frontier_node)
          frontier.add(new_node)
      else:
        frontier.add(new_node)
      
      # for node in frontier:
      #   print(node.state)
    
      # print()
        
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
  problem = Problem(ship, buffer, crane, ["Cat"], ["Frogs"])
  
  # print(uniform_cost(problem))
  # uniform_cost(problem)
  a_star(problem)
  # print()
  # print(np.matrix(ship))

driver()