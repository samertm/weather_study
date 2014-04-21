## NDFD Notes 20140420

[edited 20140420]

1. Returning to NOAA work after a week or so on OWM. Determined that no more than 200 points can be queried at once:

        500 items: HTTP Error 400: Bad Request
        400 items: HTTP Error 414: Request-URI Too Large
        300 items: no error. len(forecast.readall().decode()): 348205
        250 items: no error. len(forecast.readall().decode()): 348205
        200 items: no error. len(forecast.readall().decode()): 348205
        199 items: no error. len(forecast.readall().decode()): 346521

1. API queries composed and coded for two NOAA services: a list of 200 cities and the c. 11K points we have from OWM.

1. Both queries now compress and delete the original downloads, saving space. 

1. Since NOAA supplies only very short-term forecasts for rain and snow, I have more confidence that they have confidence in the values they are supplying.

1. Handling of `http.client.IncompleteRead` in large multi-point downloads.

[end]
