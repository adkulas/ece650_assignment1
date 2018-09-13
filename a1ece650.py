'''
Some notes:
Look into cmd module https://stackoverflow.com/questions/17352630/creating-a-terminal-program-with-python
https://code.activestate.com/recipes/280500-console-built-with-cmd-object/
'''

import sys
import shlex
import argparse
import re

def parse(line):
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


    

    #check for starting and ending quotes


def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    while True:
        line = sys.stdin.readline()
        if line == '\n':
            break
        print 'read a line:', line
        command, street_name, coords = parse(line)


    print 'Finished reading input'
    # return exit code 0 on successful termination
    sys.exit(0)

if __name__ == '__main__':
    main()