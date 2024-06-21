from indication import Indication
import time
class Attacker:
    def __init__(self,Indication ):
        self.height =1500
        self.speed_kmh = 213
        self.speed_mps = self.speed_kmh * 1000 / 3600  # מהירות במטרים לשניה
        self.duration_seconds = 5 * 60  # battery
        self.indication = Indication
        
    #get and set methods fir speed
    def get_height(self):
        return self.height
    