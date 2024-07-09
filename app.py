import math

from bson import ObjectId
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import re

app = Flask(__name__)

# Connection to mongodb
client = MongoClient('localhost', 27017)

# This is a mongodb database
db = client.archiVehicle

# This is a collection
vehicles_col = db.vehicle
all_vehicles = list(vehicles_col.find())
manufacturers_col = db.manufacturer


@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 24
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = math.ceil(len(all_vehicles) / per_page)
    vehicles = all_vehicles[start:end]
    return render_template('index.html', vehicles=vehicles, total_pages=total_pages, page=page)


@app.route("/show_single_vehicle", methods=['POST'])
def show_single_vehicle():
    vehicle_id = request.form['vehicle_id']
    vehicle = vehicles_col.find_one({'_id': ObjectId(vehicle_id)})
    manufacturer = manufacturers_col.find_one({'_id': vehicle['manufacturer_id']})
    return render_template('vehicle.html', vehicle=vehicle, manufacturer=manufacturer)

@app.route("/search_a_vehicle", methods=['POST'])
def search_a_vehicle():
    vehicle_name = request.form['vehicleSearch']
    pat = re.compile(vehicle_name, re.IGNORECASE)
    vehicles_found = vehicles_col.find({ "name": {'$regex': pat}})
    return render_template('index.html', vehicles=vehicles_found)

if __name__ == '__main__':
    app.run(debug=True)
