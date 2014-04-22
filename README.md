## Weather Study

**Examination of bulk weather predictions and their accuracy. (In progress.)**

**Main idea**: Forecasters predict the weather many days in advance for any given location. How do those predictions change as the target date approaches?

---

### To install

1. Runs in Python3. Clone from GitHub:

    git clone git@github.com:WeatherStudy/weather_study.git
        cd weather_study

  or 

        git clone https://github.com/WeatherStudy/weather_study.git
        cd weather_study

1.  Get an API key for Open Weather Map at http://openweathermap.org/appid. Store the key in a file called `owm_api.ignore` in the `DATA` directory. 

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

  Content will be compressed and stored in the `COMPRESSED/` directory after download is complete. Alternately, you can use the `limit` default keyword if you want to specify some smaller number of sites:

        download_OWM_full_forecast(limit=100)

   This full download typically takes two or three hours and for the sake of consistency should be done only once a day at the same time of day — we prefer between 4:30 p.m. and midnight, U.S. Eastern Daylight Savings time, when the content of the forecasts is relatively consistent. 

1.  Populate the database with your downloaded data. Right now this requires a preliminary manual step: decompress the compressed data and move the resulting subdirectories into the `DOWNLOADED/` directory. Then run

        In [5]: populate_db.process_dir_of_downloads()

   Your local database keeps track of whether or not a given download directory has been used to populate it, and if so, by default it does not reinsert the data. To insert the same data even so, use

        populate_db.process_dir_of_downloads(repop_if_already_done=True)

### To analyze data.

1. This step assumes that forecast data has already been collected for a number of days. 

(Further description is pending.)

---

[end]
