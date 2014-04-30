var map = L.map('map_canvas').setView([40, -90.], 4);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
     attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
     maxZoom: 20
	}).addTo(map);
  
