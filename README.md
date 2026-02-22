🚇 Paris Metro Graph – Neo4j & Python
Graph-based itinerary engine for the Paris metro network, built with Neo4j, Cypher, and Python.

🎯 Project Overview
This project models the Paris metro network as a graph database and implements an itinerary engine capable of finding the fastest route between any two geographic coordinates.
The graph captures three types of relationships:

🚇 Train links between stations on the same line
🔄 Correspondences between lines at the same station (4 min estimated)
🚶 Walking links between stations less than 1km apart (speed: 4 km/h)


📁 Repository Structure
├── build_graph.txt       # Cypher queries to build the Neo4j graph
├── data_exploration.txt  # Cypher queries for data exploration & analysis
├── itinerary.py          # Python + Cypher itinerary engine (Dijkstra)
└── README.md

🗃️ Data Sources
FileDescriptionstations.csvStation name, coordinates (x, y), traffic, city, lineliaisons.csvConnections between stations per line (bidirectional)
Source: RATP Open Data

🧱 Graph Model
Each station/line combination is represented as a unique node, allowing multi-line stations (e.g. Arts et Métiers on lines 3 & 11) to be modeled accurately.
Node: (:Station {nom, ligne, x, y, trafic, ville})
Relationships:

[:TRAIN {distance, duration}] – between consecutive stations on same line
[:CORRESPONDENCE {duration: 4}] – between lines at same station
[:WALK {distance, duration}] – between stations < 1km apart


🚀 Getting Started
Prerequisites

Docker with Neo4j container (as per course setup)
Python 3.x
neo4j Python library

bashpip install neo4j
1. Build the graph
Run the queries in build_graph.txt directly in the Neo4j console.
2. Explore the data
Run the queries in data_exploration.txt to answer analytical questions such as:

Number of correspondences per station
Stations within 2km of LA DEFENSE
Fastest route from LA DEFENSE to CHATEAU DE VINCENNES
Stations within 10 stops or 20 minutes of SAINT-LAZARE

3. Run the itinerary engine
bashpython itinerary.py --x1 652809 --y1 6863002 --x2 658000 --y2 6861000
Returns the optimal route with station names, lines, and total travel time.

⚙️ Algorithm
The itinerary engine uses Dijkstra's shortest path algorithm via Neo4j's native GDS library, called through Python using ephemeral start/end nodes for each query.

🛠️ Tech Stack

Neo4j – Graph database
Cypher – Query language
Python – API wrapper & argument handling
Docker – Containerized Neo4j environment


