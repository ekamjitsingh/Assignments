import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np

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


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return (
        f"<strong/>Here are all the Routes:</strong> <br/>"
        f"<br/><strong/>All Precipitation data:</strong> /api/v1.0/precipitation<br/>"
        f"<br/><strong/>List of stations:</strong>  /api/v1.0/stations<br/>"
        f"<br/><strong/>Temperature data for the last year of available data:</strong>  /api/v1.0/tobs<br/>"
        f"<br/><strong/>Daily minimum temperature, average temperature, and max temperature from a given start date (2017-MM-DD) to the last date in the dataset:</strong>  /api/v1.0/<start1><br/>"
        f"<br><strong/>Daily minimum temperature, average temperature, and max temperature between two dates(2017-MM-DD):</strong>  /api/v1.0/<start2>/<stop>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    query = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).first()
    ql=query[0]
    hurr = dt.datetime.strptime(ql, '%Y-%m-%d')
    date12mosago = hurr-dt.timedelta(days=366) 
    # Query last 12 months of preciptation data
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= date12mosago).order_by(Measurement.date.asc()).all()
    # Close our session (link) from Python to the DB
    session.close()
    return jsonify({k:v for k,v in results})

@app.route("/api/v1.0/stations")
def stations():
    # Returns a JSON list of station from the dataset
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results1 = session.query(Station.station).all()
    results = list(np.ravel(results1))
    # Close our session (link) from Python to the DB
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    query = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).first()
    ql=query[0]
    hurr = dt.datetime.strptime(ql, '%Y-%m-%d')
    date12mosago = hurr-dt.timedelta(days=366) 
    # Query last 12 months of temperature data
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= date12mosago).order_by(Measurement.date.asc()).all()
    # Close our session (link) from Python to the DB
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/<start1>")
def onedate(start1):
    session=Session(engine)
    # nested function originally available on Jupyter notebook
    def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    # calculate the daily normals for your trip
    # push each tuple of calculations into a list called `normals`
    normals=[]
    dates=[]
    dates_with_years=[]
    # last date in the database
    query = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).first()
    ql=query[0]
    last_date = dt.datetime.strptime(ql, '%Y-%m-%d')
    # start date is the one passed by the user
    # end date is the last date in the data base
    date1 = start1
    date2 = last_date
    start = dt.datetime.strptime(date1, '%Y-%m-%d')
    end = dt.datetime.strptime(date2, '%Y-%m-%d')
    step = dt.timedelta(days=1)
    # Stip off the year and save a list of %m-%d strings
    while start <= end:
        date_year=str(start.date())
        date_noyear=date_year.replace('2017-', '')
        dates.append(date_noyear)
        dates_with_years.append(date_year)
        start += step
    # Loop through the list of %m-%d strings and calculate the normals for each date
    for date in dates:
        normals.append(daily_normals(date)[0])
    session.close()

    return jsonify(normals)

@app.route("/api/v1.0/<start2>/<stop>")

def twodate(start2,stop):
    session=Session(engine)
    # nested function originally available on Jupyter notebook
    def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    # calculate the daily normals for your trip
    # push each tuple of calculations into a list called `normals`
    normals=[]
    dates=[]
    dates_with_years=[]
    # saving dates
    start = dt.datetime.strptime(start2, '%Y-%m-%d')
    end = dt.datetime.strptime(stop, '%Y-%m-%d')
    step = dt.timedelta(days=1)
    # Stip off the year and save a list of %m-%d strings
    while start <= end:
        date_year=str(start.date())
        date_noyear=date_year.replace('2017-', '')
        dates.append(date_noyear)
        dates_with_years.append(date_year)
        start += step
    # Loop through the list of %m-%d strings and calculate the normals for each date
    for date in dates:
        normals.append(daily_normals(date)[0])

    session.close()

    return jsonify(normals)


if __name__ == '__main__':
    app.run(debug=True)
