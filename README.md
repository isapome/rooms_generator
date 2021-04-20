# Rooms Generator

Given a database (i.e. _database.txt_) with rooms created in the past, generate partitions of the current participants, listed in a file named *YY_MM_DD.txt*, 
with Y,M, and D today's date. Otherwise the script will ask you which file it needs to use. You can specify any group the participants belong to, the script
will penalize putting people belonging to the same group together in a room. 

Requirements:

- python3
- more-itertools 8.7.0
- numpy          1.20.2
- pip            21.0.1
- setuptools     49.2.1
