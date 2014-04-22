## Weather Study

**Examination of bulk weather predictions and their accuracy. (In progress.)**

---

Forecasters predict the weather many days in advance for any given location. How do those predictions change as the target date approaches?

### To install

1. Runs in Python3. Clone from GitHub:

    git clone git@github.com:WeatherStudy/weather_study.git
        cd weather_study

  or 

        git clone https://github.com/WeatherStudy/weather_study.git
        cd weather_study

1.  Set up SQLite3 database:

        sqlite3 weather_data_OWM.db < POPULATE_DB/DB_SCRIPTS/create_weather_OWM_db.sql

1.  Populate database with US placenames.

    

1.  Open a Python3 REPL and Download forecast data from Open Weather Map:

        ipython
        In [1]: import city_codes, populate_db, requests, check_data, utils
        
        In [2]: requests.download_OWM_full_forecast()
        Saving to directory downloads_OWM_US_20140422-1409
            0 done out of 11731: 0.0%.
            100 done out of 11731: 0.9%.

        ...

  Content will be compressed after download is complete. This full download typically takes two or three hours.

    

### Populate the database:

---

Questions:

 * Can we make statistical generalizations about how those predictions change, and about the different kinds of locations for which predictions display different patterns of change?
 * In what useful ways can we map these patterns or otherwise display them graphically?

[end]
