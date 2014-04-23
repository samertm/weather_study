// -------------- SETTINGS ------------- //
// HTML frame: dimensions & colors
var width  = 630,
    height = 630,
    color = d3.scale.category10(); // d3.scale.ordinal().domain(["000000", "FFFFFF", "baz"]).range(colorbrewer.RdBu[9]);
 
// Projection: New projection, center coord, scale(?):
var projection = d3.geo.mercator()
    .center([2.2, 46.4]) // jap: [139, 35.4]
    .scale(2400) // behavioral definition welcome 
    .translate([width / 2, height / 2]); //??
 
// SVG injection:
var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);
 
// Path
var path = d3.geo.path()
    .projection(projection)
    .pointRadius(4);
 
// Data (getJSON: TopoJSON)
d3.json("final_topo_France.json", showData);
 
// ---------- FUNCTION ------------- //
function showData(error, fra) {
 
// var #Coord: projection formerly here
 
// var #Path: formerly here
    var Levels = topojson.object(fra, fra.objects.levels);

//Append Topo polygons
    svg.append("path")
        .datum(Levels)
        .attr("d", path)
    svg.selectAll(".levels")
        .data(topojson.object(fra, fra.objects.levels).geometries)
      .enter().append("path")
        .attr("class", function(d) { return "Topo_" + d.properties.name; })
        .attr("data-elev", function(d) { return d.properties.name; })
        .attr("d", path) 
         
// Function Click > Console
    function click(a){
        console.log(a.properties.name);}
 
}