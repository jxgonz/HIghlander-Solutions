# Container Class
class Container:
    def __init__(self, name, coordinates):
        # String name of the Container
        self.name = name
        # Tuple of integers [x, y]
        self.coordinates = coordinates

    def __repr__(self):
        return self.name
    
    # Operator should be a tuple of int
    def move(self, operator):
        self.coordinates = self.coordinates + operator

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates

    def containerLoaded(self):
        self.needsLoad = False
    
    def containerUnloaded(self):
        self.needsUnload = False

    # Check that returns a boolean value if the container has been
    # successfully loaded/unloaded, and is validly placed. Valid
    # placement based off of the space below the container. True
    # if the cell below is either a NAN cell or cell containing
    # a container.
    def containerSuccess(self, cellBelowExists):
        if not self.needsUnload and not self.needsLoad:
            if cellBelowExists:
                self.success = True
        else:
            self.success = False



    
