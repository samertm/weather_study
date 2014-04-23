## OWM API Running notes

1. In pursuit of weather observation data, see the history API: http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_history

  2. Using http://openweathermap.org/data/2.5/history/city/?id=5106292&type=day&units=metric&APPID=[API-key] brings up records like this running back about a day (`"cnt":23`):

        ~~~
"list":[
 {"main":{"temp":282.24,"humidity":40,"pressure":1022,"temp_min":278.15,"temp_max":284.82},
  "wind":{"speed":0.51,"gust":2.57,"deg":47},
  "clouds":{"all":0},
  "weather":[{"id":800,"main":"Clear","description":"Sky is Clear","icon":"01d"}],
  "dt":1398087314}
...]
        ~~~

     It looks as though the temperature is in Kelvin (despite our requesting metric) and the period is the hour (despite our requesting by the day). And I don't see how to go further back than 24 hours. So this doesn't seem very useful. (20140422)

  2. The page http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_history shows more useful results for weather stations rather than cities, but the examples there do not seem to work. 
  2. We can get current weather with, for instance, http://api.openweathermap.org/data/2.5/weather?id=2172797&units=metric&APPID=[API-key] but not historical
  2. We intend at the moment to concentrate only on the trends within forecast data rather than the relationship between the forecasts and the observation.

 (20140422)

1. Existing Python resource: https://github.com/csparpa/pyowm.

 > PyOWM is a client Python wrapper library for the OpenWeatherMap (OWM) web API.>
 > PyOWM runs on Python 2.7, 3.2 and 3.3

 Seems to be well documented. (20140413)

1. Attempting to search multiple location-IDs at once returns only the first of them:

    http://api.openweathermap.org/data/2.5/forecast?id=2643743,6058560

  returns data for 2643743 but none for 6058560. (20140413)

1. Appending `&cnt=14` to API call retrieves 14 days of forecast content. But the content is almost identical without `cnt` entry or with `&cnt=0`. (20140413)

1. List of cities found at http://openweathermap.org/help/city_list.txt. Code written to keep a copy of this, with hash, so that changes can be identified quickly. (20140413)

1. For bulk data, can we using `bbox` (bounding box find)? http://bugs.openweathermap.org/projects/api/wiki/Api_2_5/6. Don't understand the five parameters used:

        bbox=12,32,15,37,10

  perhaps means longitude in range 12-14, latitude in range 32-37, and a total of 10 points? Need more data. (20140413)

1. Appid must go last in query. Using

        http://openweathermap.org/data/2.5/forecast/city?...

  we only get five days of forecast, at three-hour intervals, regardless of what `cnt` parameters we use. But using

        http://openweathermap.org/data/2.5/forecast/daily?...

  we get as many days as we request, up to 16(!). Within Ipython, using

        import utils as U
        U.construct_OWM_api_req(count=16)['list']

(20140413)

1. The decoded JSON object is a dict, whose key 'list' is a list containing most of the content. (20140413)

1. List of the main description parameters: http://bugs.openweathermap.org/projects/api/wiki/Weather_Data. (20140413)

### Questions

1. What does `'cod': '200'` mean in results? Not the Weather Condition Codes (http://bugs.openweathermap.org/projects/api/wiki/Weather_Condition_Codes), which are given at `weather.id`.

1. There are slight differences in the daily forecast results with and without `&mode=daily_compact` in the query. **Update 20140423**: No idea yet what this means.

[end]
