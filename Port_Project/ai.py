import pandas as pd
import numpy as np
from container import Container
import copy

#node class
class Node:
  def __init__(self, state, parent=None, g=0, h=0):
    self.state = state
    self.parent = parent
    self.g = g
    self.h = h

  def f(self):
    return self.g + self.h

#tree class
class Tree: 
  def __init__(self, root):
    self.root = root

#crane class
class Crane:
  def __init__(self):
    self.coordinates = (0,8)   #crane's current coordinataes
    self.empty = True          #checks whether crane is holding container
    self.inBuffer = False      #checks whether crane is in buffer

#problem space
class Problem:
  def __init__(self, ship, buffer, crane, offloadShip, loadShip):
    self.ship = ship
    self.buffer = buffer
    self.crane = crane
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    
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
  
  #searches for closest container that needs to be offloaded
  def container_search(self, state, offload):
    #checks every column in the grid
    for i in range(12):
      #checks every container in the column
      for container in state[i]:
        if container.name in offload:
          return container.coordinates
    return None
  
  def heuristic(self, node, operator):
    #mahattan distance: |x1 - x2| + |y1 - y2|
    start = node.parent.state.crane.coordinates
    end = node.state.crane.coordinates
  
    transfer = 0
    # if node.parent.parent == None and end == (0, 8) and node.state.crane.empty == True:
    #   transfer = 0
    #if crane moves from and to truck, then add two
    if operator == 1 or operator == 3:
      transfer = 2
      #if crane moves from and to buffer, then add four
    elif operator == 2 or operator == 5:
      transfer = 4
    
    return(abs(start[0] - end[0]) + abs(start[1] - end[1]) + transfer)

        
  #if crane moves in between ship, then move container to closest unused cell
  def ship_to_ship(self, state):
    if state.crane.empty == False and state.crane.inBuffer == False and state.ship[state.crane.coordinates[0]][state.crane.coordinates[1]].name not in state.offloadShip:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      lhs = newCrane.coordinates[0] - 1
      rhs = newCrane.coordinates[0] + 1
      #checks whether lhs and rhs is in between the bounds of the ship
      while lhs >= 0 or rhs <= 11:
        #checks each cell in column lhs and rhs until the 9th level
        for i in range(9):
          if lhs >= 0:
            if newShip[lhs][i].name == "UNUSED":
              newShip[lhs][i].name = newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newShip[lhs][i].coordinates
              newCrane.empty = True
              newCrane.inBuffer = False
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
          if rhs <= 11:
            if newShip[rhs][i].name == "UNUSED":
              newShip[rhs][i].name = newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newShip[rhs][i].coordinates
              newCrane.empty = True
              newCrane.inBuffer = False
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
          newCrane.inBuffer = False
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
          newCrane.inBuffer = False
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
            coordinates = state.container_search(newShip, newOffload)
            if coordinates != None and i != coordinates[0]:
              if container.name == "UNUSED" and newShip[0][8].name in newLoad :
                container.name = newShip[0][8].name
                newLoad.remove(newShip[0][8].name)
                newShip[0][8].name = "UNUSED"
                newCrane.coordinates = container.coordinates
                newCrane.empty = True
                newCrane.inBuffer = False
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
      if newCrane.empty and len(newOffload) != 0:
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



def uniform_cost(problem):
  maxLength = 0
  root = Node(problem, None, 1, 1)
  tree = Tree(root)
  frontier = {root}
  explored = set()

  while len(frontier) != 0:
    current_node = min(frontier, key=lambda node: node.f())
    maxLength = max(len(frontier), maxLength)
    frontier.remove(current_node)

    if problem.goal_test(current_node.state):
      path=[]
      while current_node:
        path.append(current_node)
        current_node = current_node.parent
      path.reverse()
      for node in path:
        print(np.matrix(node.state.ship))
        print()
      return path, maxLength
  
    explored.add(current_node)

    for i in range(7):
      new_state = problem.apply_operator(i, current_node.state)

      if new_state is None:
        continue

      new_node = Node(new_state, current_node, 0, 0)
      new_node.g = current_node.g + 1

      if new_node in explored or new_node in frontier:
        continue

      frontier.add(new_node)
  return None, maxLength

