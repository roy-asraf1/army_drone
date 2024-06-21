from location import Location
class drone:
    def __init__(self,Location):
        self.speed_kmh = 213
        self.speed_mps = self.speed_kmh * 1000 / 3600  # מהירות במטרים לשניה
        self.duration_seconds = 5 * 60  # battery
        self.Location = Location
        
