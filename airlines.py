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
import psycopg2
import subprocess
import sys
from tabulate import tabulate

def connectToDatabase():
    connection = psycopg2.connect(dbname="CS431FinalProject" , user="postgres", password="postgres123", host="172.27.44.80", port=5432)
    cursor = connection.cursor()
    return connection, cursor

def closeDatabase(connection, cursor):
    connection.close()
    cursor.close()
    
def executeQuery(cursor , query):
    cursor.execute(query)
    return cursor.fetchall()
    
def query1():
    query = ""
    while not query:
      countryQuery = input("Enter the Country: ")
      query1 = f"SELECT DISTINCT airport_name FROM \"Airports\" WHERE country LIKE '%{countryQuery}%'"
      return query1

def query2():
     stopsQuery = int(input("Enter the Number of Stops: "))
     query2 = f"""SELECT DISTINCT al.name
     FROM \"Airlines\" al JOIN \"Routes\" r ON (r.airline_id = al.id)
     WHERE stops = '{stopsQuery}'
     """
     return query2

def query3():
    query3 = "SELECT DISTINCT name FROM \"Airlines\" WHERE id IN (SELECT airline_id FROM \"Routes\" WHERE codeshare = 'Y')"
    return query3

def query4():
    query4 = "SELECT DISTINCT name FROM \"Airlines\" WHERE active = 'Y'"
    return query4

def query5():
    query5 = "SELECT country, COUNT(airport_name) FROM \"Airports\" GROUP BY country ORDER BY COUNT(*) DESC LIMIT 1"
    return query5

def query6():
    query = ""
    while not query:
      kQuery = input("Enter How Many Cities You Would Like to Search For: ")
      inOutQuery = input("Enter Whether You're Searching for Incoming or Outgoing Airlines (Incoming, Outgoing): ")
      if inOutQuery == "Incoming":
        query6 = f"""SELECT ap.city, COUNT(DISTINCT r.airline) AS incoming_airlines_count
        FROM \"Routes\" r JOIN \"Airports\" ap ON (r.source_airport_id = ap.id)
        GROUP BY r.source_airport, ap.city
        ORDER BY incoming_airlines_count DESC
        LIMIT '{kQuery}'
        """
      elif inOutQuery == "Outgoing":
        query6 = f"""SELECT ap.city, COUNT(DISTINCT r.airline) AS outgoing_airlines_count
        FROM \"Routes\" r JOIN \"Airports\" ap ON (r.dest_airport_id = ap.id)
        GROUP BY r.dest_airport, ap.city
        ORDER BY outgoing_airlines_count DESC
        LIMIT '{kQuery}'
        """
      else:
        print("Please Enter a Valid Input. Ensure Your Input is Spelled Correctly and Capitalized.")
      return query6

def query7():
    query = ""
    while not query:
      cityQueryX = input("Enter the Source City IATA: ")
      cityQueryY = input("Enter the Destination City IATA: ")
      query7 = f"""SELECT al.name AS Airline_name,
      A1.airport_name AS source_airport_name,
      r.source_airport_id AS source_airport_id,
      A2.airport_name AS dest_airport_name,
      r.dest_airport_id AS dest_airport_id
      FROM \"Routes\" AS r
      INNER JOIN \"Airlines\" AS al ON (r.airline_id = al.id)
      INNER JOIN \"Airports\" AS A1 ON (r.source_airport_id = A1.id)
      INNER JOIN \"Airports\" AS A2 ON (r.dest_airport_id = A2.id)
      WHERE r.source_airport_id IN
      (SELECT source_airport_id FROM \"Routes\" WHERE source_airport LIKE '%{cityQueryX}%')
      AND r.dest_airport_id IN
      (SELECT dest_airport_id FROM \"Routes\" WHERE dest_airport LIKE '%{cityQueryY}%')
      """
      return query7

def query8():
    query = ""
    while not query:
      cityQueryX = input("Enter the Source City IATA: ")
      cityQueryY = input("Enter the Destination City IATA: ")
      stopsQueryZ = input("Enter the Maximum Number of Stops: ")
      query8 = f"""SELECT al.name AS Airline_name,
      A1.airport_name AS source_airport_name,
      r.source_airport_id AS source_airport_id,
      A2.airport_name AS dest_airport_name,
      r.dest_airport_id AS dest_airport_id,
      r.stops AS stops
      FROM \"Routes\" AS r
      INNER JOIN \"Airlines\" AS al ON (r.airline_id = al.id)
      INNER JOIN \"Airports\" AS A1 ON (r.source_airport_id = A1.id)
      INNER JOIN \"Airports\" AS A2 ON (r.dest_airport_id = A2.id)
      WHERE r.source_airport_id IN
      (SELECT source_airport_id FROM \"Routes\" WHERE source_airport LIKE '%{cityQueryX}%')
      AND r.dest_airport_id IN
      (SELECT dest_airport_id FROM \"Routes\" WHERE dest_airport LIKE '%{cityQueryY}%')
      AND r.stops <= '{stopsQueryZ}'
      """
      return query8

