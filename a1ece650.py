from __future__ import print_function
from __future__ import division
import sys
import shlex
import cmd
import argparse
import re
import itertools
import copy
import math

print(sys.executable)
print(sys.version_info)
class Cameraprog(cmd.Cmd):
    intro = 'Welcome to the camera optimizer program. Type help or ? to list commands'
    prompt = '(Assignment 1)=-> '
    use_rawinput = 0

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.graph = Graph()
    
    def parseline(self, line):
        """OVERRIDE parseline method
        Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        elif line[0] == '!':
            if hasattr(self, 'do_shell'):
                line = 'shell ' + line[1:]
            else:
                return None, None, line
        i, n = 0, len(line)
        while i < n and line[i] != ' ': i = i+1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line
    
    def do_a(self, args):
        """
        This is the help string for the add command
        """
        self.graph.add_street(*parse(args))

    def do_r(self, args):
        """
        This is the help string for the remove command
        """
        self.graph.remove_street(*parse(args))

    def do_c(self, args):
        """
        This is the help string for the change command
        """
        self.graph.change_street(*parse(args))

    def do_g(self, args):
        """
        This is the help string for the graph command
        """
        self.graph.render_graph()
        print(self.graph)

    def precmd(self, line):
        return line

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished.""" 
        #If line empty, exit program
        if not line:
            stop = True
        return stop
    def preloop(self):
        pass

    def postloop(self):
        #Cleanup and gracefully exit
        pass

    def default(self, line):
        print('Error: The command you entered was not found')
        print(line)

    def emptyline(self):
        pass    
