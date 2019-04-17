import numpy as np

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
	# Query all measurements
	results = session.query(Measurement.date, Measurement.prcp).all()

	# Create a dictionary from the row data and append 
	measurement_dict = {}
	for result in results:
		date = result[0]
		prcp = result[1]
		measurement_dict[date] = prcp

	return jsonify(measurement_dict)

@app.route("/api/v1.0/stations")
def stations():
	results = session.query(Measurement.station).all()

	return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)