def query9():
    cityQueryX = input("Enter the Source City: ")
    hopsQueryD = input("Enter the Number of Hops: ")
    query9 = f"""SELECT ap.city, r.stops FROM \"Airports\" ap
    JOIN \"Routes\" r ON (r.source_airport_id = ap.id)
    WHERE ap.id IN
    (SELECT dest_airport_id FROM \"Routes\" WHERE source_airport_id IN
    (SELECT id FROM \"Routes\" WHERE source_airport LIKE '%{cityQueryX}%'))
    AND stops = '{hopsQueryD}'
    """
    return query9

def switch(userChoice):
    userChoice = int(userChoice)

    conn , cur = connectToDatabase()

    if userChoice == 1:
        result1 = executeQuery(cur , query1())
        print(tabulate(result1 , headers=["Airport Name"]))

    elif userChoice == 2:
        result2 = executeQuery(cur , query2())
        print(tabulate(result2 , headers=["Airline Name"]))

    elif userChoice == 3:
        result3 = executeQuery(cur , query3())
        print(tabulate(result3 , headers=["Airline Name"]))

    elif userChoice == 4:
        result4 = executeQuery(cur , query4())
        print(tabulate(result4 , headers=["Airport Name"]))

    elif userChoice == 5:
        result5 = executeQuery(cur , query5())
        print(tabulate(result5 , headers=["Country" , "Count"]))

    elif userChoice == 6:
        result6 = executeQuery(cur , query6())
        print(tabulate(result6 , headers=["City Name" , "Number of Flights"]))

    elif userChoice == 7:
        result7 = executeQuery(cur , query7())
        print(tabulate(result7 , headers=["Airline Name" , "Source Airport Name" , "Source Airport ID" , "Dest Airport Name" , "Dest Airport ID"]))

    elif userChoice == 8:
        result8 = executeQuery(cur , query8())
        print(tabulate(result8 , headers=["Airline Name" , "Source Airport Name" , "Source Airport ID" , "Dest Airport Name" , "Dest Airport ID" , "Stops"]))

    elif userChoice == 9:
        result9 = executeQuery(cur , query9())
        print(tabulate(result9 , headers=["City Name" , "Number of Stops"]))

    elif userChoice == 10:
        print("Placeholder")
        #test dfs on components
        #return query10()
    else:
        print("Invalid Input")

    closeDatabase(conn , cur)

class literal_sorcery():
    def __init__(self):
        self.out = ""
        self.plex = 0
    def __xor__(self, fg):
        self.out = self.out + "\x1b[38;2;"
        self.out = self.out + str(fg[0]) + ";"
        self.out = self.out + str(fg[1]) + ";"
        self.out = self.out + str(fg[2]) + "m"
        return self
    def __truediv__(self, bg):
        self.out = self.out + "\x1b[48;2;"
        self.out = self.out + str(bg[0]) + ";"
        self.out = self.out + str(bg[1]) + ";"
        self.out = self.out + str(bg[2]) + "m"
        return self
    def __floordiv__(self, instruction):
        self.out = self.out + "\x1b[" + str(instruction) + "m"
        return self
    def __mod__(self, nibble):
        self.plex *= 16
        self.plex += nibble
        return self
    def __lshift__(self, offset):
        if offset == 1:
            self.plex += 129792
        return self
    def __rshift__(self, offset):
        if offset != 0:
            return self
        elif self.plex != 0:
            self.out = self.out + chr(self.plex)
            self.plex = 0
            return self
        else:
            return self
    def __add__(self, string):
        self.out = self.out + string
        self.plex = 0
        return self
    def __neg__(self):
        self.out = ""
        self.plex = 0
        return self
    def __invert__(self):
        return self.out

