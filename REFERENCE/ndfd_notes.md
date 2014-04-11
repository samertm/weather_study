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

1. Have requested to join the Yahoo-based discussion forum. However, there is also a REST service: http://graphical.weather.gov/xml/rest.php

[end]
