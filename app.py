# Python SQL toolkit and Object Relational Mapper
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

# Flask routes
# List of all availble routes
@app.route("/")
def welcome():
    """List of all available routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Route for precipitation by date
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for precipitation by date"""
    # Create session
    session = Session(engine)

    # Query date and precipitation from Measurment key
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictonary and append results to prcp_data list
    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    # Return dictonary as json
    return jsonify(prcp_data)

# Route for all stations
@app.route("/api/v1.0/stations")
def stations():
    """Query for list of stations"""
     # Create session
    session = Session(engine)

    # Query date and precipitation from Measurment key
    stations = session.query(Station.station).all()
    session.close()

    # Create list of stations
    station_names = list(np.ravel(stations))
    return jsonify(station_names)



if __name__ == "__main__":
    app.run(debug=True)