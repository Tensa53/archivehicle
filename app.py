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


def get_manufacturer_stats(manufacturer):
    manufacturer_stats = {}

    # Convertible
    # Hatchback
    # Pickup Truck
    # SUV
    # Sedan
    # Van
    manufacturer_name = manufacturers_col.find_one({'_id': manufacturer}, {'name': 1})
    manufacturer_stats['name'] = manufacturer_name['name']

    vehicles_per_manufacturer = vehicles_col.count_documents({'manufacturer_id': manufacturer})
    manufacturer_stats['vehicles_per_manufacturer'] = vehicles_per_manufacturer

    convertible_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                               {'chassis': "Convertible"}]})
    manufacturer_stats['convertible_count'] = convertible_count

    convertible_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                               {'chassis': "Hatchback"}]})
    manufacturer_stats['hatchback_count'] = convertible_count

    pickup_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                          {'chassis': "Pickup Truck"}]})
    manufacturer_stats['pickup_count'] = pickup_count

    suv_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                       {'chassis': "SUV"}]})
    manufacturer_stats['suv_count'] = suv_count

    sedan_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                         {'chassis': "Sedan"}]})
    manufacturer_stats['sedan_count'] = sedan_count

    van_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                       {'chassis': "Van"}]})
    manufacturer_stats['van_count'] = van_count

    # 3
    # 4
    # 6
    # 8
    cylindersthree_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                        {'mechanical_details.cylinders': 3}]})
    manufacturer_stats['cylindersthree_count'] = cylindersthree_count

    cylindersfour_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                        {'mechanical_details.cylinders': 4}]})
    manufacturer_stats['cylindersfour_count'] = cylindersfour_count

    cylinderssix_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                      {'mechanical_details.cylinders': 6}]})
    manufacturer_stats['cylinderssix_count'] = cylinderssix_count

    cylinderseight_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                        {'mechanical_details.cylinders': 8}]})
    manufacturer_stats['cylinderseight_count'] = cylinderseight_count

    # Diesel
    # E85 Flex Fuel
    # Gasoline
    # Hybrid
    # PHEV Hybrid Fuel
    diesel_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                          {'mechanical_details.fuel': "Diesel"}]})
    manufacturer_stats['diesel_count'] = diesel_count

    flexfuel_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                            {'mechanical_details.fuel': "E85 Flex Fuel"}]})
    manufacturer_stats['flexfuel_count'] = flexfuel_count

    gasoline_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                            {'mechanical_details.fuel': "Gasoline"}]})
    manufacturer_stats['gasoline_count'] = gasoline_count

    hybrid_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                          {'mechanical_details.fuel': "Hybrid"}]})
    manufacturer_stats['hybrid_count'] = hybrid_count

    phev_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                        {'mechanical_details.fuel': "PHEV Hybrid Fuel"}]})
    manufacturer_stats['phev_count'] = phev_count

    # All - wheel Drive
    # Four - wheel Drive
    # Front - wheel Drive
    # Rear - wheel Drive

    allwheel_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                            {'mechanical_details.drivetrain': "All-wheel Drive"}]})
    manufacturer_stats['allwheel_count'] = allwheel_count

    fourwheel_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                             {'mechanical_details.drivetrain': "Four-wheel Drive"}]})
    manufacturer_stats['fourwheel_count'] = fourwheel_count

    frontwheel_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                             {'mechanical_details.drivetrain': "Front-wheel Drive"}]})
    manufacturer_stats['frontwheel_count'] = frontwheel_count

    rearwheel_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                             {'mechanical_details.drivetrain': "Rear-wheel Drive"}]})
    manufacturer_stats['rearwheel_count'] = rearwheel_count

    # 2
    # 3
    # 4
    twodoors_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                            {'body_details.doors': 2}]})
    manufacturer_stats['twodoors_count'] = twodoors_count

    threedoors_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                              {'body_details.doors': 3}]})
    manufacturer_stats['threedoors_count'] = threedoors_count

    fourdoors_count = vehicles_col.count_documents({'$and': [{'manufacturer_id': manufacturer},
                                                             {'body_details.doors': 4}]})
    manufacturer_stats['fourdoors_count'] = fourdoors_count

    return manufacturer_stats


