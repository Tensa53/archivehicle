from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connection to mongodb
client = MongoClient('localhost', 27017)

# This is a mongodb database
db = client.archiVehicle

# This is a collection
vehicles_col = db.vehicle

@app.route('/', methods=['GET', 'POST'])
def index():
    vehicles_twenty = vehicles_col.find(limit=20)
    return render_template('index.html', vehicles=vehicles_twenty)


if __name__ == '__main__':
    app.run()
