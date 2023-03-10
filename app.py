# Import things
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={
    'check_same_thread': False})
# Reflect database into new model
Base = automap_base()
# Reflect tables
Base.prepare(autoload_with=engine)
# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Route Setup
#################################################
# Home page
@app.route("/")
def home():
    return (
        "Welcome to the home page!<br/>"
        "<br/>"
        "Available Routes:<br/>"
        "<br/>"
        "/api/v1.0/precipitation<br/>"
        "This returns date and precipitation data for the last year\
            in the database.<br/>"
        "<br/>"
        "/api/v1.0/stations<br/>"
        "This returns a list of all the stations from the database.<br/>"
        "<br/>"
        "/api/v1.0/tobs<br/>"
        "This returns date and temperature data for the last year\
            in the database.<br/>"
        "<br/>"
        "/api/v1.0/<start><br/>"
        "This dynamic function will show the minimum, maximum, and average\
            temperatures AFTER the date specified.<br/>"
        "To use this option, you must enter a start date\
            in the format:<br/>"
        "/api/v1.0/YYYY-MM-DD/<br/>"
        "<br/>"
        "/api/v1.0/<start>/<end><br/>"
        "This dynamic function will show the minimum, maximum, and average\
            temperatures BETWEEN the dates specified.<br/>"
        "To use this option, you must enter a start (first date)\
            and end date (second date) in the format:<br/>"
        "/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
        )


# Precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Code below is copied from the .ipynb file
    # Calculate the date one year from the last date in data set.
    one_year_past = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation scores
    precip_all = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= one_year_past).all()
    # Close session
    session.close()
    # Convert list of tuples into normal list
    precip_list = list(np.ravel(precip_all))
    # Convert list into dictionary like the assignment asks
    precip_api = dict(zip(precip_list[0::2], precip_list[1::2]))
    # Return JSON representation of dictionary
    return jsonify(precip_api)
    # All dates and precipitation values are from the last year - success!


# Stations page
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Code below is copied from the .ipynb file
    station_list = session.query(Station.station).all()
    # Close session
    session.close()
    # Convert list of tuples into normal list
    station_api = list(np.ravel(station_list))
    # Return JSON representation of dictionary
    return jsonify(station_api)
    # All nine stations are listed - success!


# Temperature page
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date one year from the last date in data set.
    one_year_past = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and TEMPERATURE scores
    temp_all = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= one_year_past,
        Measurement.station == "USC00519281").all()
    # Close session
    session.close()
    # Convert list of tuples into normal list
    tobs_api = list(np.ravel(temp_all))
    # Return JSON representation of dictionary
    return jsonify(tobs_api)
    # Observations from USC00519281 are listed from last year - success!


# Dynamic page (just the start)
# <start> is YYYY-MM-DD
@app.route("/api/v1.0/<start>/")
def dynamic_alpha(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Print both values that the user entered into the url
    print(start)
    # List of functions to use in query
    function_list_alpha = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
        ]
    dynamic_data_alpha = session.query(*function_list_alpha).filter(
        (Measurement.date >= start)).all()
    # Close session
    session.close()
    # Convert list of tuples into normal list
    dynamic_api_alpha = list(np.ravel(dynamic_data_alpha))
    # Show off the results
    return jsonify(dynamic_api_alpha)
    # Min, max, and avg temperatures show for the selected dates - success!


# Dynamic page (start/end)
# <start>, <end> are YYYY-MM-DD
@app.route("/api/v1.0/<start>/<end>")
def dynamic(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Print both values that the user entered into the url
    print(start, end)
    # List of functions to use in query
    function_list = [
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
        ]
    dynamic_data = session.query(*function_list).filter(
        (Measurement.date >= start) & (Measurement.date <= end)
        ).all()
    # Close session
    session.close()
    # Convert list of tuples into normal list
    dynamic_api = list(np.ravel(dynamic_data))
    # Show off the results
    return jsonify(dynamic_api)
    # Min, max, and avg temperatures show for the selected dates - success!


#################################################
# This goes at the end and does something important
#################################################
if __name__ == "__main__":
    app.run(debug=True)
