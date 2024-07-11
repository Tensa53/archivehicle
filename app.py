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
manufacturers_col = db.manufacturer


@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 24
    start = (page - 1) * per_page
    end = start + per_page
    all_vehicles = list(vehicles_col.find())
    total_pages = math.ceil(len(all_vehicles) / per_page)
    vehicles = all_vehicles[start:end]
    return render_template('index.html', vehicles=vehicles, total_pages=total_pages, page=page)


def get_image_path_chassis(chassis):
    match chassis:
        case "Convertible":
            return "../static/img/vehicle_sample_convertible.png"
        case "Hatchback":
            return "../static/img/vehicle_sample_hatchback.png"
        case "Pickup Truck":
            return "../static/img/vehicle_sample_pickup-truck.png"
        case "Sedan":
            return "../static/img/vehicle_sample_sedan.png"
        case "Suv":
            return "../static/img/vehicle_sample_suv.png"
        case "Van":
            return "../static/img/vehicle_sample_van.png"


def get_mechanical_details_filled(form):
    engine = form['engineInput']
    cylinders = form['cylindersInput']
    fuel = form['fuelInput']
    mileage = form['mileageInput']
    transmission = form['transmissionInput']

    check = len(engine) != 0 or len(cylinders) != 0 or len(fuel) != 0 or len(mileage) != 0

    if check:
        mechanical_details = {"engine": engine, "cylinders": cylinders, "fuel": fuel, "mileage": mileage,
                              "transmission": transmission,
                              "drivetrain": form['drivetrainInput']}
        return mechanical_details
    else:
        return None


def get_body_details(form):
    trim = form['trimInput']
    doors = form['doorsInput']
    exterior = form['excolorInput']
    interior = form['incolorInput']

    check = len(trim) != 0 or len(exterior) != 0 or len(doors) != 0 or len(interior) != 0

    if check:
        body_details = {"trim": trim, "doors": doors, "exterior": exterior, "interior": interior}
        return body_details
    else:
        return None


@app.route('/insert_vehicle', methods=['GET', 'POST'])
def insert_vehicle():
    if request.method == 'POST':
        name = request.form['nameInput']
        model = request.form['modelInput']
        chassis = request.form['chassisInput']
        image = get_image_path_chassis(chassis)
        type = request.form['typeInput']
        year = request.form['yearInput']
        price = request.form['priceInput']
        manufacturer = request.form['manufacturerInput']
        description = request.form['descriptionInput']

        new_vehicle = {}
        mechanical_details = get_mechanical_details_filled(request.form)
        body_details = get_body_details(request.form)

        if body_details is None and mechanical_details is None:
            new_vehicle = {"name": name, "model": model, "chassis": chassis, "type": type, "year": year, "price": price,
                           "image": image,
                           "description": description,
                           "manufacturer_id": ObjectId(manufacturer)}
        elif body_details is not None and mechanical_details is None:
            new_vehicle = {"name": name, "model": model, "chassis": chassis, "type": type, "year": year, "price": price,
                           "image": image,
                           "description": description,
                           "manufacturer_id": ObjectId(manufacturer),
                           "body_details": body_details}
        elif body_details is None and mechanical_details is not None:
            new_vehicle = {"name": name, "model": model, "chassis": chassis, "type": type, "year": year, "price": price,
                           "image": image,
                           "description": description,
                           "manufacturer_id": ObjectId(manufacturer),
                           "mechanical_details": mechanical_details}
        else:
            new_vehicle = {"name": name, "model": model, "chassis": chassis, "type": type, "year": year, "price": price,
                           "image": image,
                           "description": description,
                           "manufacturer_id": ObjectId(manufacturer),
                           "mechanical_details": mechanical_details,
                           "body_details": body_details}

        vehicles_col.insert_one(new_vehicle)
        return render_template('insert_vehicle.html', message_success="Vehicle inserted successfully")

    return render_template('insert_vehicle.html', manufacturers=list(manufacturers_col.find()),
                           drivetrains = vehicles_col.distinct("mechanical_details.drivetrain", {}))


@app.route("/show_single_vehicle", methods=['GET', 'POST'])
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
