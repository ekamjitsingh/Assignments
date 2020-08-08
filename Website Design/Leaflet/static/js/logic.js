var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson"

// Perform a GET request to the query URL
d3.json(queryUrl, function(data) {
  // Once we get a response, send the data.features object to the createFeatures function
  createFeatures(data.features);
});

function createFeatures(earthquakeData) {
// empty array
var circleMarkers = [];

 for (var i = 0; i < earthquakeData.length; i++) {
// Conditionals for colour of earthquake circles 
  var color = "Purple";
  if (earthquakeData[i].properties.mag > 5) {
    color = "DarkRed";
  }
  else if (earthquakeData[i].properties.mag > 4) {
    color = "Red";
  }
  else if (earthquakeData[i].properties.mag > 3) {
    color = "orange";
  }
  else if (earthquakeData[i].properties.mag > 2) {
    color = "yellow";
  }
  else if (earthquakeData[i].properties.mag > 1) {
    color = "GreenYellow";
  } else {
    color = "green";
  }
  
 // Pushing circles to previously empty array

 circleMarkers.push(
  L.circle([earthquakeData[i].geometry.coordinates[1],  earthquakeData[i].geometry.coordinates[0]], {
    fillOpacity: 0.75,
    color: color,
	opacity: 0, //I didn't like the outlines so I made it invisible
    fillColor: color,
    radius: earthquakeData[i].properties.mag * 40000
  }).bindPopup("<h3>" + earthquakeData[i].properties.place +
      "</h3><hr><p>" + new Date(earthquakeData[i].properties.time) + "</p>" + "<p>" + " Magnitude: " + earthquakeData[i].properties.mag + "</p>")
	  );
}

//creating layer
 circleLayer= L.layerGroup(circleMarkers);
 
//sending layer to createMap function
  createMap(circleLayer);
}

function createMap(earthquakes) {

  // Define streetmap and darkmap layers
  var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  });

  var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.dark",
    accessToken: API_KEY
  });

  // Define a baseMaps object to hold our base layers
  var baseMaps = {
    "Street Map": streetmap,
    "Dark Map": darkmap
  };

  // Create overlay object to hold our overlay layer
  var overlayMaps = {
    Earthquakes: earthquakes
  };

  // Create our map, giving it the streetmap and earthquakes layers to display on load
  var myMap = L.map("map", {
    center: [
      43, -79
    ],
    zoom: 4,
    layers: [streetmap, earthquakes]
  });
  
  function getColor(d) {
    return d > 5 ? 'DarkRed' :
           d > 4  ? 'Red' :
           d > 3  ? 'Orange' :
           d > 2  ? 'Yellow' :
           d > 1   ? 'GreenYellow' :
           d > 0   ? 'Green' :
                      '#Purple';
}
  
  var legend = L.control({
        position: 'bottomright'
 });
 
legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 1, 2, 3, 4, 5],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(myMap);

  // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(myMap);
}
