import pandas as pd

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



class Problem:
  def __init__(self, initial_manifest, offloadShip, loadShip, cranePos):
    self.initial_manifest = initial_manifest
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    self.cranePos = cranePos
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
      
  def apply_operator(self, state, operator):
    new_position = (self.cranePos[0] + operator[0], self.cranePos[1] + operator[1])

    if new_position[0] < 1 or new_position[0] > 12 or new_position[1] < 1 or new_position[1] > 9 or state[new_position] == 'NAN':
      return None

    self.cranePos = new_position
    print(self.cranePos)



def uniform_cost(problem):
  maxLength = 0
  root = Node(problem.initial_manifest, None, 0, 0)
  tree = Tree(root)
  frontier = {root}
  explored = set()

  while len(frontier) != 0:
    current_node = min(frontier, key=lambda node: node.f())
    maxLength = max(len(frontier), maxLength)
    frontier.remove(current_node)

    if problem.goal_test(current_node.state):
      print(current_node.state)
  
    explored.add(current_node)

    for operator in problem.operators:
      new_state = problem.apply_operator(current_node.state, operator)

      if new_state is None:
        continue

      new_node = Node(new_state, current_node, 0, 0)

      new_node.g = current_node.g
      # new_node.h = problem

      if new_node in explored or new_node in frontier:
        continue

      frontier.add(new_node)


def driver():
  fileName = "Port_Project/ShipCase1.txt"
  data = pd.read_csv(fileName, header=None)

  data[0] = data[0].str.strip('[')
  data[1] = data[1].str.strip(']')
  data[3] = data[3].str.strip()

  data[0] = pd.to_numeric(data[0])
  data[1] = pd.to_numeric(data[1])

  dict = {}
  for i in data.index:
    dict[(data.at[i, 0], data.at[i, 1])] = data.at[i, 3]

  # print(dict)

  crane = (5,5)
  problem = Problem(dict, 0, 0, crane)

  # problem.apply_operator(dict, problem.operators[3])

  for operator in problem.operators:
    problem.apply_operator(dict, operator)

  # solution = uniform_cost(problem)

driver()