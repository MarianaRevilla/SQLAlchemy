#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 16:17:48 2020

@author: marianarevilla
"""


# import Flask
from flask import Flask, jsonify


# In[30]:

import datetime as dt
from datetime import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np


# In[31]:


# create an app
app = Flask(__name__)


# In[32]:


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
stations = Base.classes.station
session = Session(engine)


# In[33]:


@app.route("/")
def home():
    return (f"home page <br/>"
           f"available routes: <br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start<br/>"
           f"/api/v1.0/start/end<br/>")


# In[34]:

@app.route("/api/v1.0/precipitation")
# retrieves the last 12 months of precipitation data
def rain():
    rain_results = session.query(measurement.date, measurement.prcp).\
                   filter(measurement.date.between('2016-08-23', '2017-08-23')).all()
    rain= []
    for result in rain_results:
            row = {"date":"prcp"}
            row["date"] = result[0]
            row["prcp"] = (result[1])
            rain.append(row)
    return jsonify(rain)

# In[35]:

@app.route("/api/v1.0/stations")
# retrieves all the stations from the station table 
def station():
    stations = session.query(measurement.station).all()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

# In[36]:


@app.route("/api/v1.0/tobs")
# retrieves the last 12 months of temperature observation data (TOBS)
def tobs():
    temp_results = session.query(measurement.station, measurement.tobs).filter(measurement.station == 'USC00519281' ).filter(measurement.date.between('2016-08-01', '2017-08-01')).all()
    temp=[]
    for tobs in temp_results:
        t_dict = {}
        t_dict["station"] = tobs[0]
        t_dict["tobs"] = float(tobs[1])
        temp.append(t_dict)
    return jsonify(temp)


# In[ ]:

@app.route ("/api/v1.0/start")
def start():
    start_t= session.query(func.max(measurement.tobs), \
                            func.min(measurement.tobs),\
                            func.avg(measurement.tobs)).\
                            filter(measurement.date >= '2016-02-10') 
    tobs_list = []
    for tobs in start_t:
        tobs_dict = {}
        tobs_dict["average temperature"] = float(tobs[2])
        tobs_dict["maximum temperature"] = float(tobs[0])
        tobs_dict["minimum temperature"] = float(tobs[1])
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/start/end")
def end():      
    results=session.query(func.max(measurement.tobs).label("max_tobs"), \
                      func.min(measurement.tobs).label("min_tobs"),\
                      func.avg(measurement.tobs).label("avg_tobs")).\
                      filter(measurement.date.between('2016-08-01', '2016-08-15'))   

    se_list = []
    for tobs in results:
        se_dict = {}
        se_dict["average temperature"] = float(tobs[2])
        se_dict["maximum temperature"] = float(tobs[0])
        se_dict["minimum temperature"] = float(tobs[1])
        se_list.append(se_dict)
    return jsonify(se_list)


# In[37]:


if __name__ == "__main__":
   app.run(debug=True)