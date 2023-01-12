import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct
from flask import Flask, jsonify 

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

#Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Note: to access values between a start and end date enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return a list of all daily precipitation totals for the last year"""
    
    start_date = '2016-08-23'
    sel = [measurement.date, 
        func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
            filter(measurement.date >= start_date).\
            group_by(measurement.date).\
            order_by(measurement.date).all()
   
    session.close()
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all the active Weather stations in Hawaii"""
    sel = [measurement.station]
    active_stations = session.query(*sel).\
        group_by(measurement.station).all()
    session.close()

    precipitaton_query_values = []
    for prcp, date in precipitation_query_results:
        precipitation_dict = {}
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"] = date
        precipitaton_query_values.append(precipitation_dict)

    return jsonify(precipitaton_query_values) 
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all the active Weather stations in Hawaii"""
    sel = [measurement.station]
    active_stations = session.query(*sel).\
        group_by(measurement.station).all()
    session.close()
    
    list_of_stations = list(np.ravel(active_stations)) 
    return jsonify(list_of_stations)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    start_date = '2016-08-23'
    sel = [measurement.date, 
        measurement.tobs]
    station_temps = session.query(*sel).\
            filter(measurement.date >= start_date, measurement.station == 'USC00519281').\
            group_by(measurement.date).\
            order_by(measurement.date).all()
    session.close()

    observation_dates = []
    temperature_observations = []

    for date, observation in station_temps:
        observation_dates.append(date)
        temperature_observations.append(observation)
    
    most_active_tobs_dict = dict(zip(observation_dates, temperature_observations))

    return jsonify(most_active_tobs_dict)
@app.route("/api/v1.0/<start_date>") 
def start_date(start):
    session = Session(engine) 

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""
    start_date_tobs_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close() 

    for min, avg, max in start_date_tobs_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min"] = min
        start_date_tobs_dict["average"] = avg
        start_date_tobs_dict["max"] = max
        start_date_tobs_values.append(start_date_tobs_dict)
    
    return jsonify(start_date_tobs_values)
@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    session = Session(engine)

    """Return a list of min, avg and max tobs between start and end dates entered"""
    start_end_date_tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
  
    start_end_tobs_date_values = []
    for min, avg, max in start_end_date_tobs_results:
        start_end_tobs_date_dict = {}
        start_end_tobs_date_dict["min_temp"] = min
        start_end_tobs_date_dict["avg_temp"] = avg
        start_end_tobs_date_dict["max_temp"] = max
        start_end_tobs_date_values.append(start_end_tobs_date_dict) 
    
    if start_end_tobs_date_values['Min']: 
        return jsonify(start_end_tobs_date_values)
    else:
        return jsonify({"error": f"Date(s) not found, invalid date range or dates not formatted correctly."}), 404
  

   
if __name__ == '__main__':
    app.run(debug=True) 