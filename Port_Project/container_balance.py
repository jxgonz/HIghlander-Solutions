# Container Class
class Container:

    def __init__(self, name, x, y, weight):
        # String name of the Container
        self.name = name
        # X coord
        self.x = x
        # Y coord
        self.y = y

        self.coordinates = (x,y)
        # Weight
        self.weight = weight

    def __repr__(self):
        return self.name
        



    
