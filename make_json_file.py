#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demographics Devices Analysis
Exporting the data from MySQL to JSON File
"""

import itertools
import mysql.connector as mysql
from mysql.connector import errorcode

import json
from bson import json_util
# from bson.json_util import dumps


def demographics_devices(path):
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
        json_file = path + 'devices.json'
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
    path = '/home/df/dashio/static/json/demographics/'
    demographics_devices(path)