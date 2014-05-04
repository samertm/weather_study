## Weather Study Installation Instructions: Part 2. Install and Populate the Database

 1.  Get an API key for Open Weather Map at http://openweathermap.org/appid. Store the key in a file called `owm_api.ignore` in the `DATA/` directory. It will be read from there when API calls are made; no copies of the key should be visible in your public repository. Files ending in `.ignore` are marked in `.gitignore` as not to be pushed to the repository, so your API-key will remain private.

 1.  Make sure `sqlite3` is installed and then set up a SQLite3 database:

        sqlite3 weather_data_OWM.db < CODE/DB_SCRIPTS/create_weather_OWM_db.sql

### To begin collecting and inserting data

 1.  Enter the `CODE/` directory. Open a Python3 REPL. Import needed modules. Then populate database with US placenames and their codes and latitude/longitude values.

        cd CODE
        ipython
        In [1]: import city_codes, populate_db, requests, check_data, utils, retrieve
        
        In [2]: city_codes.get_city_code_list()

   This file will be normalized and saved to `DATA/CITY_LISTS/`.

 1.  Still in the REPL, populate the database with this data.

        In [3]: populate_db.populate_db_w_city_codes()

   The function will print the value of each record it inserts, unless the `to_print` argument is used:

        In [4]: populate_db.populate_db_w_city_codes(to_print=None)

 1.  Still in the REPL, download forecast data from Open Weather Map:

        In [5]: requests.download_OWM_full_forecast()
        Saving to directory downloads_OWM_US_20140422-1409
            0 done out of 11731: 0.0%.
            100 done out of 11731: 0.9%.
            ...

   Once the download is complete, the content will be compressed and stored as a single `.tar.bz2` archive in the `COMPRESSED/` directory. This full download typically takes two or three hours. Alternately, you can use the `limit` default keyword if you want to specify some smaller number of sites:

        In [6]: requests.download_OWM_full_forecast(limit=100)

    For the sake of consistency this download should be done only once a day at the same time of day — we prefer between 4:30 p.m. and midnight, U.S. Eastern Daylight Savings time, when we find the content of the forecasts to be relatively uniform. 
    You will need to download forecast data yourself, once a day, for every day you want to study.

 1.  Populate the database with your downloaded data:

        In [7]: populate_db.process_dir_of_downloads()

   This step creates a temporary directory `TEMPORARY/` into which the compressed data is extracted and later deleted, leaving the compressed form intact. Your local database keeps track of whether or not a given download directory has been used to populate it, and if so, by default it does not reinsert the data. To insert the same data even so, use:

        In [8]: populate_db.process_dir_of_downloads(repop_if_already_done=True)

---

### To collect NOAA forecast data.

 1. NOAA offers data in a number of different forms. For a single file of forecasts for a set of 200 major US cities, use:

        In [101]: requests.download_NOAA_cities_forecast()

   For forecasts for all the US cities used in the OWM request above, use:

        In [102]: requests.download_NOAA_all_US_points()

   In the latter case, the argument `limit` is also available if you want to restrict the number of files downloaded:

        In [103]: requests.download_NOAA_all_US_points(limit=2)

 1. Currently NOAA data is not being inserted into the database.

---

### Further installation steps:

See these files in the `INSTALLATION_INSTRUCTIONS` directory:

 1. `install_1_dependencies.md`
 1. `install_2_database.md` (**this file**)
 1. `install_3_netCDF4.md`
 1. `install_4_ matplotlib_basemap.md`
 1. `install_5_analyze_data.md`

---

[end]
