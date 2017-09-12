L.VectorGrid.JsonTile = L.VectorGrid.extend({
  // dataLayer should be a leaflet-dvf DataLayer
  initialize: function(url, options, dataLayer) {
    this._url = url;
    this._dataLayer = dataLayer;
    this._zoom = -1;
    L.VectorGrid.prototype.initialize.call(this, options);
    this.on('load', function() {
      this._dataLayer.reloadData();
    });
  },
  _urlAsJson: function(tileUrl) {
    return fetch(tileUrl).then(
      function(response) {return response.json();
    });
  },
  _getVectorTilePromise: function(coords) {
    var data = {
      s: 'abc',
      x: coords.x,
      y: coords.y,
      z: coords.z
    };
    if (this._map && !this._map.options.crs.infinite) {
      var invertedY = this._globalTileRange.max.y - coords.y;
      if (this.options.tms) {
        data['y'] = invertedY;
      }
      data['-y'] = invertedY;
    }

    if(this._zoom!=coords.z) {
      this._zoom = coords.z;
      while(this._dataLayer._data.length > 0) {
        this._dataLayer._data.pop();
      }
    }

    var tileUrl = L.Util.template(this._url, L.extend(data, this.options));
    // console.log('Fetch url: ' + tileUrl);
    return Promise.all([this._dataLayer._data, this._urlAsJson(tileUrl)])
      .then(function(args) {
        var dataSource = args[0];
        var data = args[1];
        data.forEach(function(item) {
            dataSource.push(item);
        });
        return {};
      });
  }
});

L.vectorGrid.jsontile = function(url, options) {
  return new L.VectorGrid.JsonTile(url, options);
};
