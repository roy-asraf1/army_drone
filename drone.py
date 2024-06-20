class Drone:
    def __init__(self, start_location):
        self.speed = 0
        self.maxSpeed_x = 100
        self.maxSpeed_y = 100
        self.maxSpeed_z = 100
        self.location = start_location
    
    def __str__(self):
        return f"Drone at {self.location}"
    
    #get and set methods
    def get_speed(self):
        return self.speed
    
    def set_speed(self, speed):
        self.speed = speed
        
    
        
    
        