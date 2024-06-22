from indication import Indication
import time
import math
class Attacker:
    def __init__(self,Indication):
        self.height =1500
        self.speed_kmh = 213
        self.speed_mps = self.speed_kmh * 1000 / 3600  # 
        self.duration_seconds = 5 * 60  # battery
        self.indication = Indication
        
    #get and set methods fir speed
    def get_height(self):
        return self.height
        
    def move(self):
        direction_rad = math.radians(self.direction)
        self.location.x += self.speed_mps * math.cos(direction_rad)
        self.indication.y += self.speed_mps * math.sin(direction_rad)
    