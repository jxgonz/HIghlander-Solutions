# Container Class
class Container:
    def __init__(self, name, coordinates, needsLoad, needsUnload):
        # String name of the Container
        self.name = name
        # Tuple of integers [x, y]
        self.coordinates = coordinates
        # Boolean value: True if the container needs to be loaded
        self.needsLoad = needsLoad
        # Boolean value: True if the container needs to be unloaded
        self.needsUnload = needsUnload
        self.success = False

    # Operator should be a tuple of int
    def move(self, operator):
        self.coordinates = self.coordinates + operator

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

    # In relation to the project, an example use would be:
    # 
    # If a container needs to be loaded, it's coordinates would be the pink box?
    # containerA = Container("walMart", [1,10], True, False)
    # containerB = Container("target", [1,2], False, True)

    # If a container is already on the ship and doesn't need to be loaded,
    # both parameters are False to signifiy no transfer needed.
    # containerC = Container("cat", [1,3], False, False)
    # 
    # After operations, we can check if a container is successfully placed
    # containersList = [containerA, containerB, containerC]
    # if all containersList.success
    #   problem.Solved()
        



    
