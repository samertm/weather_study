## NDFD API running notes

[edited 20140423]

1. API access discussion at http://www.ncdc.noaa.gov/cdo-web/webservices/v2. (20140422)

1. Useful sites:

  2. 200 pre-chosen cities: `http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php?`
  2. Up to 200 individual sites: `http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?`

 (20140420)

1. Matter for the API calls:

   2. points: `listLatLon=1...`
   2. metric: `&Unit=m`
   2. maximum number of forecast days: `&product=time-series`
   2. parameters: `&maxt=maxt&mint=mint&qpf=qpf&snow=snow`
   2. daily rather than sub-daily report: `&format=24+hourly` — not sure if this always has an effect

 (20140420)
 
1. Determined that no more than 200 points can be queried at once:

        500 items: HTTP Error 400: Bad Request
        400 items: HTTP Error 414: Request-URI Too Large
        300 items: no error. len(forecast.readall().decode()): 348205
        250 items: no error. len(forecast.readall().decode()): 348205
        200 items: no error. len(forecast.readall().decode()): 348205
        199 items: no error. len(forecast.readall().decode()): 346521

 (20140420)

1. Learned from NOAA that historical forecast records are served at SRRS.

  2. GUI: http://has.ncdc.noaa.gov/pls/plhas/HAS.FileAppSelect?datasetname=9957ANX
  2. SRRS documentation: http://www1.ncdc.noaa.gov/pub/data/documentlibrary/tddoc/td9949.pdf
  2. SRRS resource description: http://www.ncdc.noaa.gov/oa/documentlibrary/surface-doc.html#9957

   Our NOAA contact, asked about API availability, says:
   
   > There is none.  This data is usually requested by customers looking for a specific date or two for forecasts or watches/warnings issued or by the NWS for plane craft accident data.
   
   We will see if using the Web-GUI we can't construct our own API-calls.

 (20140416)

1. Information from Andrea Fey about NOAA's Nomad and THREDD/LAS materials, as well as about weather forecasting models. We will defer studying these for now, however.

  2. Nomads: nomads.ncdc.noaa.gov
  2. Thredds: http://www.unidata.ucar.edu/downloads/thredds/index.jsp

 (20140416)

[end]
