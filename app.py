from flask import Flask, jsonify

# Flask Setup
app = Flask(__name__)

# Def Home
@app.route("/")
def home():
    return (
        f"Welcome to the Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#Import MatplotLib 

import numpy as np
import pandas as pd
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine,reflect=True)
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

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
    precipitation_df=prcp_date_df.set_index("Date")
    precipitation = precipitation_df.to_dict()
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    #active_stations = session.query(Measurement.station).group_by(Measurement.station).count()
    from operator import itemgetter 
    list_stations = session.query(Measurement.station).group_by(Measurement.station).all()
    return jsonify(list_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    list_temp=[]
    for row in session.query(Measurement.tobs, Measurement.date).filter(Measurement.station=="USC00519281").filter(Measurement.date>="2016-08-23").all():
        (tobs,date) = row
        list_temp.append(tobs)
        list_tempdate.append(date)
    return jsonify(list_temp)

from markupsafe import escape

@app.route("/api/v1.0/<start>")
def start_date(start):

    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=str(start)).all()
    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>=str(start)).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=str(start)).all()
    return(
        f"The lowest temperature observation data (TOBS) on {escape(start)} was {(escape(lowest_temp[0]))}<br>"
        f"The highest temperature observation data (TOBS) on {escape(start)} was {(escape(highest_temp[0]))}<br>"
        f"The average temperature observation data (TOBS) on {escape(start)} was {(escape(avg_temp[0]))}<br>"
        )
    #return(f"Date {start} not found.")


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=str(start)).filter(Measurement.date<=str(end)).all()
    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>=str(start)).filter(Measurement.date<=str(end)).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=str(start)).filter(Measurement.date<=str(end)).all()

    return(
        f"The lowest temperature observation data (TOBS) between {escape(start)} and {escape(end)} was {(escape(lowest_temp[0]))}<br>"
        f"The highest temperature observation data (TOBS) on {escape(start)} and {escape(end)} was {(escape(highest_temp[0]))}<br>"
        f"The average temperature observation data (TOBS) on {escape(start)} and {escape(end)} was {(escape(avg_temp[0]))}<br>"
        )
    #Calculate the average temperature recorded
    #
    #lowest_temp
    #return print(f" {lowest_temp}")

if __name__ == "__main__":
    app.run(debug=True)