function newdata() { 

	$(rmdata.mydots).each(function() {
		map.removeLayer(this);
	});

	$(rmdata.myarrow).each(function() {
		map.removeLayer(this);
	});
     
	var value = document.getElementById('date_select').value;
	
    if (value === "20140422") {
        url = '20140422gs.json';
	}
	//console.log(url);
	/*$.getJSON(url, function (data) {
	   //mapme(data);
       myData = data;
       //makeColorScale(myData);
       mapme(myData);
       makeLegend();
	//console.log(myData.length);
	});*/
    makeLegend();
    d3.json(url,function(data){
        myData = data;
        mapme(myData);
        makeHist(myData);
        makeScatter(myData);
    });

}


function makeLegend(){
    var legend = L.control({position: 'topright'});

    legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [10, 8, 6, 4, 2, 0, -2, -4, -6, -8, -10],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + colorDot(grades[i], 0) + '"></i> ' +
            //grades[i] + (grades[i+1] ? '&ndash;' + grades[i+1] + '<br>' : '+');
            grades[i];
        }

        return div;
    };

    legend.addTo(map);
}


function colorDot(day0,diffDay){
    var diff = day0-diffDay;
    if (diff <= -10) {
        return '#053061';
    } else if (diff <= -8 && diff >-10){
        return '#2166ac';
    } else if (diff <= -6 && diff >-8){
        return '#4393c3';
    } else if (diff <= -4 && diff >-6){
        return '#92c5de';
    } else if (diff <= -2 && diff >-4){
        return '#d1e5f0';
    } else if (diff <= 0 && diff >-2){
        return '#f7f7f7';
    } else if (diff <= 2 && diff >0){
        return '#fddbc7';
    } else if (diff <= 4 && diff >2){
        return '#f4a582';
    } else if (diff <= 6 && diff >4){
        return '#d6604d';
    } else if (diff <= 8 && diff >6){
        return '#b2182b';
    } else if (diff <= 10 && diff >8){
        return '#67001f';
    } else if (diff > 10){
        return '#67001f';
    }

};


function mapme(myData){
	dots = L.geoJson(myData, {
		pointToLayer: function (feature, latlng) {
            //console.log(feature.properties.mint_0);
			var makeDots = L.circleMarker(latlng, {
					radius: 1.5,
					fillColor: colorDot(feature.properties.mint_0,feature.properties.mint_1),
					color: null,
					weight: 1,
					opacity: 1,
					fillOpacity: 0.8
				})
				makeDots.addTo(map);
				return makeDots;
		}
	});
};
	

getNumWithSetDec = function( num, numOfDec ){
    var pow10s = Math.pow( 10, numOfDec || 0 );
    return ( numOfDec ) ? Math.round( pow10s * num ) / pow10s : num;
};

getAverageFromNumArr = function( numArr, numOfDec ){
    var i = numArr.length, 
        sum = 0;
    while( i-- ){
        sum += numArr[ i ];
    }
    return getNumWithSetDec( (sum / numArr.length ), numOfDec );
};
getStandardDeviation = function( numArr, numOfDec ){
    var stdDev = Math.sqrt( getVariance( numArr, numOfDec ) );
    return getNumWithSetDec( stdDev, numOfDec );
};

function getVariance (numArr, numOfDec){
    var avg = getAverageFromNumArr( numArr, numOfDec ), 
        i = numArr.length,
        v = 0;
 
    while( i-- ){
        v += Math.pow( (numArr[ i ] - avg), 2 );
    }
    v /= numArr.length;
    return getNumWithSetDec( v, numOfDec );
};

