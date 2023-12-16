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
    self.cost = self.g + self.h

  def f(self):
    return self.g + self.h

#crane class
class Crane:
  def __init__(self):
    self.coordinates = (8,0)   #crane's current coordinataes
    self.empty = True          #checks whether crane is holding container
    self.inBuffer = False      #checks whether crane is in buffer
    self.onTruck = False

#problem space
class Problem:
  def __init__(self, ship, buffer, crane, offloadShip, loadShip):
    self.ship = ship
    self.buffer = buffer
    self.crane = crane
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    
  def goal_test(self, state):
    if len(state.loadShip) == 0 and len(state.offloadShip) == 0 and state.ship[8][0].name == "UNUSED":
      for i in range(4):
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
    for i in range(8):
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
    #if crane moves from or to truck, then add two
    if operator == 1 or operator == 3:
      transfer = 2
      #if crane moves from or to buffer, then add four
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
      lhs = newCrane.coordinates[1] - 1
      rhs = newCrane.coordinates[1] + 1
      #checks whether lhs and rhs is in between the bounds of the ship
      while lhs >= 0 or rhs <= 11:
        #checks each cell in column lhs and rhs until the 9th level
        for i in range(9):
          if lhs >= 0:
            if newShip[i][lhs].name == "UNUSED":
              newShip[i][lhs].name = newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newShip[i][lhs].coordinates
              newCrane.empty = True
              newCrane.inBuffer = False
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
          if rhs <= 11:
            if newShip[i][rhs].name == "UNUSED":
              newShip[i][rhs].name = newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newShip[i][rhs].coordinates
              newCrane.empty = True
              newCrane.inBuffer = False
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        lhs -= 1
        rhs += 1
    else:
      return None

  def ship_to_truck(self, state):
    if state.crane.inBuffer == False and state.crane.onTruck == False:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      if newCrane.empty:
        if len(newLoad) != 0:
          newCrane.coordinates = (8,0)
          newCrane.empty = False
          newCrane.inBuffer = False
          newCrane.onTruck = True
          newShip[8][0].name = newLoad[0]
          return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        else:
          return None
      else:
        if newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name in newOffload:
          newOffload.remove(newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name)
          newShip[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
          newCrane.coordinates = (8,0)
          newCrane.empty = True
          newCrane.inBuffer = False
          newCrane.onTruck = True
          return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        else:
          return None
    else:
      return None

  def ship_to_buffer(self, state):
    counter = 0
    full = False
    for i in range(12):
      if state.ship[8][i].name == "UNUSED":
        counter += 1
    if counter <= 1:
      full = True
    if full:
      if state.crane.coordinates == (8,0) and state.crane.inBuffer == False:
        newCrane = state.crane
        newOffload = state.offloadShip
        newLoad = state.loadShip
        newShip = state.ship
        newBuffer = state.buffer
        if newCrane.empty:
          for i in range(4):
            for container in list(reversed(newBuffer[i])):
              if container.name != "UNUSED":
                newCrane.coordinates = container.coordinates
                newCrane.empty = False
                newCrane.inBuffer = True
                return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)

          # print(newCrane.coordinates, newCrane.empty, newCrane.inBuffer)
          # print(buffer[newCrane.coordinates[0]][newCrane.coordinates[1]])
        else:
          container_name = newShip[8][0]
          for i in range(4):
            for container in list(reversed(newBuffer[i])):
              if container.name == "UNUSED":
                container.name = container_name.name
                newShip[8][0].name = "UNUSED"
                newCrane.coordinates = container.coordinates
                newCrane.empty = True
                newCrane.inBuffer = True
                return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
      else:
        return None
    else:
      return None

  def truck_to_ship(self, state):
    if state.crane.coordinates == (8,0) and state.crane.inBuffer == False and state.crane.onTruck == True:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      if newCrane.empty:
        coordinates = state.container_search(newShip, newOffload)
        if coordinates != None:
          for i in range(8, -1, -1):
            if newShip[i][coordinates[1]].name != "UNUSED":
              newShip[8][0].name = "UNUSED"
              newCrane.coordinates = newShip[i][coordinates[1]].coordinates
              newCrane.empty = False
              newCrane.inBuffer = False
              newCrane.onTruck = False
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        else:
          return None
      else:
        coordinates = state.container_search(newShip, newOffload)
        if coordinates == None:
          for i in range(12):
            for j in range(9):
              if newShip[j][i].name == "UNUSED" and newShip[8][0].name in newLoad:
                newShip[j][i].name = newShip[8][0].name
                newLoad.remove(newShip[8][0].name)
                newShip[8][0].name = "UNUSED"
                newCrane.coordinates = newShip[j][i].coordinates
                newCrane.empty = True
                newCrane.inBuffer = False
                newCrane.onTruck = False
                return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
        else:
          for i in range(12):
            if i != coordinates[1]:
              for j in range(9):
                if newShip[j][i].name == "UNUSED" and newShip[8][0].name in newLoad:
                  newShip[j][i].name = newShip[8][0].name
                  newLoad.remove(newShip[8][0].name)
                  newShip[8][0].name = "UNUSED"
                  newCrane.coordinates = newShip[j][i].coordinates
                  newCrane.empty = True
                  newCrane.inBuffer = False
                  newCrane.onTruck = False
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
      lhs = newCrane.coordinates[1] - 1
      rhs = newCrane.coordinates[1] + 1

      while lhs >= 0 or rhs <= 23:
        for i in range(4):
          if lhs >= 0:
            if newBuffer[i][lhs].name == "UNUSED":
              newBuffer[i][lhs].name = newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newBuffer[i][lhs].coordinates
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)

          if rhs <= 23:
            if newBuffer[i][rhs].name == "UNUSED":
              newBuffer[i][rhs].name = newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name
              newBuffer[newCrane.coordinates[0]][newCrane.coordinates[1]].name = "UNUSED"
              newCrane.coordinates = newBuffer[i][rhs].coordinates
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
        for i in range(8, -1, -1):
            if newShip[i][coordinates[1]].name != "UNUSED":
              newCrane.coordinates = newShip[i][coordinates[1]].coordinates
              newCrane.empty = False
              newCrane.inBuffer = False
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
      else:
        for i in range(12):
          for j in range(9):
            if newShip[j][i].name == "UNUSED":
              newShip[j][i].name = container_name.name
              container_name.name = "UNUSED"
              newCrane.coordinates = newShip[j][i].coordinates
              newCrane.inBuffer = False
              newCrane.empty = True
              return Problem(newShip, newBuffer, newCrane, newOffload, newLoad)
    else:
      return None
    
  def crane_to_ship(self, state):
    if state.crane.empty and state.crane.inBuffer == False:
      newCrane = state.crane
      newOffload = state.offloadShip
      newLoad = state.loadShip
      newShip = state.ship
      newBuffer = state.buffer
      if state.container_search(newShip, newOffload) != None:
        column = state.container_search(newShip, newOffload)[1]
        for i in range(8,-1,-1):
          if newShip[i][column].name != "UNUSED":
            newCrane.coordinates = newShip[i][column].coordinates
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
      # for node in path:
      #   print(np.matrix(node.state.ship))
      #   print()
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
  root = Node(problem, None, 0, 0)
  frontier = [root]
  explored = set()
  
  while frontier:
    current_node = min(frontier, key=lambda node: node.f())
    frontier.remove(current_node)

    if problem.goal_test(current_node.state):
        path=[]
        test=[]
        while current_node:
          test.append(current_node.state.ship)
          step=[]
          if current_node.parent == None:
            step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
            step.append('ship')
            step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
            step.append('ship')
            step.append(current_node.h)
            path.append(step)
          elif current_node.state.crane.onTruck and current_node.parent.state.crane.empty == False:
            step.append([current_node.parent.state.crane.coordinates[0] + 1, current_node.parent.state.crane.coordinates[1] + 1])
            step.append('ship')
            step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
            step.append("truck")
            step.append(current_node.h)
            path.append(step)
          elif current_node.parent.state.crane.onTruck and current_node.parent.state.crane.empty == False:
            step.append([current_node.parent.state.crane.coordinates[0] + 1, current_node.parent.state.crane.coordinates[1] + 1])
            step.append("truck")
            step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
            step.append('ship')
            step.append(current_node.h)
            path.append(step)
          elif current_node.state.crane.inBuffer and current_node.parent.state.crane.inBuffer and current_node.parent.state.crane.empty == False:
            step.append([current_node.parent.state.crane.coordinates[0] + 1, current_node.parent.state.crane.coordinates[1] + 1])
            step.append('buffer')
            step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
            step.append('buffer')
            step.append(current_node.h)
            path.append(step)
          elif current_node.state.crane.inBuffer and current_node.parent.state.crane.empty == False:
            step.append([current_node.parent.state.crane.coordinates[0] + 1, current_node.parent.state.crane.coordinates[1] + 1])
            step.append('ship')
            step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
            step.append('buffer')
            step.append(current_node.h)
            path.append(step)
          elif current_node.parent.state.crane.inBuffer and current_node.parent.state.crane.empty == False:
            step.append([current_node.parent.state.crane.coordinates[0] + 1, current_node.parent.state.crane.coordinates[1] + 1])
            step.append('buffer')
            step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
            step.append('ship')
            step.append(current_node.h)
            path.append(step)
          else:
            if current_node.parent.state.crane.empty == False:
              step.append([current_node.parent.state.crane.coordinates[0] + 1, current_node.parent.state.crane.coordinates[1] + 1])
              step.append('ship')
              step.append([current_node.state.crane.coordinates[0] + 1, current_node.state.crane.coordinates[1] + 1])
              step.append('ship')
              step.append(current_node.h)
              path.append(step)
          current_node = current_node.parent
          
        path.reverse()
        test.reverse()
        return path
    
    explored.add(current_node)
    
    for i in range(7):
      new_state = problem.apply_operator(i, current_node.state)
      
      if new_state is None:
        continue
      
      new_node = Node(new_state, current_node)
      new_node.g = current_node.g + 1
      new_node.h = problem.heuristic(new_node, i)
      new_node.cost = new_node.g + new_node.h
      
      if new_node in explored:
        continue

      if any(node.state == new_node.state for node in frontier):
        frontier_node = next(node for node in frontier if node.state == new_node.state)
        if new_node.cost < frontier_node.cost:
          frontier.remove(frontier_node)
          frontier.append(new_node)
      else:
        frontier.append(new_node)
              
  return None, maxLength

# Method that calls AI algorithm on problem
# Needs fileName, list of strings of offLoad,
# list of strings of onLoad containers
def driver(fileName, offLoad, onLoad):
  data = pd.read_csv(fileName, header=None)

  data[0] = data[0].str.strip('[')
  data[1] = data[1].str.strip(']')
  data[3] = data[3].str.strip()

  data[0] = pd.to_numeric(data[0])
  data[1] = pd.to_numeric(data[1])

  # SHIP SETUP
  ship = []
  for r in range(9):
    row = []
    for c in range(12):
      row.append(Container("BLANK",()))
    ship.append(row)
    row = None

  k = 0
  for i in range(0,8):
    for j in range(0,12):
      containerName = data.at[k,3]
      ship[i][j] = Container(containerName, (i,j))
      k = k + 1
  
  for i in range(0,12):
    ship[8][i] = Container("UNUSED", (i,8))

  # BUFFER SETUP
  buffer = []
  for r in range(4):
    ro = []
    for c in range(24):
      ro.append(Container("UNUSED", (r,c)))
    buffer.append(ro)
    ro = None

  crane = Crane()
  problem = Problem(ship, buffer, crane, offLoad, onLoad)
  
  return a_star(problem)