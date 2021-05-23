# importing dependencies
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# importing Flask
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Save calculation
year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Creating an app
app = Flask(__name__)

# Flask routes
@app.route("/")
def welcome():
    return (
        f"Welcome to my Hawaii weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
	session = Session(engine)

	year_data = session.query(measurement.date, measurement.prcp).\
	filter(measurement.date >= year_before).\
	filter(measurement.date <= dt.date(2017, 8, 23)).all()

	session.close()

	prcp_dict = {}
	for date, prcp in year_data:
		prcp_dict[date] = prcp

	return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
	session = Session(engine)

	stations = session.query(station.station).all()

	session.close()

	all_stations = list(np.ravel(stations))

	return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
	session = Session(engine)

	temp_data = session.query(measurement.date, measurement.tobs).\
	filter(measurement.date >= year_before).\
	filter(measurement.date <= dt.date(2017, 8, 23)).\
	filter(measurement.station == 'USC00519281').all()

	session.close()

	top_station = list(np.ravel(temp_data))

	return jsonify(top_station)

@app.route("/api/v1.0/<start>")


@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None, end = None):
	session = Session(engine)

	if not end:
		temp_data = session.query(measurement.station, func.min(measurement.tobs),\
                func.max(measurement.tobs), func.avg(measurement.tobs)).\
				filter(measurement.date >= start).\
				group_by(measurement.station).all()

		all_temps = list(np.ravel(temp_data))

		return jsonify(all_temps)
	# Fetch min, max, and avg temps for all dates greater than or equal to supplied date
	temp_data = session.query(measurement.station, func.min(measurement.tobs),\
                func.max(measurement.tobs), func.avg(measurement.tobs)).\
				filter(measurement.date >= start).\
				filter(measurement.date <= end).\
				group_by(measurement.station).all()

	session.close()

	all_temps = list(np.ravel(temp_data))

	print(temp_data)

	return jsonify(all_temps)

if __name__ == "__main__":
    app.run(debug=True)