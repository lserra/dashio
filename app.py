#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
App Web Server Flask
"""
import itertools
from flask import render_template
from flask import Flask

import mysql.connector as mysql
from mysql.connector import errorcode

import json
from bson import json_util
# from bson.json_util import dumps

app = Flask(__name__)

"""
=================================================================================================================
this code is deprecated, because the mongodb has been changed by mysql
=================================================================================================================
from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME1 = 'donorschoose'
COLLECTION_NAME1 = 'projects'
DBS_NAME2 = 'demographics'
COLLECTION_NAME2 = 'devices'

# 1=True; 0=False
FIELDS1 = {'school_state': 1, 'resource_type': 1, 'poverty_level': 1, 'date_posted': 1, 'total_donations': 1}
FIELDS2 = {'school_state': 1, 'resource_type': 1, 'poverty_level': 1, 'date_posted': 1, 'total_donations': 1}
"""


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/main')
def index():
    return render_template('index.html')


@app.route('/dashs')
def dashs():
    return render_template('menu.html')


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/devices")
def devices():
    return render_template("devices.html")


"""
=================================================================================================================
this code is deprecated, because the mongodb has been changed by mysql
=================================================================================================================
@app.route("/donorschoose/projects")
def donorschoose_projects():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME1][COLLECTION_NAME1]
    # projects = collection.find({}, FIELDS1).limit(1)
    projects = collection.find({}, FIELDS1)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects
"""


@app.route("/donorschoose/projects")
def donorschoose_projects():
    """
    Create a connection with the MySQL Server
    Create a cursor with all records returned by query
    Save all these records in a json file
    :return:
    """
    try:
        db = mysql.connect(user='root', password='admin', host='127.0.0.1', database='dashio')

        query = 'SELECT dd.school_state as school_state, ' \
                'dd.resource_type as resource_type, ' \
                'dd.poverty_level as poverty_level, ' \
                'dd.date_posted as date_posted, ' \
                'dd.total_donations as total_donations ' \
                'FROM dashio.donorschoose dd ' \
                'WHERE DATE_FORMAT(dd.date_posted, \'%Y-%m-%d\') BETWEEN \'2015-10-11\' AND \'2016-10-11\';'

        cursor = db.cursor()
        cursor.execute(query)

        # Returns all rows from a cursor as a list of dicts
        desc = cursor.description
        json_projects = [dict(itertools.izip([col[0] for col in desc], row)) for row in cursor.fetchall()]

        json_results_p = json.dumps(json_projects, default=json_util.default)

        cursor.close()
        db.close()

        # Source:http://json-validator.com/
        json_file = '/home/df/dashio/static/json/donorschoose/projects.json'
        f = open(json_file, 'wb')
        f.write(json_results_p)
        f.close()

        return json_results_p

    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        db.close()


@app.route("/demographics/devices")
def demographics_devices():
    """
    Create a connection with the MySQL Server
    Create a cursor with all records returned by query
    Save all these records in a json file
    :return:
    """
    try:
        db = mysql.connect(user='root', password='admin', host='127.0.0.1', database='dashio')

        query = 'SELECT DATE_FORMAT(dd.timestamp, \'%Y-%m-%d\') AS date_device, dd.longitude, dd.latitude, ' \
                'dd.phone_brand_en, dd.gender, dd.age_segment, dd.qty ' \
                'FROM dashio.demographics dd ' \
                'WHERE DATE_FORMAT(dd.timestamp, \'%Y-%m-%d\') BETWEEN \'2016-01-01\' AND \'2016-12-31\';'

        cursor = db.cursor()
        cursor.execute(query)

        # Returns all rows from a cursor as a list of dicts
        desc = cursor.description
        json_devices = [dict(itertools.izip([col[0] for col in desc], row)) for row in cursor.fetchall()]

        json_results_d = json.dumps(json_devices, default=json_util.default)

        cursor.close()
        db.close()

        # Source:http://json-validator.com/
        json_file = '/home/df/dashio/static/json/demographics/devices.json'
        f = open(json_file, 'wb')
        f.write(json_results_d)
        f.close()

        return json_results_d

    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        db.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