class Graph(object):
    def __init__(self):
        self.history = {}
        self.vertices = {}
        self.edges = set([])
        self.intersections = set([])
        self.test = {}
    
    def __str__(self):
        string = 'V = {\n'
        for k, v in self.vertices.iteritems():
            if type(v[0]) == 'float' or type(v[1]) == 'float':
                xcoord, ycoord = round(v[0], 3), round(v[1], 3)
            else:
                xcoord, ycoord = v[0], v[1] 
            string += '{0}: ({1},{2})\n'.format( k, xcoord, ycoord)
        string += '}\nE = {\n'
        for edge in self.edges:
            tmp = list(edge)
            string += '<{0},{1}>,\n'.format(tmp[0],tmp[1])
        string = string[:-2] + '\n}'

        return string

    def add_street(self, street, vertices):
        # type: (str, List[Tuple(int, int), ...]) -> Bool
        if vertices:
            if street in self.history:
                print('Error: You already have \"{0}\" in the graph'.format(street))
            else:
                self.history[street] = vertices
                return True
        else:
            print('Error: a command has no vertices specified')

        return False

    def change_street(self, street, vertices):
        # type: (str, List[Tuple(int, int), ...]) -> Bool
        if vertices:
            if street in self.history:
                self.history[street] = vertices
                return True
            else:
                print('Error: c specified for a street \"{0}\" that does not exist'.format(street))
        else:
            print('Error: c command has no vertices specified')

        return False

    def remove_street(self, street, *args):
        # type: (str, List[Tuple(int, int), ...]) -> Bool
        if street in self.history:
            del self.history[street]
            return True
        else:
            print('Error: r specified for a street \"{0}\" that does not exist'.format(street))
        
        return False

    def old_render_graph(self):
        self.vertices = {}
        self.edges = set([])
        i = 1
        for street, vertices in self.history.iteritems():
            for index, vertex in enumerate(vertices):
                self.vertices[i] = vertex
                if index > 0:
                    self.edges.add(frozenset([i, i-1]))
                i += 1
        return

    def render_graph(self):
        self.vertices = {}
        self.edges = set([])

        tmp_graph = {}
        intersections = set([])
        for street, points in self.history.iteritems():
            tmp_graph[street] = []

            # loop through edges of street
            for i in xrange(len(points)-1):
                tmp_p_to_add = [] #need this list because can have more than one intersection per segement
                
                #Loop through all other streets to find intersections
                for street_2, points_2 in self.history.iteritems():
                    if street != street_2:
                        # loop through other streets segments
                        for j in xrange(len(points_2)-1):
                            inter_p = intersect(points[i], points[i+1], points_2[j], points_2[j+1])
                            if inter_p:
                                intersections.add(inter_p)
                                if ( inter_p != points[i] and inter_p != points[i+1] ):
                                    tmp_p_to_add.append(inter_p)
                        
                # add first point of segement if valid
                if (points[i] in intersections
                        or points[i+1] in intersections
                        or inter_p
                        or (tmp_graph[street] or [None])[-1] in intersections):
                    tmp_graph[street].append(points[i])

                # insert all intersections by order of distance to segment
                if len(tmp_p_to_add) > 1:
                    tmp_p_to_add = list(set(tmp_p_to_add)) # remove duplicates
                    tmp_dist = [distance(p, points[i]) for p in tmp_p_to_add]
                    tmp_dist, tmp_p_to_add = zip(*sorted(zip(tmp_dist, tmp_p_to_add))) # sort the list by distance
                for tmp_p in tmp_p_to_add:
                    tmp_graph[street].append(tmp_p)

            #add last point if valid
            if (tmp_graph[street][-1] in intersections):
                tmp_graph[street].append(points[-1])
        
        # build graph from tmp_graph
        i = 1
        for street, vertices in tmp_graph.iteritems():
            prev = 0
            for index, vertex in enumerate(vertices):
                # if vertex doesnt exist, add it
                if vertex not in self.vertices.values():
                    self.vertices[i] = vertex
                    if index > 0:
                        self.edges.add(frozenset([i, prev]))
                    prev = i
                    i += 1
                # if vertex exists then find the vertex id
                else:
                    for v_id, val in self.vertices.iteritems():
                        if vertex == val:
                            if index > 0:
                                self.edges.add(frozenset([v_id, prev]))
                                prev = v_id
        return
    
    def rem_render_graph(self):
        self.vertices = {}
        self.edges = set([])
        
        #Build initial polyline of each street with unique id
        i = 1
        data = {}
        self.vertices = {}
        for street, points in self.history.iteritems():
            tmp_edges = set([])
            for index, point in enumerate(points):
                self.vertices[i] = point
                if index > 0:
                    tmp_edges.add(frozenset([i, i-1]))
                i += 1
            data[street] = tmp_edges

        #Iterate through all edges to find intersections
        tmp_intersections = set([])
        for street, street_cmp in itertools.permutations(data.keys(),2):
            street_edges = list(data[street])
            street_cmp_edges = list(data[street_cmp])
            for street_edge in street_edges:
                for street_cmp_edge in street_cmp_edges:
                    v1, v2 = list(street_edge)
                    v3, v4 = list(street_cmp_edge)
                    inter = intersect(self.vertices[v1], self.vertices[v2], self.vertices[v3], self.vertices[v4])
                    if inter:
                        # check if intersection is already a vertex in graph
                        if inter in self.vertices.values():
                            tmp_intersections.add(inter)
                        # add it as new vertex
                        else:
                            self.vertices[i] = inter
                            tmp_intersections.add(inter)
                            i += 1
        
        #Now need to add intersections to the poly line for each street
        for street, edges in data.iteritems():
            print(street)
            new_edges = set([])
            
            for edge in edges:
                v_id_A, v_id_B = list(edge)   
                points_intersecting = []
                
                for point in tmp_intersections:
                    v_id_A, v_id_B = list(edge)
                    if point_is_on_line(self.vertices[v_id_A], self.vertices[v_id_B], point):
                        points_intersecting.append(point)
                



                        
                        #find vertex id in vertices dictionary and create new edge
                        # for v_id, coords in self.vertices.iteritems():
                        #     if coords == inter:    
                        #         data[street]['E'].remove(street_edge)
                        #         data[street]['E'].add(frozenset([v1, v_id]))
                        #         data[street]['E'].add(frozenset([v_id, v2]))

        # for edge in self.edges:
        #     for cmp_edge in self.edges:
        #         v1, v2 = list(edge)
        #         v3, v4 = list(cmp_edge)
        #         inter = intersect(self.vertices[v1], self.vertices[v2], self.vertices[v3], self.vertices[v4])
        #         print(inter)
        return


