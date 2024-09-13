# ArchiVehicle

ArchiVehicle is a project realized for the Database II class. The goal of this project is to digitalize and simplify
the information management about a vehicle park, through a graphical user interface served by a client/server 
web application. ArchiVehicle offers the following functionalities:
1. Insert, update, delete the information about a vehicle;
2. Insert, update, delete the information about a manufacturer of vehicles;
3. Searching for a vehicle by applying some filters;
4. Quick view of the number of vehicles by each manufacturer, based on various characteristics by vehicle.

## Install ArchiVehicle

In order to install and use ArchiVehicle you need to follow the steps:
1. Import through MongoDB Compass these collections of documents:
   > archiVehicle.manufacturer.json <br>
     archiVehicle.vehicle.json
2. Change the current directory to the root of the project;
3. Create a virtual environment with the command:
   > python -m venv .venv
4. Activate the virtual environment;
5. Install the needed dependencies with the command:
   > pip install flask pymongo
6. Execute the flask server with the command:
   > flask run