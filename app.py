
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<br/>Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Fetching the date and precipitation data and loading into dictionary """

    # Fetching most recent date
    date_now = session.query(func.max(Measurement.date)).first()[0]

    # Calculate the date 1 year ago from the last date in the database
    #year = int(date_now[0:4])
    #onth = int(date_now[5:7])
    #day = int(date_now[8:])
    #one_year_ago_date = dt.date(year, month, day)- dt.timedelta(days=365)
    one_year_ago_date = '2016-08-23'

    # Perform a query to retrieve the data and precipitation scores
    last_12_months_prcp_record = session.query(Measurement.date, Measurement.prcp).\
                                filter(Measurement.date >= one_year_ago_date).\
                                filter(Measurement.date <= date_now).all()

    session.close()

    # Save the query results into a dictionary

    prcp_dict = {}
    for dt, prc in last_12_months_prcp_record:
        prcp_dict[dt] = prc

    # JSON representation of dictionary
    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Fetching the stations data and loading into dictionary """

    stations = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(stations))

    session.close()

    return jsonify(stations_list)




@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Fetching the temperature data """
    # Design a query to find the temperature of last year

    date_now = session.query(func.max(Measurement.date)).first()[0]

    # Calculate the date 1 year ago from the last date in the database
    #year = int(date_now[0:4])
    #onth = int(date_now[5:7])
    #day = int(date_now[8:])
    #one_year_ago_date = dt.date(year, month, day)- dt.timedelta(days=365)
    one_year_ago_date = '2016-08-23'

    # Perform a query to retrieve the data and precipitation scores
    last_12_months_prcp_record = session.query(Measurement.date, Measurement.tobs).\
                                filter(Measurement.date >= one_year_ago_date).\
                                filter(Measurement.date <= date_now).all()

    session.close()

    # Save the query results into a dictionary

    temp_dict = {}
    for dt, temp in last_12_months_prcp_record:
        temp_dict[dt] = temp

    # JSON representation of dictionary
    return jsonify(temp_dict)



@app.route("/api/v1.0/<start_date>")
def temp_start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Fetching the temperature data from start date"""
    # Calculate the lowest temperature recorded, highest temperature recorded, and average temperature

    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).first()[0]
    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).first()[0]
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).first()[0]

    session.close()

    # Creating a dictionary to hold min, max and avg temperature values
    temp_dict = {}
    temp_dict['TMIN'] = lowest_temp
    temp_dict['TMAX'] = highest_temp
    temp_dict['TAVG'] = avg_temp

    # JSON representation of dictionary
    return jsonify(temp_dict)




@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Fetching the temperature data between start date and end date"""
    # Calculate the lowest temperature recorded, highest temperature recorded, and average temperature

    lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).first()[0]
    highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).first()[0]
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).first()[0]

    session.close()

    # Creating a dictionary to hold min, max and avg temperature values
    temp_dict = {}
    temp_dict['TMIN'] = lowest_temp
    temp_dict['TMAX'] = highest_temp
    temp_dict['TAVG'] = avg_temp

    # JSON representation of dictionary
    return jsonify(temp_dict)




if __name__ == '__main__':
    app.run(debug=True)
