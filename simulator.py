import csv
import random
import time
import os
import sys
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from location import Location
from indication import Indication
from drone import Drone
# part 1 get the indiciation and calculate the road of the next 5 km with the speed of 100 km/h and make csv file fro this
class Simulator:
    def __init__(self, drone, indication, attacker):
        self.drone = drone
        self.indication = indication
        self.time = 0
        self.location = self.indication.location
        self.direction = self.indication.direction
        self.road = []
        self.attacker = attacker
        
    def calculate_road(self):
        road = []
        for i in range(5):
            road.append(self.location)
            self.location = self.location + self.direction * self.speed
        self.road = road
        return road
    
    def write_csv(self):
        with open('road.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['x', 'y'])
            for location in self.road:
                writer.writerow([location.x, location.y])