def parse(args):
    """return a list [street, [list of points]]"""
    tmp = shlex.split(args)
    street = tmp[0].lower()
    if len(tmp) > 1:
        vertices = ''.join(tmp[1:])
        
        #Check all vertices have open and closing parentheses
        open_paren_count = vertices.count('(')
        close_paren_count = vertices.count(')')
        if open_paren_count != close_paren_count:
            print('Error: Vertices entered are missing a parenthesis')
            return [street, None]

        # match everything between '(' and ')'
        regex = r'\((.*?)\)+?'
        vertices = re.findall(regex, vertices)
        parsed_vertices = []
        
        # Cast all inputs to tuples of type int
        try:        
            for vertex in vertices:
                coords = vertex.split(',')
                if len(coords) != 2:
                    raise Exception
                parsed_vertices.append(tuple([int(x) for x in coords]))  
        except:
            print('Error: Vertices entered could not be parsed')
            return [street, None]
        
        if (len(parsed_vertices) == 0 or
            len(parsed_vertices) != open_paren_count):
            
            print('Error: No valid vertices were entered')
            parsed_vertices = None
    else:
        parsed_vertices = None
    
    parsed_args = [street, parsed_vertices]
 
    return parsed_args

def distance(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2

    dist = math.sqrt((p1x-p2x)**2 + (p1y-p2y)**2)
    return dist

def intersect(p_1, p_2, p_3, p_4):
    # type: (Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]) -> Tuple[float, float]

    x1, y1 = p_1[0], p_1[1]
    x2, y2 = p_2[0], p_2[1]
    x3, y3 = p_3[0], p_3[1]
    x4, y4 = p_4[0], p_4[1]

    xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
    xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

    ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    try:
        xcoor =  xnum / xden    
        ycoor = ynum / yden
    except ZeroDivisionError:
        return None

    seg1_xmin = min(x1,x2)
    seg1_xmax = max(x1,x2)
    seg2_xmin = min(x3,x4)
    seg2_xmax = max(x3,x4)
    seg1_ymin = min(y1,y2)
    seg1_ymax = max(y1,y2)
    seg2_ymin = min(y3,y4)
    seg2_ymax = max(y3,y4)
    x_interval = (max(seg1_xmin, seg2_xmin), min(seg1_xmax, seg2_xmax))
    y_interval = (max(seg1_ymin, seg2_ymin), min(seg1_ymax, seg2_ymax))

    if (xcoor < x_interval[0] or xcoor > x_interval[1] or
        ycoor < y_interval[0] or ycoor > y_interval[1]):
        return None

    return ( round(xcoor,2), round(ycoor,2) )

def point_is_on_line(A, B, point):
    Ax, Ay = A
    Bx, By = B
    Px, Py = point

    # check vertical line
    if Ax == Bx:
        if (Px == Ax and
        Py >= min(Ay, By) and Py <= max(Ay, By)):
            return True
        else:
            return False
    # y = mx + b
    else:
        m = (By - Ay)/(Bx - Ax)
        b = Ay - m * Ax

    if (Py == m * Px + b and
        Px >= min(Ax, Bx) and Px <= max(Ax, Bx) and
        Py >= min(Ay, By) and Py <= max(Ay, By)):
        return True
    else:
        return False

def main(args):
    program = Cameraprog()
    program.cmdloop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

'''
test inputs:
a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)
a "King Street S" (4,2) (4,8)
a "Davenport Road" (1,4) (5,8)
g
c "Weber Street" (2,1) (2,2)
g
r "King Street S"
g
'''