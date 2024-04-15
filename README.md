# Airline Search Engine

Airline Search Engine is an airline search engine that can help users plan trips via air travel, providing possible routes and information about general flights.

CS 431/631 Project

Contributors: Alexander Ram, Mason Smith, Thomas Braun

University of Nevada, Reno - Computer Science and Engineering

Professor: Dr. Lei Yang

## Popular Features

- Explore available airports within a designated country.
- Discover the airlines operating within a specified country.
- Determine a travel route between two cities.
- Locate a direct route between two cities with minimal layovers.
- Obtain a list of cities easily accessible from another city by air.
- Identify airlines offering direct flights.
- Evaluate routes with the fewest layovers en route to your destination.

## Extra Features

- Check for airline codeshare agreements with other carriers.
- Calculate the total number of airports within a selected country.
- Investigate which cities are served by the greatest number of airlines.

## Requirements

Our software is currently designed for the Linux terminal (any distro should work), and requires at least Python 3.7 installed.

We use PostgreSQL as our relational database management system.

As our program is a command-line application, the hardware requirements are extremely minimal, and will not be listed here—hardly a device exists that couldn't run the search engine.

## Usage

Simply start up a terminal window and navigate to the installation folder.

Run the following command to start the program, assuming you have Python 3 installed:

```
python3 airlines.py
```

## Advanced

Our search engine can be used in scripts for other programs; run the following command for more details:

```
python3 airlines.py -h
```

## License

See LICENSE for details.
