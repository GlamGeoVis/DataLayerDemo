L.VectorGrid.JsonTile = L.VectorGrid.extend({
  initialize: function(url, options, datasource) {
    this._url = url;
    this._datasource = datasource;
    L.VectorGrid.prototype.initialize.call(this, options);
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

    var tileUrl = L.Util.template(this._url, L.extend(data, this.options));

    // console.log('Fetch url: ' + tileUrl);
    return Promise.all([this._datasource, this._urlAsJson(tileUrl)])
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
