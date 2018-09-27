## A simple unit test example. Replace by your own tests
from __future__ import print_function
from __future__ import division
import sys
import unittest
import a1ece650

class MyTest(unittest.TestCase):

    def test_intersection_basic(self):
        """Test intersection method"""
        #Check simple intersection of two lines
        result = a1ece650.intersect((0, 0), (2, 2), (2, 0), (0, 2))
        self.assertEqual(result, (1.0, 1.0))

    def test_intersection_interval(self):
        #Check out of interval
        result = a1ece650.intersect((0, 5), (5, 5), (0, 0), (6, 5))
        self.assertEqual(result, (None, None))
    
    def test_intersection_endpoint(self):
        #Check endpoint intersect
        result = a1ece650.intersect((0, 5), (5, 5), (0,0), (5, 5))
        self.assertEqual(result, (5.0, 5.0))

if __name__ == '__main__':
    unittest.main()
