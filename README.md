## Weather Study

**Examination of bulk weather predictions and their accuracy. (In progress.)**

**Main idea**: Forecasters predict the weather many days in advance for any given location. How do those predictions change as the target date approaches?

**Tools used**: Python3, SQLite3, weather APIs, MatPlotLib, D3.

---

### To install

 1. Runs in Python3. Clone from GitHub and enter the newly created directory:

        git clone git@github.com:WeatherStudy/weather_study.git
        cd weather_study

   or 

        git clone https://github.com/WeatherStudy/weather_study.git
        cd weather_study

 1.  Get an API key for Open Weather Map at http://openweathermap.org/appid. Store the key in a file called `owm_api.ignore` in the `DATA/` directory. It will be read from there when API calls are made; no copies of the key should be visible in your public repository. Files ending in `.ignore` are marked in `.gitignore` as not to be pushed to the repository, so your API-key will remain private.

 1.  Set up SQLite3 database:

        sqlite3 weather_data_OWM.db < POPULATE_DB/DB_SCRIPTS/create_weather_OWM_db.sql

### To begin collecting and inserting data

 1.  Enter the `CODE/` directory. Open a Python3 REPL. Import needed Populate database with US placenames and their codes and latitude/longitude values.

        cd CODE
        ipython
        In [1]: import city_codes, populate_db, requests, check_data, utils
        
        In [2]: city_codes.get_city_code_list()

   This file will be normalized and saved to `DATA/CITY_LISTS/`.

 1.  Still in the REPL, populate the database with this data.

        In [3]: populate_db.populate_db_w_city_codes()

 1.  Still in the REPL, download forecast data from Open Weather Map:

        In [4]: requests.download_OWM_full_forecast()
        Saving to directory downloads_OWM_US_20140422-1409
            0 done out of 11731: 0.0%.
            100 done out of 11731: 0.9%.
            ...

   Once the download is complete, the content will be compressed and stored as a single `.tar.bz2` archive in the `COMPRESSED/` directory. This full download typically takes two or three hours. Alternately, you can use the `limit` default keyword if you want to specify some smaller number of sites:

        In [5]: requests.download_OWM_full_forecast(limit=100)

    For the sake of consistency this download should be done only once a day at the same time of day — we prefer between 4:30 p.m. and midnight, U.S. Eastern Daylight Savings time, when we find the content of the forecasts to be relatively uniform. 
    You will need to download forecast data yourself, once a day, for every day you want to study.

 1.  Populate the database with your downloaded data. Right now this requires a preliminary manual step: decompress the compressed data and move the resulting subdirectories into the `DOWNLOADED/` directory. Then run

        In [6]: populate_db.process_dir_of_downloads()

   Your local database keeps track of whether or not a given download directory has been used to populate it, and if so, by default it does not reinsert the data. To insert the same data even so, use

        populate_db.process_dir_of_downloads(repop_if_already_done=True)

### To analyze data.

 1. This step assumes that forecast data has already been collected for a number of days. We are using Numpy to conduct statistical analysis, MatPlotLib to plot, and D3 to display in the browser.

(Description of this part of the project is pending.)

---

### To collect NOAA forecast data.

 1. NOAA offers data in a number of different forms. For a single file of forecasts for a set of 200 major US cities, use:

        In [101]: requests.construct_NOAA_request_200_cities()

   For forecasts for all the US cities used in the OWM request above, use:

        In [102]: requests.download_NOAA_all_US_points()

   In the latter case, the argument `limit` is also available if you want to restrict the number of files downloaded:

        In [103]: requests.download_NOAA_all_US_points(limit=100)

---

[end]