def process_query():
    query_dict = {}
    query_list = []
    filter_list = {}

    vehicle_name = request.form['nameFilter']

    if vehicle_name != "":
        # filter_list['nameFilter'] = vehicle_name
        pat = re.compile(vehicle_name, re.IGNORECASE)
        query_list.append({'name': {'$regex': pat}})

    vehicle_year = request.form['yearFilter']
    if vehicle_year != "No Year Filter":
        # filter_list['yearFilter'] = vehicle_year
        query_list.append({'year': int(vehicle_year)})

    vehicle_price_above = request.form['priceAboveFilter']
    if vehicle_price_above != "":
        # filter_list['priceAboveFilter'] = vehicle_price_above
        query_list.append({"price": {"$gt": int(vehicle_price_above)}})

    vehicle_price_below = request.form['priceBelowFilter']
    if vehicle_price_below != "":
        # filter_list['priceBelowFilter'] = vehicle_price_below
        query_list.append({"price": {"$lt": int(vehicle_price_below)}})

    vehicle_cylinders = request.form['cylindersFilter']
    if vehicle_cylinders != "No Cylinders Filter":
        # filter_list['cylindersFilter'] = vehicle_cylinders
        query_list.append({'mechanical_details.cylinders': int(vehicle_cylinders)})

    vehicle_fuel = request.form['fuelFilter']
    if vehicle_fuel != "No Fuel Filter":
        # filter_list['fuelFilter'] = vehicle_fuel
        query_list.append({'mechanical_details.fuel': vehicle_fuel})

    vehicle_drivetrain = request.form['drivetrainFilter']
    if vehicle_drivetrain != "No Drivetrain Filter":
        # filter_list['drivetrainFilter'] = vehicle_drivetrain
        query_list.append({'mechanical_details.drivetrain': vehicle_drivetrain})

    vehicle_doors = request.form['doorsFilter']
    if vehicle_doors != "No Doors Filter":
        # filter_list['doorsFilter'] = vehicle_doors
        query_list.append({'body_details.doors': int(vehicle_doors)})

    vehicle_chassis = request.form['chassisFilter']
    if vehicle_chassis != "No Chassis Filter":
        # filter_list['chassisFilter'] = vehicle_chassis
        query_list.append({'chassis': vehicle_chassis})

    vehicle_manufacturer = request.form['manufacturerFilter']
    if vehicle_manufacturer != "No Manufacturer Filter":
        # filter_list['manufacturerFilter'] = vehicle_manufacturer
        query_list.append({'manufacturer_id': vehicle_manufacturer})

    query_dict["$and"] = query_list

    return query_dict



def get_mechanical_details(form):
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
        case "SUV":
            return "../static/img/vehicle_sample_suv.png"
        case "Van":
            return "../static/img/vehicle_sample_van.png"


def filter_parameters():
    year = vehicles_col.distinct("year", {})
    cylinders = vehicles_col.distinct("mechanical_details.cylinders", {})
    fuel = vehicles_col.distinct("mechanical_details.fuel", {})
    drivetrain = vehicles_col.distinct("mechanical_details.drivetrain", {})
    doors = vehicles_col.distinct("body_details.doors", {})
    chassis = vehicles_col.distinct("chassis", {})
    manufacturer = manufacturers_col.distinct("manufacturer", {})
    return chassis, cylinders, doors, drivetrain, fuel, manufacturer, year


def process_manufacturer_form():
    name = request.form['nameInput']
    country = request.form['countryInput']
    year = request.form['yearInput']
    founder = request.form['founderInput']
    description = request.form['descriptionInput']
    new_manufacturer = {"name": name, "country": country, "year": year, "founder": founder, "description": description}
    return new_manufacturer


@app.route('/', methods=['GET', 'POST'])
def index():
    chassis, cylinders, doors, drivetrain, fuel, manufacturer, year = filter_parameters()
    return render_template('index.html', year=year, cylinders=cylinders, fuel=fuel,
                           drivetrain=drivetrain, doors=doors, chassis=chassis, manufacturer=manufacturer)



@app.route('/manufacturers', methods=['GET', 'POST'])
def manufacturers():
    manufacturers = manufacturers_col.find()
    return render_template("manufacturers.html", manufacturers=manufacturers)


@app.route('/insert_manufacturer', methods=['GET', 'POST'])
def insert_manufacturer():
    if request.method == 'POST':
        new_manufacturer = process_manufacturer_form()
        manufacturers_col.insert_one(new_manufacturer)
        return render_template("insert_manufacturer.html",
                               message_success="Manufacturer inserted successfully")

    return render_template("insert_manufacturer.html")


@app.route('/update_manufacturer', methods=['POST'])
def update_manufacturer():
    print(request)
    input = request.form['updateBtn']

    if input == "Update Info":
        manufacturer_id = request.form['manufacturerId']
        manufacturer = manufacturers_col.find_one({'_id': ObjectId(manufacturer_id)})
        return render_template("update_manufacturer.html", manufacturer=manufacturer)
    elif input == "Save Update":
        manufacturer_id = request.form['manufacturerId']
        updated_manufacturer = process_manufacturer_form()
        manufacturers_col.update_one({"_id": ObjectId(manufacturer_id)}, {"$set": updated_manufacturer}, upsert=False)
        return render_template("update_manufacturer.html",
                               message_success="Manufacturer updated successfully")


