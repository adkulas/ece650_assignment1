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

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = 'Welcome to the camera optimizer program. Type help or ? to list commands'
        self.graph = Graph()
    
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
    program.prompt = '=-> ' 
    program.use_rawinput = False
    program.cmdloop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))