def a_star(problem):
  maxLength = 0
  root = Node(problem, None, 1, 1)
  tree = Tree(root)
  frontier = {root}
  explored = set()
  
  while frontier:
    current_node = min(frontier, key=lambda node: node.f())
    frontier.remove(current_node)

    if problem.goal_test(current_node.state):
        path=[]
        while current_node:
          path.append(current_node)
          current_node = current_node.parent
        path.reverse()
        for node in path:
          print(np.matrix(node.state.ship))
          print()
        return path, maxLength
    
    explored.add(current_node)
    
    for i in range(7):
      new_state = problem.apply_operator(i, current_node.state)
      
      if new_state is None:
        continue
      
      new_node = Node(new_state, current_node, 1, 1)
      new_node.g = current_node.g + 1
      new_node.h = problem.heuristic(new_node, i)
      
      if new_node in explored:
        continue

      if new_node in frontier:
        frontier_node = next(node for node in frontier if node.state == new_node.state)
        if new_node.f() < frontier_node.f():
          frontier.remove(frontier_node)
          frontier.add(new_node)
      else:
        frontier.add(new_node)
        
  return None, maxLength          
  
# Method that calls AI algorithm on problem
# Needs fileName, list of strings of offLoad,
# list of strings of onLoad containers
def driver(self, fileName, offLoad, onLoad):
  data = pd.read_csv(fileName, header=None)

  data[0] = data[0].str.strip('[')
  data[1] = data[1].str.strip(']')
  data[3] = data[3].str.strip()

  data[0] = pd.to_numeric(data[0])
  data[1] = pd.to_numeric(data[1])

  # SHIP SETUP
  ship = []
  for r in range(12):
    row = []
    for c in range(9):
      row.append(Container("BLANK",()))
    ship.append(row)
    row = None

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

  # BUFFER SETUP
  buffer = []
  for r in range(24):
    ro = []
    for c in range(4):
      ro.append(Container("UNUSED", (r,c)))
    buffer.append(ro)
    ro = None

  crane = Crane()
  problem = Problem(ship, buffer, crane, offLoad, onLoad)
  
  # uniform_cost(problem)
  a_star(problem)

# def driver():
#   fileName = "ShipCase1.txt"
#   data = pd.read_csv(fileName, header=None)

#   data[0] = data[0].str.strip('[')
#   data[1] = data[1].str.strip(']')
#   data[3] = data[3].str.strip()

#   data[0] = pd.to_numeric(data[0])
#   data[1] = pd.to_numeric(data[1])

#   # SHIP SETUP
#   ship = []
#   for r in range(12):
#     row = []
#     for c in range(9):
#       row.append(Container("BLANK",()))
#     ship.append(row)
#     row = None

#   k = 0
#   for i in range(0,8):
#     for j in range(0,12):
#       containerName = data.at[k,3]
#       ship[j][i] = Container(containerName, (j,i))
#       # Creates a Container at (i, j) that still needs to be told
#       # if needed to be unloaded or loaded (if at all needed)
#       k = k + 1
  
#   for i in range(0,12):
#     ship[i][8] = Container("UNUSED", (i,8))

#   # BUFFER SETUP
#   buffer = []
#   for r in range(24):
#     ro = []
#     for c in range(4):
#       ro.append(Container("UNUSED", (r,c)))
#     buffer.append(ro)
#     ro = None

#   crane = Crane()
#   problem = Problem(ship, buffer, crane, ["Cat"], ["Frog"])
  
#   # uniform_cost(problem)
#   a_star(problem)

driver()