from __future__ import division

from flask import Flask, send_from_directory, jsonify
from random import randint
import math

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

@app.route('/jsonData/<x>/<y>/<z>')
def buildData(x,y,z):
    x = int(x)
    y = int(y)
    z = int(z)
    lat,lon = num2deg(x, y, z)

    #  latitudes 50 and 54 N, and longitudes 3 and 8 E.
    if 48 <= lat <= 56 and 3 <= lon <= 8:
        data = dutchData(lat,lon,z)
    else:
        data = randomData(lat,lon)
    return jsonify(data)

def randomData(lat,lon):
    bluePart = randint(10,90)
    return [{
        "location": [ lon, lat ],
        "bluePart": bluePart,
        "redPart": 100 - bluePart,
    }]

def dutchData(lat,lon,z):
    if z < 8:
        # Return aggregated data
        return [{
            "location": [ 5.0, 52.0 ],
            "bluePart": 25,
            "redPart": 75,
        }]
    else:
        # Return expanded data
        return [{
            "location": [ 4.8, 52.3 ],
            "bluePart": 90,
            "redPart": 10,
        }, {
            "location": [ 5.8, 51.8 ],
            "bluePart": 10,
            "redPart": 90,
        }]

@app.route('/<path:path>')
def send_files(path):

    return send_from_directory('', path)

app.run(host='0.0.0.0', port=8000, debug=True)