function makeScatter(myData){
    var min = Infinity,
    max = -Infinity;

    bdata = [];
    for (var i = 0; i < myData.length; i++) { 
        x = (myData[i].properties.mint_0 - myData[i].properties.mint_1); 
        bdata.push(x)
    };
    
    var average = getAverageFromNumArr(bdata,1);
    var stdev = getStandardDeviation(bdata, 1);
    data = [{ "x":1, "y":average, "s": stdev}];
    errormin = data[0].y-data[0].s;
    errormax = data[0].y+data[0].s;
    console.log(errormin, errormax);

    var m = [10, 30, 30, 30],
        w = 250 - m[1] - m[3],
        h = 300 - m[0] - m[2]

    var x = d3.scale.linear()
    .domain([0, 15])
    //.domain(d3.extent(data.map(function(d){return d.x})))
    .range([0,w]);

    var y = d3.scale.linear()
    .domain([-10, 10])
    //.domain(d3.extent(data.map(function(d){return d.y})))
    .range([h,0]);

    xaxis = d3.svg.axis().scale(x).orient("bottom").tickSize(-h);
    yaxis = d3.svg.axis().scale(y).orient("left").tickSize(-w);
    eb = errorBar()
          .oldXScale(x)
          .xScale(x)
          .oldYScale(y)
          .yScale(y)
          .yValue(function(d){return d.y})
          .xValue(function(d){return d.x})
          .xError(function(d){return null})
          .yError(function(d){return d.s});

    var svg2 = d3.select("body").append("svg")
        .attr("width", w + m[1] + m[3])
        .attr("height", h + m[0] + m[2])
      .append("g")
        .attr("class","container")
        .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

    var d = svg2.selectAll("g").data(data),

    dEnter = d.enter().append("g")
        .attr("transform",function(d){return "translate(" + x(d.x) + "," + y(d.y) + ")"})
        .attr("fill","steelblue");    
    dEnter.append("circle")
        .attr("r",5);
    dEnter.call(eb);

    svg2.append("g")
      .attr("class","axis x")
      .attr("transform", "translate(0," + y.range()[0] + ")")  
      .call(xaxis);
    svg2.append("text")
      .attr("x", w - 100 )
      .attr("y", h + 25 )
      .style("text-anchor","middle")
      .text("Days till Target Day");
    svg2.append("g")
      .attr("class","axis y")
      .attr("transform", "translate(" + x.range()[0] + ",0)")
      .call(yaxis);
    svg2.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -25)
        .attr("x", -130)
        .attr("dy", "1em")
        .style("text-anchor","middle")
        .text("Average Difference");

}


function makeHist(myData){
    values = [];
    for (var i = 0; i < myData.length; i++) { 
        x = (myData[i].properties.mint_0 - myData[i].properties.mint_1); 
        values.push(x)};
   // console.log(values);
    var formatCount = d3.format(",.0f");

    var margin = {top: 50, right: 30, bottom: 30, left: 120},
        width = 250 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain([-20, 20])
        .range([-100,100]);

    // Generate a histogram using twenty uniformly-spaced bins.
    var data = d3.layout.histogram()
        .bins(d3.range(-20,20,2))
        //.bins(x.ticks(21))
        (values);

    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return d.y; })])
        .range([height, 0]);


    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");
 
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("float", "right")
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var bar = svg.selectAll(".bar")
        .data(data)
      .enter().append("g")
        .attr("class", "bar")
        .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

    bar.append("rect")
        .attr("x", 1)
        .attr("width", x(data[0].dx) - 1)
        .attr("height", function(d) { return height - y(d.y); });

    bar.append("text")
        .attr("dy", ".75em")
        .attr("y", -16)
        .attr("x", x(data[0].dx) / 2)
        .attr("text-anchor", "middle")
        .text(function(d) { return formatCount(d.y); });

    svg.append("text")
        .attr("x", width/10 )
        .attr("y", height + 30 )
        .style("text-anchor","middle")
        .text("Differenced Values");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);




}



/* Event handlers */
var rmdata = {
    mydots: [],
    myarrow: []
};

var mapclick = {
    startLatlng: null,
    endLatlng: null,
    currentLine: null,
    allArray: []
};

var myData = {};

$( document ).ready(function () {
    newdata();
});
