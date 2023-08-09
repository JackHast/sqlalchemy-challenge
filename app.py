import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflecting database into a new model
Base = automap_base()
# reflecting the tables
Base.prepare(engine,reflect=True)
# Saving references to tables
measurement = Base.classes.measurement
station = Base.classes.station
# Creating session
session = Session(engine)


#Flask setup
app = Flask(__name__)

#Flask routes

#home route
@app.route("/")
def homepage():
    #returning information about routes on homepage
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"You can also access the min, max and mean temperature<br/>"
        f"for any period between 2010-01-01 and 2017-08-23.<br/>"
        f"For example the route /api/v1.0/2013-01-01<br/>"
        f"will provide a jsonified dictionary with the min,<br/>"
        f"max and mean temperatures between 2013-01-01 and<br/>"
        f"2017-08-23.<br/>"
        f"Likewise, /api/v1.0/2013-01-01/2016-01-01<br/>"
        f"will give the same between 2013-01-01 and 2016-01-01 "


    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #opening session
    session = Session(engine)
    #finding rows for last year
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365) 
    precipitation = session.query(measurement.date,measurement.prcp).filter(measurement.date >=year_ago)      
    #converting query to pd dataframe, setting index to date and converting to dictionary                                                     
    precipitation_df = pd.DataFrame(precipitation,columns=['Date','Precipitation'])
    precipitation_df.set_index('Date', inplace=True)
    precipitation_dict = precipitation_df.to_dict()
    #closing session and returning jsonified dictionary
    session.close()
    return (jsonify(precipitation_dict))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #querying stations
    station_list = session.query(station.station).all()
    #removing station names for tuples
    station_list = list(np.ravel(station_list))
    session.close()
    #returning jsonified list
    return (jsonify(station_list))

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #querying measurement db to find the number of measurements from each station
    station_count = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station)\
        .order_by(func.count(measurement.station).desc()).all()
    #most active station in first tuple of query since arranged in descending order
    most_active_station = station_count[0][0]
    #finding rows of measurement db from most active station from last year
    most_active_station_tobs = session.query(measurement.date,measurement.tobs).filter(measurement.station==most_active_station)\
        .filter(measurement.date >=year_ago).all()
    #converting response to dictionary
    most_active_station_tobs_df = pd.DataFrame(most_active_station_tobs)
    most_active_station_tobs_df.set_index('date', inplace=True)
    most_active_station_tobs_df = most_active_station_tobs_df.to_dict()
    session.close()
    #returning jsonified dictionary 
    return (jsonify(most_active_station_tobs_df['tobs']))

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    #Finding rows with starting date 'start'
    temp_stats = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
        .filter(measurement.date>=start).all()
    #removing elements from tuples and storing data in dictionary 'temp_stats_dict
    temp_stats_list = list(np.ravel(temp_stats))
    temp_stats_dict = {}
    temp_stats_dict['min_temp'] = temp_stats_list[0]
    temp_stats_dict['max_temp'] = temp_stats_list[1]
    temp_stats_dict['mean_temp'] = temp_stats_list[2]
    session.close()
    #returning jsonified dictionary
    return (jsonify(temp_stats_dict))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    #returning rows for dates between 'start' and 'end'
    temp_stats = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
        .filter(measurement.date>=start).filter(measurement.date<=end).all()
    #removing data from tuples and creating dictionary
    temp_stats_list = list(np.ravel(temp_stats))
    temp_stats_dict = {}
    temp_stats_dict['min_temp'] = temp_stats_list[0]
    temp_stats_dict['max_temp'] = temp_stats_list[1]
    temp_stats_dict['mean_temp'] = temp_stats_list[2]
    session.close()
    #returning jsonified dictionary
    return (jsonify(temp_stats_dict))


if __name__ == '__main__':
    app.run(debug=True)


