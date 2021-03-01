# Python SQL toolkit and Object Relational Mapper
import numpy as np
import datetime as dt
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
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
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

# Route for dates and temps for most active station
@app.route("/api/v1.0/tobs")
def activestation():
    """Query for most acitve station within previous 12 months"""
     # Create session
    session = Session(engine)

    # Query date and temp of most active station over the last 12 months
    station_freq = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    max_obv = station_freq[0]
    station_final_date = session.query(Measurement.date).filter(Measurement.station == max_obv[0]).\
        order_by(Measurement.date.desc()).first()

    # Convert date from string
    station_final_date = dt.datetime.strptime(station_final_date[0],"%Y-%m-%d").date()

    # Calculate the date one year from the last date of filtered data
    station_oneyear = station_final_date - dt.timedelta(days=365)

    # Create query for highest observation station temps over 12 months
    station_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == max_obv[0]).\
        filter(Measurement.date >= station_oneyear).\
        order_by(Measurement.date.asc()).all()
    
    # Close session
    session.close()

    # Create dictonary and append results to temps and dates list
    temps_and_dates = []
    for date, tobs in station_data:
        t_d_dict = {}
        t_d_dict["date"] = date
        t_d_dict["tobs"] = tobs
        temps_and_dates.append(t_d_dict)

    # Return as json
    return jsonify(temps_and_dates)

# Route for start date
@app.route("/api/v1.0/<start>")
def start(start):
    # Create session
    session = Session(engine)

    # Query date and precipitation from Measurment key
    sum_temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.station >= start).all()
    session.close()
    




if __name__ == "__main__":
    app.run(debug=True)