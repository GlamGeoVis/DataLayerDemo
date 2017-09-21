from __future__ import division

from flask import Flask, send_from_directory, jsonify, request
from random import randint
import math
import pandas as pd

app = Flask(__name__, static_url_path='/')

# http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)

    lat_deg += 0.001 if lat_deg==0.0 else 0.0
    lon_deg += 0.001 if lon_deg==0.0 else 0.0
    return (lat_deg, lon_deg)

@app.route('/jsonData/<x>/<y>/<z>/cat')
# Connected to 'column selection' button
# Display pie charts based on category data
def buildCatData(x,y,z):
    # Use different datasets for each zoomlevel
    data = buildClusteredData(x,y,z,'cat')
    return jsonify(data)

@app.route('/jsonData/<x>/<y>/<z>/aut')
# Connected to 'column selection' button
# Display pie charts based on author data
def buildAutData(x,y,z):
    # Use different datasets for each zoomlevel
    data = buildClusteredData(x,y,z,'aut')
    return jsonify(data)

def buildClusteredData(x,y,z,var):
    x = int(x)
    y = int(y)
    z = int(z)
    lat,lon = num2deg(x, y, z)

    if z >= 9:
        data = dummyClusterData(x,y,z,'dataZL9.csv',var)
    elif z == 8:
        data = dummyClusterData(x,y,z,'dataZL8.csv',var)
    elif z == 7:
        data = dummyClusterData(x,y,z,'dataZL7.csv',var)
    elif z == 6:
        data = dummyClusterData(x,y,z,'dataZL6.csv',var)
    elif 4 == z or z == 5:
        data = dummyClusterData(x,y,z,'dataZL4.csv',var)
    elif z <=3:
        data = dummyClusterData(x,y,z,'dataZL3.csv',var)
    return data

@app.route('/jsonData/<x>/<y>/<z>/Wolff')
# Connected to free text search box
# Display data filtered for one particular property (in this case: author = Wolff)
def buildWolffData(x,y,z):
    x = int(x)
    y = int(y)
    z = int(z)

    # Use one dataset independent of zoomlevel
    lat,lon = num2deg(x, y, z)
    if z < 9:
        data = queryData(x,y,z)
    else:
        data = []
    return jsonify(data)


def buildPieData(latlon, group, var):
    d = group.groupby(var).size().to_dict()
    nItems = sum(d.values())
    print 'Build pie data, nr of items: : ',nItems
    data = { k:100 * v/nItems for k,v in d.iteritems() }
    data["location"] = [ latlon[1], latlon[0] ]
    return data

def dummyClusterData(x,y,z,file,var):
    lat0,lon0 = num2deg(x, y, z)
    lat1,lon1 = num2deg(x + 1, y + 1, z)
    # Here instead of loading data from file, we will load data clustered
    # for the lat/lon we are interested in
    data = pd.read_csv(file, sep=' ', names=['lat', 'lon', 'w', 'cat', 'aut'])
    byLL = data.groupby(['lat', 'lon'])
    return [ buildPieData(latlon,g,var) for latlon,g in byLL ]


def queryData(x,y,z):
    print 'Read Wolff data...'
    lat0,lon0 = num2deg(x, y, z)
    lat1,lon1 = num2deg(x + 1, y + 1, z)
    # Here instead of loading data from file, we will load data clustered
    # for the lat/lon we are intereste on
    data = pd.read_csv('dataWolff.csv', sep=' ', names=['lat', 'lon', 'w', 'cat'])
    print 'Zoomlevel: ',z
    byLL = data.groupby(['lat', 'lon'])
    print 'Group data'
    return [ buildPieData(latlon,g,'cat') for latlon,g in byLL ]

@app.route('/<path:path>')
def send_files(path):
    return send_from_directory('', path)

app.run(host='0.0.0.0', port=8000, debug=True)
