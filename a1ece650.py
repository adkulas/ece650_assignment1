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
        while i < n and line[i] in self.identchars: i = i+1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line
    
    def do_a(self, args):
        """
        This is the help string for the add command
        """
        print('doing command a with', args)
        print(parse(args))
        self.graph.add_street(parse(args))

    def do_r(self, args):
        """
        This is the help string for the remove command
        """
        print('doing command r')

    def do_c(self, args):
        """
        This is the help string for the change command
        """
        print('doing command c')

    def do_g(self, args):
        """
        This is the help string for the graph command
        """
        print ('doing command g')
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
        print('This is the history of commands')
        print(self.history)
        print('These are the vertices')
        print(self.vertices)
        print('These are the edges')
        print(self.edges)
        return '.'

    def add_street(self, args):
        street = args[0]
        vertices = args[1:]
        self.history[street] = vertices

def parse(args):
    args = shlex.split(args)
    return args

def check_coordinate_input(coords):
    if len(coords)==0:
        print("Error: No coordinates were entered")
        return False
    for coord in coords:
        if not(coord.startswith('(') and coord.endswith(')')):
            print('Error: coordinate \"%s\" does not start with \'(\' and end with \')\'') % coord

def main(args):
    program = Cameraprog()
    program.cmdloop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))