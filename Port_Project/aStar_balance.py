#uniform cost search
from grid_balance import *

def a_star(start):
    frontier = []
    visited = []
    max_frontier_size = 0
    goal = 0.9
    
    current_node = start
    frontier.append(current_node) #push start node to frontier

    iter = 0
    while True:
        if not frontier:
            return None #problem is impossible to solve
        
        if(len(frontier) > max_frontier_size):
            max_frontier_size = len(frontier)

        frontier.sort(key = lambda x: (x.cost, x.manhattan_distance), reverse=True) #order frontier by cost
        current_node = frontier.pop()
        
        if current_node.check_goal() >= goal and current_node.check_bufferEmpty():
            return current_node
            
        visited.append(current_node)
        
        if current_node.check_bufferEmpty() == True:
            loopRange = 12
        else:
            loopRange = 36
        for i in range(0,loopRange): #get all child nodes ##Changing to 0,36 to include buffer as well as to include buffer as well original us 0,12
            new = current_node.operators(i)
            if new != None:
                in_lists = False
                #Added conditional with heuristic to just not include unbalancable states
                if new and new.calc_heuristic(hn=0) != None: #check that this state is not already in lists
                    new.parent = current_node
                    new.g = current_node.g + 1 # update g(n)
                    new.manhattan_distance = new.manhattan(current_node.craneRow, current_node.craneCol) # update manhattan distance
                    if new.calc_heuristic(hn=0) != None:
                        new.h = new.calc_heuristic(hn=0) # update h(n)
                    else:
                        "Error impossible to balance"
                        return 0
                    new.cost = new.g + new.h # update total cost
                    
                    in_lists = any(node.inventory_array == new.inventory_array and node.buffer_inventory == new.buffer_inventory and node.crane == new.crane for node in frontier) #check if already in frontier or visited
                    if not in_lists:
                        in_lists = any(node.inventory_array == new.inventory_array and node.buffer_inventory == new.buffer_inventory and node.crane == new.crane for node in visited)
                
                    if not in_lists:
                        frontier.append(new)
                    else: #replace if in frontier and higher cost
                        for i,node in enumerate(frontier):
                            if (node.inventory_array == new.inventory_array and node.buffer_inventory == new.buffer_inventory and node.crane == new.crane) and (new.cost <= node.cost):
                                print("Node information:")
                                print(node.h)
                                node.printGridWeights()
                                print()
                                print("New information:")
                                print(new.h)
                                new.printGridWeights()

                                if new.cost < node.cost:
                                    frontier[i] = new
                                elif new.cost == node.cost:
                                    if new.manhattan_distance < node.manhattan_distance:
                                        frontier[i] = new
                
        iter += 1