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
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
	"""Return a dictionary using `date` as the key and `prcp` as the value."""
	
	results = session.query(Measurement.date, Measurement.prcp).all()

	# this query actually overwrites the data and only returns one year. 
	# but per conversation with Jason (TA), it is acceptable

	measurement_dict = {}
	for result in results:
		date = result[0]
		prcp = result[1]
		measurement_dict[date] = [prcp]

	return jsonify(measurement_dict)

@app.route("/api/v1.0/stations")
def stations():

	""" return a JSON list all stations"""

	results = session.query(Measurement.station).distinct().all()

	return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():

	""" returns a year's worth of temperature observations 
	(from the last data point) for each station """

	max_date = session.query(func.max(Measurement.date)).scalar()
	year, month, day = max_date.split("-")
	m_date = dt.date(int(year), int(month), int(day))
	query_date = m_date - dt.timedelta(days=365)
	data = session.query(Measurement.date,Measurement.tobs,Measurement.station).\
		filter(Measurement.date >= query_date).all()

	return jsonify(data)

@app.route("/api/v1.0/<start1>")
def startx(start1):

	""" returns a list with the cumulative max, min and avg temperature 
	of all dates in the dataset after date entered """

	startx = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start1).all()

	return jsonify(startx)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

	""" returns a list with the cumulative max, min and avg temperature 
	of all dates in between the dataset after dates entered """

	startend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

	return jsonify(startend)




if __name__ == '__main__':
    app.run(debug=True)
















