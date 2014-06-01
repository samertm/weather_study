function newdata() { 

	$(rmdata.mydots).each(function() {
		map.removeLayer(this);
	});

	$(rmdata.myarrow).each(function() {
		map.removeLayer(this);
	});
     
	var value = document.getElementById('date_select').value;
	
    if (value === "20140422") {
        url = '20140422.json';
	}
	console.log(url);
	$.getJSON(url, function (data) {
	   //mapme(data);
       myData = data;
	//console.log(myData.length);
	});

}

function mapme(myData){
//Load in Selected JSON file
	var myFilteredData = $(myData).filter(function() {
		return this.properties.svx <= document.getElementById('sigmax').value && this.properties.svy <= document.getElementById('sigmax').value;
	});
	
    myFilteredData = [].slice.call(myFilteredData);
	dots = L.geoJson(myFilteredData, {
		pointToLayer: function (feature, latlng) {
			var makeDots = L.circleMarker(latlng, {
					radius: 3,
					fillColor: "#ff7800",
					color: "#000",
					weight: 1,
					opacity: 1,
					fillOpacity: 0.8
				})
				rmdata.mydots.push(makeDots);
				makeDots.addTo(map);
				return makeDots;
		}
	});
};
	



function highCharts(mydataplot, myuncertsplot, myparplot, myparuncertsplot, myperpplot, myperpuncertsplot){
        $('#container').highcharts({
            chart: {
                zoomType: 'xy'
            },
            title: {
                //text: 'GPS velocity as a function of Distance along a Profile'
                text: ''
            },
           // subtitle: {
           //     text: 'GPS Magnitude'
           // },
            xAxis: {
                title: {
                    enabled: false,
                    text: 'Distance (km)'
                },
                startOnTick: true,
                endOnTick: true,
                showLastLabel: true
            },
            yAxis: {
                title: {
                    text: 'V Magnitude (mm/yr)'
                }
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                verticalAlign: 'bottom',
                x: 100,
                y: 70,
                floating: true,
                backgroundColor: '#FFFFFF',
                borderWidth: 1
            },
            plotOptions: {
                scatter: {
                    marker: {
                        radius: 5,
                        states: {
                            hover: {
                                enabled: true,
                                lineColor: 'rgb(100,100,100)'
                            }
                        }
                    },
                    states: {
                        hover: {
                            marker: {
                                enabled: false
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: '<b>{series.name}</b><br>',
                        pointFormat: '{point.x} km, {point.y} mm/yr'
                    }
                }
            },
            series: [{
                name: 'Magnitude',
                type: 'scatter',
                color: 'rgba(223, 83, 83, .7)',
                data: mydataplot
            } , 
    	/*{ 
            name: 'GPS error',
            type: 'errorbar',
            data: myuncertsplot
           } */

    	],
        });
    };  /* End High Charts function */


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
    
    // var url = '/vectorprojector/data/pbo_velocity_snarf.json';

    // $.getJSON(url, function (myData) {
    //         mapme(myData);
    //         transect(myData);
    // });

    newdata();
});
