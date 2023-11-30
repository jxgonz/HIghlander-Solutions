import pandas as pd

class Node:
  def __init__(self, parent=None, g=0, h=0):
    self.parent = parent
    self.g = g
    self.h = h

  def f(self):
    return self.g + self.h

class Problem:
  def __init__(self, initial_manifest, offloadShip, loadShip):
    self.initial_manifest = initial_manifest
    self.offloadShip = offloadShip
    self.loadShip = loadShip
    self.operators = [
      (-1, 0), #move container down
      (1, 0),  #move container up
      (0, -1), #move container left
      (0, 1),  #move container right
      ]
    
  def goal_test(self):
    if self.offloadShip in dict.values():
      return False
    else:
      if self.loadShip in dict.values():
        return True
      else:
        return False

def driver():
  fileName = "ShipCase1.txt"
  data = pd.read_csv(fileName, header=None)

  data[0] = data[0].str.strip('[')
  data[1] = data[1].str.strip(']')
  data[3] = data[3].str.strip()

  data[0] = pd.to_numeric(data[0])
  data[1] = pd.to_numeric(data[1])

  dict = {}
  for i in data.index:
    dict[(data.at[i, 0], data.at[i, 1])] = data.at[i, 3]
    
  print(dict)


driver()