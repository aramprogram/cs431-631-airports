#!/usr/bin/env python3

'''

CS 431/631 Project

Authors:
    Alexander Ram
    .
    .

'''

import getopt
import os
import sys

def displayMenu(cols, rows, debug):
    option = ''
    if debug:
        print("active window is %d columns, %d rows" % (cols, rows))
    print("what do you want to do? ")
    print("1 - something")
    print("0 - leave")
    option = input()
    if option == '0':
        return False
    elif option == '1':
        return True
    else:
        print("not a valid option")
        return True


def print_help():
    print("Usage:  airports [-h]")
    print("        airports [-d] [OPTION]...")
    print("Search through the airports and airlines database.")
    print("Returns results in a tabulated text format.")
    print("\nCommand-line user interface is the default usage.")
    print("Line-by-line scripting is possible using the options below.")
    print("\nOptions:")
    print("  -h, --help               display this help screen")
    print("  -d, --debug              start program in debug mode")

def main(argv):
    path = ''
    menuActive = True
    debug = False
    cols, rows = os.get_terminal_size()
    try:
        opts, args = getopt.getopt(argv, "hd", ["help", "debug"])
    except getopt.GetoptError as err:
        # print help and exit
        print(err)
        print_help()
        sys.exit(2)
    debugString = "Program started in debug mode."
    for o, a in opts:
        if o in ("-h", "--help"):
            print_help()
            sys.exit()
        elif o in ("-d", "--debug"):
            print(debugString)
            debug = True
        else:
            assert False, "unhandled option"
    try:
        # debug code; edit this later
        x = 1
    except:
        # debug code; edit this later
        x = 1
    while menuActive == True:
        menuActive = displayMenu(cols, rows, debug)

if __name__ == '__main__':
    main(sys.argv[1:])
