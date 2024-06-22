'''
miz:744291
northern:681351
azimuth: 145

miz: 743379 
northern: 676114
height:80

'''
import unittest
from location import Location

class TestLocation(unittest.TestCase):
    def test_distance(self):
        loc1 = Location(0, 0, 0)
        loc2 = Location(3, 4, 0)
        self.assertAlmostEqual(loc1.distance(loc2), 5.0)

if __name__ == '__main__':
    unittest.main()
