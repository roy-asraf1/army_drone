class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"
    
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2 +(self.z -other.z)**2)**0.5
