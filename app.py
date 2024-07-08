from bson import ObjectId
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connection to mongodb
client = MongoClient('localhost', 27017)

# This is a mongodb database
db = client.archiVehicle

# This is a collection
vehicles_col = db.vehicle
manufacturers_col = db.manufacturer


@app.route('/', methods=['GET', 'POST'])
def index():
    vehicles_twenty = vehicles_col.find(limit=20)
    return render_template('index.html', vehicles=vehicles_twenty)


@app.route("/show_single_vehicle", methods=['POST'])
def show_single_vehicle():
    vehicle_id = request.form['vehicle_id']
    vehicle = vehicles_col.find_one({'_id': ObjectId(vehicle_id)})
    manufacturer = manufacturers_col.find_one({'_id': vehicle['manufacturer_id']})
    return render_template('vehicle.html', vehicle=vehicle, manufacturer=manufacturer)


if __name__ == '__main__':
    app.run()