@app.route('/delete_manufacturer', methods=['POST'])
def delete_manufacturer():
    manufacturer_id = request.form['manufacturerId']
    vehicles_by_manufacturer = vehicles_col.find_one({"manufacturer_id": ObjectId(manufacturer_id)})
    if len(vehicles_by_manufacturer) > 0:
        return render_template('manufacturers.html',
                               message_error="You cannot delete this manufacturer. "
                                             "There are still vehicles of this manufacturer")
    else:
        vehicles_col.delete_one({'_id': ObjectId(manufacturer_id)})
        return render_template('manufacturers.html', message_success="Manufacturer deleted successfully")


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


def process_vehicle_form():
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
    mechanical_details = get_mechanical_details(request.form)
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
    return new_vehicle


@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    page = request.args.get('page', default=1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    all_vehicles = list(vehicles_col.find())
    total_pages = math.ceil(len(all_vehicles) / per_page)
    vehicles = all_vehicles[start:end]
    return render_template('vehicles.html', vehicles=vehicles, total_pages=total_pages, page=page)


@app.route('/insert_vehicle', methods=['GET', 'POST'])
def insert_vehicle():
    if request.method == 'POST':
        new_vehicle = process_vehicle_form()

        vehicles_col.insert_one(new_vehicle)
        return render_template('insert_vehicle.html', message_success="Vehicle inserted successfully")

    return render_template('insert_vehicle.html', manufacturers=list(manufacturers_col.find()),
                           drivetrains=vehicles_col.distinct("mechanical_details.drivetrain", {}),
                           all_chassis=vehicles_col.distinct("chassis", {}))


@app.route("/show_single_vehicle", methods=['GET', 'POST'])
def show_single_vehicle():
    vehicle_id = request.form['vehicle_id']
    vehicle = vehicles_col.find_one({'_id': ObjectId(vehicle_id)})
    manufacturer = manufacturers_col.find_one({'_id': vehicle['manufacturer_id']})
    return render_template('show_vehicle.html', vehicle=vehicle, manufacturer=manufacturer)


@app.route("/search_a_vehicle", methods=['POST'])
def search_a_vehicle():
    chassis, cylinders, doors, drivetrain, fuel, manufacturer, year = filter_parameters()

    query = process_query()

    if len(query['$and']) == 1:
        return redirect("/")

    vehicles_found = list(vehicles_col.find(query))
    if len(vehicles_found) > 0:
        return render_template('index.html', year=year, cylinders=cylinders, fuel=fuel,
                               drivetrain=drivetrain, doors=doors, chassis=chassis, manufacturer=manufacturer,
                               vehicles=vehicles_found)
    else:
        return render_template('index.html', year=year, cylinders=cylinders, fuel=fuel,
                               drivetrain=drivetrain, doors=doors, chassis=chassis, manufacturer=manufacturer,
                               empty_message="No Vehicles Found")


@app.route("/update_vehicle", methods=['POST'])
def update_vehicle():
    input = request.form['updateBtn']

    if input == "Update Info":
        vehicle_id = request.form['vehicleId']
        vehicle = vehicles_col.find_one({'_id': ObjectId(vehicle_id)})
        return render_template('update_vehicle.html', vehicle=vehicle,
                               manufacturers=list(manufacturers_col.find()),
                               drivetrains=vehicles_col.distinct("mechanical_details.drivetrain", {}),
                               all_chassis=vehicles_col.distinct("chassis", {}))
    elif input == "Save Update":
        vehicle_id = request.form['vehicleId']
        updated_vehicle = process_vehicle_form()
        vehicles_col.update_one({"_id": ObjectId(vehicle_id)}, {"$set": updated_vehicle}, upsert=False)
        return render_template('update_vehicle.html', message_success="Vehicle updated successfully")


@app.route("/delete_vehicle", methods=['POST'])
def delete_vehicle():
    vehicle_id = request.form['vehicleId']
    vehicles_col.delete_one({'_id': ObjectId(vehicle_id)})
    return render_template('show_vehicle.html', message_success="Vehicle deleted successfully")


@app.route("/stats", methods=['GET', 'POST'])
def stats():
    manufacturers_id = manufacturers_col.distinct("_id", {})
    manufacturer_stats = {}

    for manufacturer in manufacturers_id:
        manufacturer_stats[manufacturer] = get_manufacturer_stats(manufacturer)

    manufacturer_stats_list = list(manufacturer_stats.values())

    return render_template("stats.html", manufacturer_stats=manufacturer_stats_list)


if __name__ == '__main__':
    app.run(debug=True)
