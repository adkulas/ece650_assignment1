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

    def test_intersection_overlap(self):
        #Check endpoint intersect
        result = a1ece650.intersect((0, 0), (5, 5), (-1,-1), (6, 6))
        self.assertEqual(result, (None, None))

    def test_parse_valid_input(self):
        string = '"King St West" (1,2)(2,3) (5,6)'
        result = a1ece650.parse(string)
        self.assertEqual(result, ['king st west', [(1,2),(2,3),(5,6)]])

    def test_parse_valid_input_empty(self):
        string = '"King St West"'
        result = a1ece650.parse(string)
        self.assertEqual(result, ['king st west', None])

    def test_parse_valid_input_empty_2(self):
        string = '"King St West"       '
        result = a1ece650.parse(string)
        self.assertEqual(result, ['king st west', None])

    def test_parse_missing_parentheses(self):
        string = '"King St West" (1,2)(2,3) 5,6)'
        result = a1ece650.parse(string)
        self.assertEqual(result, ['king st west', None])
    
    def test_parse_invalid_coord_toofew(self):
        string = '"King St West" (12)(2,3)(5,6)'
        result = a1ece650.parse(string)
        self.assertEqual(result, ['king st west', None])
    
    def test_parse_invalid_coord_toomany(self):
        string = '"King St West" (1,2,3)(2,3)(5,6)'
        result = a1ece650.parse(string)
        self.assertEqual(result, ['king st west', None])

if __name__ == '__main__':
    unittest.main()
