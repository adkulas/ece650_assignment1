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
        self.assertEqual(result, [(1.0, 1.0)])

    def test_intersection_interval(self):
        #Check out of interval
        result = a1ece650.intersect((0, 5), (5, 5), (0, 0), (6, 5))
        self.assertEqual(result, [])
    
    def test_intersection_endpoint(self):
        #Check endpoint intersect
        result = a1ece650.intersect((0, 5), (5, 5), (0,0), (5, 5))
        self.assertEqual(result, [(5.0, 5.0)])

    def test_intersection_overlap_full(self):
        #Check overlapping lines
        result = a1ece650.intersect((0, 0), (5, 5), (-1,-1), (6, 6))
        self.assertEqual(result, [(0,0),(5,5)])

    def test_intersection_overlap_partial(self):
        #Check overlapping lines
        result = a1ece650.intersect((0, 0), (5, 5), (2,2), (6, 6))
        self.assertEqual(result, [(5,5),(2,2)])

    def test_parse_valid_input(self):
        string = '"King St West" (1,2)(2,3) (5,6)'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, ['king st west', [(1,2),(2,3),(5,6)]])

    def test_parse_valid_input_empty(self):
        string = '"King St West"'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, ['king st west', None])

    def test_parse_valid_input_empty_2(self):
        string = '"King St West"       '
        result = a1ece650.parse(string, '')
        self.assertEqual(result, ['king st west', None])

    def test_parse_missing_parentheses(self):
        string = '"King St West" (1,2)(2,3) 5,6)'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, False)
    
    def test_parse_invalid_coord_toofew(self):
        string = '"King St West" (12)(2,3)(5,6)'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, False)
    
    def test_parse_invalid_coord_toomany(self):
        string = '"King St West" (1,2,3)(2,3)(5,6)'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, False)

    def test_parse_invalid_street_name(self):
        string = '"King St-West" (1,3)(2,3)(5,6)'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, False)

    def test_parse_invalid_char_in_vertices(self):
        string = '"King St West" (1.0,3)(2,3)(5,6)'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, False)

    def test_parse_missing_closing_quote(self):
        string = '"King St West (1,3)(2,3)(5,6)'
        result = a1ece650.parse(string, '')
        self.assertEqual(result, False)

    def test_render_basic_intersection(self):
        graph = a1ece650.Graph()
        graph.add_street('King', [(0,0), (4,4)])
        graph.add_street('Weber', [(0,4), (4,0)])
        graph.render_graph()
        result = set(graph.vertices.keys())
        expected = { (0,0), (4,4), (0,4), (4,0), (2,2) }
        print(graph)
        self.assertEqual(result, expected)

    def test_render_vertical_overlapping_intersection(self):
        graph = a1ece650.Graph()
        graph.add_street('King', [(-1,0), (-1,5)])
        graph.add_street('Weber', [(-1,2), (-1,7)])
        graph.render_graph()
        result = set(graph.vertices.keys())
        expected = { (-1,0), (-1,5), (-1,2), (-1,7) }
        print(graph)
        self.assertEqual(result, expected)

    def test_render_complete_overlap_intersection(self):
        graph = a1ece650.Graph()
        graph.add_street('King', [(-3,5), (2,0)])
        graph.add_street('Weber', [(-1,3), (1,1)])
        graph.render_graph()
        result = set(graph.vertices.keys())
        expected = { (2,0), (-1,3), (1,1), (-3,5) }
        print(graph)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
