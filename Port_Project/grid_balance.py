from container_balance import *
import copy

# Ship Grid Class
class Grid:

    def __init__(self, inventory_array, buffer_inventory, parent, removeRow, removeCol, craneRow, craneCol, craneContainer):
        # Grid dimensions
        self.row = 9
        self.col = 12
        # Buffer Dimensions
        self.bufferRow = 5
        self.bufferCol = 24
        
        #Array to keep track of intial coordinates and new coordinates when a container is moved
        self.coordinate_tracking = [None]

        self.manhattan_distance = 0 #manhattan distance

        # Set 2d array of ship equal to initial array passed in
        self.inventory_array = copy.deepcopy(inventory_array)
        self.buffer_inventory = copy.deepcopy(buffer_inventory)

        # Parent
        self.parent = parent
        # Crane current x coord
        self.craneRow = craneRow
        # Crane current y coord
        self.craneCol = craneCol
        # Heuristic
        self.g = 0
        self.h = 0
        self.cost= 0

        # Holds contaner row and col location to be removed after container is dropped off in new location
        self.removeRow = removeRow
        self.removeCol = removeCol

        # Holds None value if crane is empty or container object is crane is carrying container
        self.crane = craneContainer
        # Bool to show if crane is empty or not
        if(self.crane==None):
            self.craneEmpty = True
        else:
            self.craneEmpty = False

    # CLASS METHODS
    def __repr__(self):
        return self.name
    
    # Calculate Heuristic h(n)
    def calc_heuristic(self, hn):
        
        # Make a copy of ship grid obj to modify
        current_grid = Grid(self.inventory_array, self.buffer_inventory, self.removeRow, self.removeCol, self.parent, self.craneRow, self.craneCol, self.crane)
        # If already balanced and buffer is empty, return h(n) = 0
        if current_grid.check_goal() >= .9 and current_grid.check_bufferEmpty():
            return hn
        
        # Create a list of all container weights that do not equal 0
        all_containers = []
        for row in range(0,current_grid.row):
            for col in range(0,current_grid.col):
                if current_grid.inventory_array[row][col].weight != 0:
                    all_containers.append(current_grid.inventory_array[row][col].weight)

        # If h(n) > number of containers on the ship, impossible case
        if hn > len(all_containers):
            print("IMPOSSIBLE CASE: Ship cannot be balanced!")
            return None
    
        # Get left and right side of ship weights
        leftWeight = current_grid.leftWeight()
        rightWeight = current_grid.rightWeight()
        # Calc balance mass
        balanceMass = (leftWeight+rightWeight)/2

        #calc weight deficits of each side
        leftDeficit = balanceMass-leftWeight
        rightDeficit = balanceMass-rightWeight

        # Sort elements on left side by weight
        list_to_sort = []

        # If left side heavier and buffer empty, sort weights on left side to see how many need to be moved
        if leftWeight > rightWeight and current_grid.check_bufferEmpty():
            for row in range(0,current_grid.row):
                for col in range(0,6):
                    if current_grid.inventory_array[row][col].weight != 0:
                        list_to_sort.append([current_grid.inventory_array[row][col].weight, row, col])
            # Create a sorted list of container weights from lowest weight to highest weight
            sorted_list = sorted(list_to_sort, key=lambda x: x[0], reverse=False)

            # if a container on the left side = deficit on right side
            hn_found = False
            for i in range(0,len(sorted_list)):
                if sorted_list[i][0] == rightDeficit:
                    hn = hn+1
                    hn_found = True
            if(hn_found == True):
                return hn
    
            # If no container weight exactly matches the right deficit
            # Find weight closest to right deficit
            closest_weight = min(sorted_list, key=lambda x:abs(x[0]-rightDeficit))
            rightWeight = rightWeight + closest_weight[0]
            rightDeficit = rightDeficit - closest_weight[0]
            leftWeight = leftWeight - closest_weight[0]
            temp_container = current_grid.inventory_array[closest_weight[1]][closest_weight[2]]
            current_grid.inventory_array[closest_weight[1]][closest_weight[2]] = Container("UNUSED", closest_weight[1]+1, closest_weight[2]+1, 0)
            # Place container in closest unused spot on the other side
            placed = False
            # Start at bottom row
            row = 0
            while placed == False and row < len(current_grid.inventory_array):
                if current_grid.inventory_array[row][6].name == "UNUSED":
                    current_grid.inventory_array[row][6] = temp_container
                    placed = True
                row = row + 1
            hn = hn + 1
            # Recursive call with updated hn and ship state
            hn = current_grid.calc_heuristic(hn=hn)

        # If right side heavier and buffer empty, sort weights on right side to see how many need to be moved
        elif leftWeight < rightWeight and current_grid.check_bufferEmpty():
            for row in range(0,current_grid.row):
                for col in range(6,12):
                    if current_grid.inventory_array[row][col].weight != 0:
                        list_to_sort.append([current_grid.inventory_array[row][col].weight, row, col])
            # Create a sorted list of container weights from lowest weight to highest weight
            sorted_list = sorted(list_to_sort, key=lambda x: x[0], reverse=False)

            # if a container on the right side = deficit on left side
            hn_found = False
            for i in range(0,len(sorted_list)):
                if sorted_list[i][0] == leftDeficit:
                    hn = hn+1
                    hn_found = True
            if(hn_found == True):
                return hn
            
            # If no container weight exactly matches the left deficit
            # Find weight closest to left deficit
            closest_weight = min(sorted_list, key=lambda x:abs(x[0]-leftDeficit))
            leftWeight = leftWeight + closest_weight[0]
            leftDeficit = leftDeficit - closest_weight[0]
            rightWeight = rightWeight - closest_weight[0]
            temp_container = current_grid.inventory_array[closest_weight[1]][closest_weight[2]]
            current_grid.inventory_array[closest_weight[1]][closest_weight[2]] = Container("UNUSED", closest_weight[1]+1, closest_weight[2]+1, 0)
            # Place container in closest unused spot on the other side
            placed = False
            # Start at bottom row
            row = 0
            while placed == False and row < len(current_grid.inventory_array):
                if current_grid.inventory_array[row][5].name == "UNUSED":
                    current_grid.inventory_array[row][5] = temp_container
                    placed = True
                row = row + 1
            hn = hn + 1
            # Recursive call with updated hn and ship state
            hn = current_grid.calc_heuristic(hn=hn)

        # If left side heavier and buffer is not empty
        elif leftWeight > rightWeight and (current_grid.check_bufferEmpty() == False):

            list_to_sort_buffer = []
            buffer_list = []
            # First sort buffer weights to see if they can balance ship without moving any containers already on ship
            for row in range(0,current_grid.bufferRow):
                for col in range(0,current_grid.bufferCol):
                    if current_grid.buffer_inventory[row][col].weight != 0:
                        list_to_sort_buffer.append([current_grid.buffer_inventory[row][col].weight, row, col])
            # Create a sorted list of buffer container weights from lowest weight to highest weight
            buffer_list = sorted(list_to_sort_buffer, key=lambda x: x[0], reverse=False)

            # If there is only one container in the buffer and it matches the right weight deficit, return h(n)=1
            hn_found = False
            for i in range(0,len(buffer_list)):
                if buffer_list[i][0] == rightDeficit and (len(buffer_list)==1):
                    hn = hn+1
                    hn_found = True
            if(hn_found == True):
                return hn
            
            # If there is more than one container in buffer or container weight does not match right deficit
            # Find weight closest to right deficit
            closest_weight = min(buffer_list, key=lambda x:abs(x[0]-rightDeficit))
            rightWeight = rightWeight + closest_weight[0]
            rightDeficit = rightDeficit - closest_weight[0]
            # Update ship and buffer state
            temp_container = current_grid.buffer_inventory[closest_weight[1]][closest_weight[2]]
            current_grid.buffer_inventory[closest_weight[1]][closest_weight[2]] = Container("UNUSED", closest_weight[1]+1, closest_weight[2]+1, 0)
            # Place container in closest unused spot on the unbalanced (right) side
            placed = False
            # Start at bottom row
            row = 0
            while placed == False and row < len(current_grid.inventory_array):
                if current_grid.inventory_array[row][6].name == "UNUSED":
                    current_grid.inventory_array[row][6] = temp_container
                    placed = True
                row = row + 1
            hn = hn + 1
            # Recursive call with updated hn and buffer state
            hn = current_grid.calc_heuristic(hn=hn)


        # If right side heavier and buffer is not empty
        elif leftWeight < rightWeight and (current_grid.check_bufferEmpty() == False):

            list_to_sort_buffer = []
            buffer_list = []
            # First sort buffer weights to see if they can balance ship without moving any containers already on ship
            for row in range(0,current_grid.bufferRow):
                for col in range(0,current_grid.bufferCol):
                    if current_grid.buffer_inventory[row][col].weight != 0:
                        list_to_sort_buffer.append([current_grid.buffer_inventory[row][col].weight, row, col])
            # Create a sorted list of buffer container weights from lowest weight to highest weight
            buffer_list = sorted(list_to_sort_buffer, key=lambda x: x[0], reverse=False)

            # If there is only one container in the buffer and it matches the left weight deficit, return h(n)=1
            hn_found = False
            for i in range(0,len(buffer_list)):
                if buffer_list[i][0] == leftDeficit and (len(buffer_list)==1):
                    hn = hn+1
                    hn_found = True
            if(hn_found == True):
                return hn
            
            # If there is more than one container in buffer or container weight does not match left deficit
            # Find weight closest to right deficit
            closest_weight = min(buffer_list, key=lambda x:abs(x[0]-leftDeficit))
            leftWeight = leftWeight + closest_weight[0]
            leftDeficit = leftDeficit - closest_weight[0]
            # Update ship and buffer state
            temp_container = current_grid.buffer_inventory[closest_weight[1]][closest_weight[2]]
            current_grid.buffer_inventory[closest_weight[1]][closest_weight[2]] = Container("UNUSED", closest_weight[1]+1, closest_weight[2]+1, 0)
            # Place container in closest unused spot on the unbalanced (left) side
            placed = False
            # Start at bottom row
            row = 0
            while placed == False and row < len(current_grid.inventory_array):
                if current_grid.inventory_array[row][1].name == "UNUSED":
                    current_grid.inventory_array[row][1] = temp_container
                    placed = True
                row = row + 1
            hn = hn + 1
            # Recursive call with updated hn and buffer state
            hn = current_grid.calc_heuristic(hn=hn)
            
        return hn

    def manhattan(self, tempRow, tempCol):
        dis = abs(self.craneRow - tempRow) + abs(self.craneCol - tempCol)

        return dis
    
    # Removes container from ship grid
    def remove_container(self, row, col):
        self.inventory_array[row][col] = Container("UNUSED", row+1, col+1, 0)

    # Removes container from buffer
    def remove_container_buffer(self, row, col):
        self.buffer_inventory[row][col] = Container("UNUSED", row+1, col+1, 0)

    # Removes container from ship grid
    def remove_crane_container(self):
        self.crane = None

    # Computes Left side weight
    def leftWeight(self):
        totalWeight = 0

        for row in range(0,self.row):
            for col in range (0,6):
                totalWeight = totalWeight + self.inventory_array[row][col].weight
        
        return totalWeight

    # Computes ride side weight
    def rightWeight(self):
        totalWeight = 0

        for row in range(0,self.row):
            for col in range (6,12):
                totalWeight = totalWeight + self.inventory_array[row][col].weight

        return totalWeight
    
    # Computes and returns weight ratio
    def check_goal(self):
        weightRatio = ((min(self.rightWeight(), self.leftWeight()))/(max(self.rightWeight(), self.leftWeight())))
        return weightRatio

    # check buffer empty
    def check_bufferEmpty(self):
        empty=True
        for row in range(0,self.bufferRow):
            for col in range(0, self.bufferCol):
                if self.buffer_inventory[row][col].name != "UNUSED":
                    empty = False
        return empty

    #Grid print of the names
    def printGridNames(self):
        lines = []
        for row in reversed(self.inventory_array):
            lines.append(' '.join(str(container.name) for container in row))
        print('\n'.join(lines))
        print()

    #Grid print of the weights
    def printGridWeights(self):
        lines = []
        for row in reversed(self.inventory_array):
            lines.append(' '.join(str(container.weight) for container in row))
        print('\n'.join(lines))
        print()

    def valid_move(self, col):
            response = [False, None, None, None]
            below_row = None
            if self.craneEmpty: #if the crane is empty and we want to pick up a container
                for row in range(8,-1,-1):
                    if self.inventory_array[row][col].name != "UNUSED" and self.inventory_array[row][col].name != "NAN":
                        response = [True, row, col, self.inventory_array[row][col]]
                        self.removeRow = row
                        self.removeCol = col
                        return response
            else:
                for row in range(8,0,-1):#if the crane is not empty and we want to drop a container
                    below_row = row - 1
                    if self.inventory_array[row][col].name == "UNUSED" and self.inventory_array[below_row][col].name != "UNUSED":
                        response = [True, row, col, self.inventory_array[row][col]]
                        return response
                if below_row == 0 and self.inventory_array[below_row][col].name == "UNUSED":
                        response = [True, below_row, col, self.inventory_array[row][col]] #POTENTIAL PROBLEM: Changed row to below_row
                        return response
            return response
    
    def valid_move_buffer(self, col):
            col = col - 12
            response = [False, None, None, None]
            below_row = None
            if self.craneEmpty: #if the crane is empty and we want to pick up a container from buffer
                for row in range(4,-1,-1):
                    if self.buffer_inventory[row][col].name != "UNUSED":
                        response = [True, row, col, self.buffer_inventory[row][col]]
                        self.removeRow = row
                        self.removeCol = col
                        return response
            else:
                for row in range(4,0,-1):#if the crane is not empty and we want to drop a container in buffer
                    below_row = row - 1
                    if self.buffer_inventory[row][col].name == "UNUSED" and self.buffer_inventory[below_row][col].name != "UNUSED":
                        response = [True, row, col, self.buffer_inventory[row][col]]
                        return response
                if below_row == 0 and self.buffer_inventory[below_row][col].name == "UNUSED":
                        response = [True, below_row, col, self.buffer_inventory[row][col]] #POTENTIAL PROBLEM: Changed row to below_row
                        return response
            return response

    # Adds a cost of 1 when moving to buffer (should be cost of 4 after implementing heuristics)
    def move_fromShip_toBuffer(self):
        self.cost = self.cost + 1

    def operators(self, case):
        inShip = None
        result = None
        # Verify case is a valid column num
        if case >= 0 and case <= 11:
            response = self.valid_move(case)
            pass_state = response[0]
            temp_row = response[1]
            temp_col = response[2]
            temp_container = response[3]
            inShip = True
        elif case >= 12 and case <= 35:
           response = self.valid_move_buffer(case)
           pass_state = response[0]
           temp_row = response[1]
           temp_col = response[2]
           temp_container = response[3]
           inShip = False
        else:
            # Invalid case
            response = None
            pass_state = None
            temp_row = None
            temp_col = None
            temp_container = None
            inShip = None
            result = None

        self.buffer_pickup = False
        if pass_state and self.craneEmpty and inShip:#Ship Pickup
            #print("Valid move: Pickup Container (row, col) --> (" + str(temp_row) + ", " + str(temp_col) + ")")
            result = Grid(self.inventory_array, self.buffer_inventory, parent=None, removeRow=temp_row, removeCol=temp_col, craneRow=temp_row, craneCol=temp_col, craneContainer = temp_container)
        elif pass_state and not self.craneEmpty and inShip:#Ship Dropoff
            #print("Valid move: Dropoff Container (row, col) --> (" + str(temp_row) + ", " + str(temp_col) + ")")
            result = Grid(self.inventory_array, self.buffer_inventory, parent=None, removeRow=self.removeRow, removeCol=self.removeCol, craneRow=temp_row, craneCol=temp_col, craneContainer = None)
            result.inventory_array[temp_row][temp_col] = self.crane
            result.remove_container(result.removeRow, result.removeCol)
            # Update coord array ([intital coordinates, new coordinates])
            if self.buffer_pickup == True:
                result.coordinate_tracking = [[result.removeRow,result.removeCol], "Buffer", [temp_row,temp_col], "Ship"]
            else:
                result.coordinate_tracking = [[result.removeRow,result.removeCol], "Ship", [temp_row,temp_col], "Ship"]
            result.remove_crane_container()

        if pass_state and self.craneEmpty and not inShip:#Buffer Pickup
            #print("Valid move: Pickup Container (row, col) --> (" + str(temp_row) + ", " + str(temp_col) + ")")
            result = Grid(self.inventory_array, self.buffer_inventory, parent=None, removeRow=temp_row, removeCol=temp_col, craneRow=temp_row, craneCol=temp_col, craneContainer = temp_container)
            self.buffer_pickup = True
        elif pass_state and not self.craneEmpty and not inShip:#Buffer Dropoff
            #print("Valid move: Dropoff Container (row, col) --> (" + str(temp_row) + ", " + str(temp_col) + ")")
            result = Grid(self.inventory_array, self.buffer_inventory, parent=None, removeRow=self.removeRow, removeCol=self.removeCol, craneRow=temp_row, craneCol=temp_col, craneContainer = None)
            result.buffer_inventory[temp_row][temp_col] = self.crane
            if self.buffer_pickup == True:
                result.coordinate_tracking = [[result.removeRow,result.removeCol], "Buffer", [temp_row,temp_col], "Buffer"]
            else:
                result.coordinate_tracking = [[result.removeRow,result.removeCol], "Ship", [temp_row,temp_col], "Buffer"]
            result.remove_container_buffer(result.removeRow, result.removeCol)
            result.remove_crane_container()
        
        # Return new state of ship grid after picking up/dropping off container
        return result
    