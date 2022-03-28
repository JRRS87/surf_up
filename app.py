import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



# Import the Flask Dependency
from flask import Flask, jsonify


#Set Up the Database

engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes.

Base = automap_base()

#Add the following code to reflect the database:

Base.prepare(engine, reflect=True)

#We'll create a variable for each of the classes so that we can reference them later, as shown below.

Measurement = Base.classes.measurement
Station = Base.classes.station


#Finally, create a session link from Python to our database with the following code:

session = Session(engine)


#Create a New Flask App Instance

app = Flask(__name__)

#We can define the welcome route using the code below:

@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#To create the route, add the following code. Make sure that it's aligned all the way to the left.

@app.route("/api/v1.0/precipitation")

#Next, we will create the precipitation() function.

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#For this route we'll simply return a list of all the stations.

@app.route("/api/v1.0/stations")

#we'll create a new function called stations()

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#For this route, the goal is to return the temperature observations for the previous year.

@app.route("/api/v1.0/tobs")

#Next, create a function called temp_monthly()

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Our last route will be to report on the minimum, average, and maximum temperatures.
#However, this route is different from the previous ones in that we will have to provide both a starting and ending date.

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Next, create a function called stats()

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