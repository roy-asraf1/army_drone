class Location:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"
    
    #get and set methods
    def get_x(self):
        return self.x
    
    def set_x(self, x):
        self.x = x
        
    def get_y(self):
        return self.y
    
    def set_y(self, y):
        self.y = y
        
    def get_z(self):
        return self.z
    
    def set_z(self, z):
        self.z = z