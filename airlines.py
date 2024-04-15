#!/usr/bin/env python3

'''

CS 431/631 Project

Authors:
    Alexander Ram
    Mason Smith
    Thomas Braun

'''

import getopt
import os
import subprocess
import sys

def displayMenu(cols, rows, debug):
    option = ''
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
    debug = False
    unicodeEnabled = False
    menuActive = True
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
    if debug:
        print(f"active window is {cols} columns, {rows} rows")
        try:
            s = subprocess.getstatusoutput(f"locale | head -n 1")
            if 'UTF-8' in s[1]:
                unicodeEnabled = True
        except:
            pass
        if unicodeEnabled:
            print("Unicode compatible\n")
        else:
            print("Unicode NOT compatible\n")
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
