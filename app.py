from flask import Flask, jsonify

# Flask Setup
app = Flask(__name__)

# Def Home. Provide welcome message and available routes
@app.route("/")
def home():
    return (
        f"Welcome to the Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"To find the minimum temperature, the average temperature, and the max temperature for a given start date, write the start date after v1.0/<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"To find the minimum temperature, the average temperature, and the max temperature between two dates, write the start after v1.0/ and the end date after that<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )

#Import dependencies 

import numpy as np
import pandas as pd
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Create engine to Hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})

#Reflection using automap
Base = automap_base()
Base.prepare(engine,reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Start session
session = Session(engine)

#Return the jsonified precipitation data for the last year in the database with the date as the key and the value as the precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Return the precipitation data per date in json
    list_prcp=[]
    list_date=[]
    for row in session.query(Measurement.prcp, Measurement.date).filter(Measurement.date>="2016-08-23").all():
        (prcp,date) = row
        list_prcp.append(prcp)
        list_date.append(date)
    prcp_date_df=pd.DataFrame({"Date":list_date,"Precipitation":list_prcp})
    #Set date as index 
    precipitation_df=prcp_date_df.set_index("Date")
    #Convert dataframe to dictionary
    precipitation = precipitation_df.to_dict()
    #Jsonify
    #Return the jsonified precipitation data for the last year in the database
    return jsonify(precipitation)

#Returns jsonified data of all the stations in the data base
@app.route("/api/v1.0/stations")
def stations():
    #import itemgetter
    from operator import itemgetter 
    #query to get activity per station
    list_stations = session.query(Measurement.station).group_by(Measurement.station).all()
    #jsonify list of stations
    return jsonify(list_stations)

#Returns jsonified data for the most active station (USC00519281) for the last year 
@app.route("/api/v1.0/tobs")
def tobs():
    #create empty list of temperatures for the most active station
    list_temp=[]
    #query to get tthe activity of the last 12 months for a particular station
    for row in session.query(Measurement.tobs, Measurement.date).filter(Measurement.station=="USC00519281").filter(Measurement.date>="2016-08-23").all():
        (tobs,date) = row
        list_temp.append(tobs)
    #jsonify list of temperatures
    return jsonify(list_temp)

#import dependency escape
from markupsafe import escape

#Start date as a parameter in the url
@app.route("/api/v1.0/<start>")
def start_date(start):
    #filter by variable start
    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=str(start)).all()
    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>=str(start)).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=str(start)).all()
    return(
        f"The lowest temperature observation data (TOBS) on {escape(start)} was {(escape(lowest_temp[0]))}<br>"
        f"The highest temperature observation data (TOBS) on {escape(start)} was {(escape(highest_temp[0]))}<br>"
        f"The average temperature observation data (TOBS) on {escape(start)} was {(escape(avg_temp[0]))}<br>"
        )

#Start date and end date as a parameter in the url
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    #filter by variables start and end
    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=str(start)).filter(Measurement.date<=str(end)).all()
    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>=str(start)).filter(Measurement.date<=str(end)).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=str(start)).filter(Measurement.date<=str(end)).all()

    return(
        f"The lowest temperature observation data (TOBS) between {escape(start)} and {escape(end)} was {(escape(lowest_temp[0]))}<br>"
        f"The highest temperature observation data (TOBS) on {escape(start)} and {escape(end)} was {(escape(highest_temp[0]))}<br>"
        f"The average temperature observation data (TOBS) on {escape(start)} and {escape(end)} was {(escape(avg_temp[0]))}<br>"
        )

if __name__ == "__main__":
    app.run(debug=True)