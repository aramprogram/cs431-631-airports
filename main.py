import psycopg2
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

def query10():
    query = ""
    while not query:
      sQuery = ("Enter the ")
      query10 = f""

    return query10

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


print("Select an option from the following choices:")
print("1: List Airports operating in a specified country")
print("2: List airlines having specified number of stops")
print("3: List airlines operating within codeshare")
print("4: List active airports in the United States")
print("5: Display country with the most airports")
print("6: Specify list of cities with most ingoing / outgoing flights")
print("7: Find a trip that connects two specified cities")
print("8: Find a trip that connects two specified cities with less than X stops")
print("9: Find all cities reachable within specified number of stops from a city")
print("10: Run transitive connected component algorithm\n")


userChoice = input("Enter choice here: ")

queryOutput = switch(userChoice)