# ticket
def ticket():
    back = [234, 215, 105]
    line = [211, 107, 57]
    dark = [57, 84, 211]
    s = literal_sorcery()
    for i in range(0, 10):
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    for i in range(0, 2):
        s = s % 2 % 0 << 0 >> 0
    s = s ^ back
    s = s % 4 % 9 << 1 >> 0
    s = s // 0
    s = s / back
    s = s ^ line
    for i in range(0, 12):
        s = s % 2 % 0 << 0 >> 0
        s = s % 2 % 13 << 0 >> 0
    s = s % 2 % 0 << 0 >> 0
    s = s // 0
    s = s ^ back
    s = s % 3 % 14 << 1 >> 0
    s = s // 0
    print(~s)
    s = -s
    s = s // 0
    for i in range(0, 10):
        s = s % 2 % 0 << 0 >> 0
    s = s ^ back
    s = s % 4 % 8 << 1 >> 0
    s = s % 4 % 6 << 1 >> 0
    s = s % 4 % 1 << 1 >> 0
    s = s // 0
    s = s / back
    s = s ^ line
    for i in range(0, 25):
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    s = s ^ back
    s = s % 4 % 12 << 1 >> 0
    s = s % 5 % 1 << 1 >> 0
    s = s % 3 % 13 << 1 >> 0
    s = s // 0
    print(~s)
    s = -s
    for i in range(0, 10):
        s = s % 2 % 0 << 0 >> 0
    s = s / back
    s = s ^ line
    s = s // 1
    s = s % 2 % 1 << 0 >> 0
    for i in range(0, 4):
        s = s % 2 % 0 << 0 >> 0
    s = s + "Airline Search Engine"
    for i in range(0, 4):
        s = s % 2 % 0 << 0 >> 0
    s = s % 2 % 1 << 0 >> 0
    s = s // 0
    print(~s)
    s = -s
    for i in range(0, 10):
        s = s % 2 % 0 << 0 >> 0
    s = s / back
    s = s ^ line
    s = s % 2 % 1 << 0 >> 0
    s = s ^ dark
    s = s // 1
    for i in range(0, 2):
        s = s % 2 % 0 << 0 >> 0
    s = s + "Your ticket to the skies!"
    for i in range(0, 2):
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    s = s / back
    s = s ^ line
    s = s % 2 % 1 << 0 >> 0
    s = s // 0
    print(~s)
    s = -s
    for i in range(0, 10):
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    s = s ^ back
    s = s % 6 % 3 << 1 >> 0
    s = s % 6 % 7 << 1 >> 0
    s = s % 5 % 2 << 1 >> 0
    s = s // 0
    s = s / back
    s = s ^ line
    for i in range(0, 25):
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    s = s ^ back
    s = s % 5 % 13 << 1 >> 0
    s = s % 5 % 12 << 1 >> 0
    s = s % 5 % 8 << 1 >> 0
    s = s // 0
    print(~s)
    s = -s
    for i in range(0, 10):
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    for i in range(0, 2):
        s = s % 2 % 0 << 0 >> 0
    s = s ^ back
    s = s % 6 % 6 << 1 >> 0
    s = s // 0
    s = s / back
    s = s ^ line
    for i in range(0, 12):
        s = s % 2 % 0 << 0 >> 0
        s = s % 2 % 13 << 0 >> 0
    s = s % 2 % 0 << 0 >> 0
    s = s // 0
    s = s ^ back
    s = s % 5 % 11 << 1 >> 0
    s = s // 0
    print(~s)

def grad(width, pos):
    maxw = 209.0
    minw = 49.0
    a = pos - width / 2.0 + 1.0
    b = maxw - minw
    c = (-width / 2.0 + 1.0) ** 2.0
    d = b / c
    e = d * a ** 2.0
    return int(maxw - e)

def menuBar():
    title = "  *  Menu - Enter a number to access a feature  *  "
    width = len(title)
    s = literal_sorcery()
    for i in range(0, width):
        s = s / [grad(width, i), 255, 255]
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    print(~s)
    s = -s
    s = s ^ [41, 28, 181]
    for i in range(0, width):
        s = s / [grad(width, i), 255, 255]
        s = s + title[i]
    s = s // 0
    print(~s)
    s = -s
    for i in range(0, width):
        s = s / [grad(width, i), 255, 255]
        s = s % 2 % 0 << 0 >> 0
    s = s // 0
    print(~s)

def displayMenu(cols, rows, uni):
    option = 0
    print("  1 - List all available airports in a country")
    print("  2 - List all airlines serving X number of airports")
    print("  3 - List all airlines that share flights with each other")
    print("  4 - List all airlines operating in a country")
    print("  5 - Which country has the highest number of airports?")
    print("  6 - Which cities have the most incoming/outgoing airlines?")
    print("  7 - Find a trip connecting city A and city B")
    print("  8 - Find a trip connecting city A and city B with less than X stops")
    print("  9 - Find all cities reachable from city A within X stops")
    print(" 10 - Fast Transitive closure/connected component implemented in parallel/distributed algorithms")
    print("  0 - Close program")
    validOption = False
    while validOption == False:
        try:
            option = int(input("  "))
            if option == 0:
                validOption = True
            elif option >= 1 and option <= 10:
                print("chose " + str(option))
                validOption = True
                queryOutput = switch(option)
            else:
                print("invalid option")
        except:
            option = 0
            print("invalid option")
    if option == 0:
        return False
    else:
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
    if (unicodeEnabled == True and debug == False) or unicodeEnabled == False:
        print("")
        ticket()
        print("")
        menuBar()
        print("")
    else:
        print("")
        print("     Airline Search Engine     ")
        print("   Your ticket to the skies!   ")
        print("")
    while menuActive == True:
        menuActive = displayMenu(cols, rows, unicodeEnabled)

if __name__ == '__main__':
    main(sys.argv[1:])
