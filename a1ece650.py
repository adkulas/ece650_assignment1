from __future__ import print_function
from __future__ import division
import sys
import shlex
import cmd
import argparse
import re

print(sys.executable)
print(sys.version_info)
class Cameraprog(cmd.Cmd):
    intro = 'Welcome to the camera optimizer program. Type help or ? to list commands'
    prompt = '=->'
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
        print('doing command a with', args)
        print(parse(args))
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
        self.edges = {}
    
    def __str__(self):
        string = 'V = {\n'
        for k, v in self.vertices:
            string += '{0}: ({1:.2f})\n'.format(str(k),str(v))
        string += '}\nE = {\n'
        for k, v in self.edges:
            string += '<{0},{1}>,\n'.format(v[0],v[1])
        string += '\n}'
        
        print('This is the history of commands')
        print(self.history)

        return string

    def add_street(self, street, vertices):
        # type: (str, list) -> Bool
        if vertices:
            if street in self.history:
                print('Error: You already have {0} in the graph'.format(street))
            else:
                self.history[street] = vertices
                return True
        else:
            print('Error: a command has no vertices specified')

        return False

    def change_street(self, street, vertices):
        # type: (str, list) -> Bool
        if vertices:
            if street in self.history:
                self.history[street] = vertices
            else:
                print('Error: c specified for a street \"{0}\" that does not exist'.format(street))
                return True
        else:
            print('Error: c command has no vertices specified')

        return False

    def remove_street(self, street, *args):
        # type: (str, list) -> Bool
        if street in self.history:
            del self.history[street]
            return True
        else:
            print('Error: r specified for a street \"{0}\" that does not exist'.format(street))
        
        return False

def parse(args):
    """return a list [street, [list of points]]"""
    tmp = shlex.split(args)
    street = tmp[0].lower()
    if len(tmp) > 1:
        vertices = ''.join(tmp[1:])
        # matches (dig, dig) including whitespaces
        # regex = '\((\s*\d+\s*)?,(\s*\d+\s*)?\)+?'
        # match everything between '(' and ')'
        regex = r'\((.+?)\)+?'
        vertices = re.findall(regex, vertices)
        parsed_vertices = []
        try:        
            for vertex in vertices:
                parsed_vertices.append(tuple([int(x) for x in vertex.split(',')]))  
        except:
            print('Error: Vertices entered could not be parsed')
            parsed_vertices = None
        
        if len(parsed_vertices) == 0:
            print('Error: No valid vertices were entered')
            parsed_vertices = None
    else:
        parsed_vertices = None
    
    parsed_args = [street, parsed_vertices]
 
    return parsed_args

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
        xcoor = None
        ycoor = None
        return (xcoor, ycoor)

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
        xcoor = None
        ycoor = None

    return (xcoor, ycoor)

def main(args):
    program = Cameraprog()
    program.cmdloop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))