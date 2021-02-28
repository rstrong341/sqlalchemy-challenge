#################################################
# Import tools
#################################################
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
 
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

 
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)
 
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
 
#Open session
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
 
 
#################################################
# Flask Routes
#################################################

#Create App route
@app.route("/")
def welcome():
    """Here are all available api routes."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

#Create App route
#Set prev_yar variable to equal 12 months ago
#Grab the date and corresponding precipitation level from the Measurement data
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= twelve_months).all()
    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
           
    stations = list(np.ravel(results))
    return jsonify(stations)
#Create App route
#Query all stations
#Filter for the station
#Filter for previous year
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def temp_monthly():
    twelve_months = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= twelve_months).all()

    temps = list(np.ravel(results))

    return jsonify(temps)

#Create App routes
#Select the min average and max
#If there is no end date then show min avg and max
#If there are both start and end dates then show the min avg and max between those dates

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
           
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run()
    
    
    

