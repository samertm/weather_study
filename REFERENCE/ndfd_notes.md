## NDFD Notes

[edited 20140411]

1. NDFD: National Digital Forecast Database. http://www.nws.noaa.gov/ndfd/technical.htm

1. Proprietary applications "DeGRIB" and "GRIB2 Decoder" exist to decode the GRIB2 binary data files. (http://www.nws.noaa.gov/mdl/NDFD_GRIB2Decoder/) We had some complications compiling and making them

1. XML (including samples) is available from NDFD. See:

  2. "[How do you use the web service?](http://graphical.weather.gov/xml/#use_it)"

  2. "[What if I need lots of NDFD data or find the web service too slow?](http://graphical.weather.gov/xml/#degrib)"

1. XML is served through Simple Object Access Protocol (SOAP) requests. Python 2.7 libraries:

  2. `suds`: Lightweight SOAP client
  2. `SOAPpy`: SOAP Services for Python

1. On Python SOAP requests, see 

  2. http://stackoverflow.com/questions/18902517/sending-a-soap-request-from-python
  2. http://stackoverflow.com/questions/19708597/how-to-make-a-soap-request-by-using-soappy
  2. http://www.diveintopython.net/soap_web_services/

1. Have requested to join the Yahoo-based discussion forum. However, there is also a REST service: http://graphical.weather.gov/xml/rest.php. There are sample query strings under http://graphical.weather.gov/xml/rest.php#use_it:

        http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=38.99&lon=-77.01&product=time-series&begin=2004-01-01T00:00:00&end=2013-04-20T00:00:00&maxt=maxt&mint=mint

        http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?listLatLon=38.99,-77.02 39.70,-104.80 47.6,-122.30&product=time-series&begin=2004-01-01T00:00:00&end=2013-04-20T00:00:00&Unit=e&maxt=maxt&mint=mint

1. Some details about what the database contains:

  2. [Description of NDFD Database Contents: Elements](http://www.nws.noaa.gov/ndfd/technical.htm#elements);

  2. [Element Definitions](http://www.nws.noaa.gov/ndfd/definitions.htm).

1. It isn't clear to us whether "maximum/minimum temperature" and "apparent temperature" are predictions or not. On 20140411, we wrote to the National Weather Service (NWS) to ask for clarification about this.

[end]
