class Path:
    def __init__(self, axis, name):
        self.axis = axis 
        self.name = name 

    def __str__(self):
        return "{}::{}".format(self.axis, self.name)

    
