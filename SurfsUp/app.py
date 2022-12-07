# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

# Create Flask setup
app = Flask(__name__)

# Start at homepage and list all available routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br>"
        f"Availble Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start/<start><br>"
        f"/api/v1.0/start_end/<start>/<end>"
    )
# Precipitation Route - Converts results from analysis to dictionary and returns as JSON response
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link from Python to DB
    session = Session(engine)

    # Query results from precipitation analysis
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date>="2016-08-23").all()

    # Close session
    session.close()

    # Create dictionary from row data to return JSON response
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

# Stations Route - Returns JSON response of stations
@app.route("/api/v1.0/stations")
def stations():
    # Create session link from Python to DB
    session = Session(engine)

    # Query all stations
    results = session.query(station.station, station.name).all()

    # Close session
    session.close()

    # Create list and return JSON response
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


# Tobs Route - Queries dates and temp observations of the most-active station for the previous year, and returns a JSON response
@app.route("/api/v1.0/tobs")
def tobs():
    # Create session link from Python to DB
    session = Session(engine)

    # Query dates and temp observations of most-active station for previous year
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date>="2016-08-23").all()

    # Close session
    session.close()

    # Create list and return JSON response
    most_active = list(np.ravel(results))

    return jsonify(most_active)


# Start and End Routes - Returns JSON resposne of min temp, max temp, and avg temp for a specified start or start-end range
@app.route("/api/v1.0/start/<start>")
@app.route("/api/v1.0/start_end/<start>/<end>")
def start_end(start, end = "2017-08-23"):
    # Create session link from Python to DB
    session = Session(engine)

    # Query min temp, avg temp, and max temp for specified start or start-end range
    results = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
        filter(measurement.date >=start).filter(measurement.date <= end).all()

    # Close session
    session.close()

    # Create list and return JSON response
    start_result = list(np.ravel(results))

    return jsonify(start_result)

if __name__ == '__main__':
    app.run(debug=True)