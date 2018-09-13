import sys
import shlex
import cmd
import argparse
import re
print sys.executable
class Cameraprog(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = 'Welcome to the camera optimizer program. Type help or ? to list commands'

    def do_a(self, line):
        print 'doing command /"a/"'
    
    def help_a(self):
        print 'this is help string for \"a"'

    def do_r(self, line):
        print 'doing command /"r/"'

    def do_c(self, line):
        print 'doing command /"c/"'

    def do_g(self, line):
        print 'doing command /"g/"'

    def precmd(self, line):
        return line

    def postcmd(self, stop, line):
        #If line empty, exit program
        if not line:
            stop = True
        return stop

    def postloop(self):
        #Cleanup and gracefully exit
        sys.exit(0)

    def default(self, line):
        print 'Error: The command you entered was not found'
        print line

    def emptyline(self):
        pass
        
def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['a','c','r','g'])
    parser.add_argument('street_name')
    parser.add_argument('coords', nargs='+')
    try:
        args = parser.parse_args(shlex.split(line))
    except SystemExit:
        print 'FAILURE ABORT'
        return False
    check_coordinate_input(args.coords)
    print args.coords
    return args.command, args.street_name, args.coords

def check_coordinate_input(coords):
    if len(coords)==0:
        print "Error: No coordinates were entered"
        return False
    for coord in coords:
        if not(coord.startswith('(') and coord.endswith(')')):
            print 'Error: coordinate \"%s\" does not start with \'(\' and end with \')\'' % coord

def main(args):
    program = Cameraprog()
    program.prompt = '=-> ' 
    program.use_rawinput = False
    program.cmdloop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))