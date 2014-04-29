## Weather Study To-Do List

### Questions

- [ ] What is meant by `mode=daily_compact` in a query? (It does seem to change the results slightly.) **Update**: Posted question to StackOverflow.

----

- [x] Decide how to manipulate data.
- [x] Decide how to visualize data.
- [x] How often are forecasts revised? We will test this by two full runs within a 24-hour (or shorter) period. 
 * **Update**: It seems that query-runs around noon are disorganized; our three query-runs on 20140414 and 20140415 between the hours of 16:30 and 01:00 were more coherent.
 * **Update**: NOAA's gridded forecasts are updated every hour.
- [x] What is the unit of measurement for rain (in metric queries)? Mm. (Seen on bugs.openweathermap.org/projects/api/wiki/Weather_Data)
- [x] What are the locations available? List located; code written to check for updates.
- [x] How many locations can be queried in a single query? Apparently only one for forecasts.

### To build             

- [ ] Test suite. Above all: to confirm data integrity.
- [x] Tools to process all values for display.
- [ ] Make separate `INSTALL` instruction file. **Update**: separate directory created and two files placed in it.
- [ ] Place name of data source and and license information on site.
- [ ] Consider changing compression module to `shutil` (http://chimera.labs.oreilly.com/books/1230000000393/ch13.html#_problem_218).
- [ ] Replace SQL code with ORM code.
 
---

- [x] Check whether `get_city_code_list` is in fact working — successive downloaded files appear to be identical (according to diff). Then why are we downloading them?
- [x] Tools to place observation data in database.
- [x] Function to retrieve data from db.
- [x] Function to store in (new) db table the name of each download set that is inserted.
- [x] Function to store forecast data.
- [x] Tools to evaluate concisely any changes between subsequent downloads.
- [x] Tool to evaluate extent of any differences in multiple downloads for the same 24-hour period.
- [x] Select locations for study based on Country and Lat./Long. **Update**: de facto, we are studying US locations.
- [x] Experiment to see what the ideal representation of non-integer numbers is. Rain has two places of precision. Snow has between zero and two. Latitude and longitude have many. How will Python's floating point behavior affect these? Consider storing `lat` and `lon` each as a pair of integers rather than as a number or text. Or multiply by some power of ten and truncate the decimal portion, giving us only high-precision integers to store. **Update**: simply changed them to `float()` in `utils.py` and to `NUMBER` in SQL script.
- [x] Tools to fetch observation data.
- [x] Public short description suitable for README and Hacker School project pages.
- [x] Tool to read data from saved `.txt` files. Use `ast.literal_eval()`.
- [x] Tool to archive data after storage. Use `tarfile` module.
- [x] Revise `full_forecast_download()` and `make_urlrequest()` to show URL in case of error. (We had one `HTTP Error 504: Gateway Time-out` on 20140415 morning download run.)
- [x] Save returned results to file in standard format. 
- [x] Enter city list into database.
- [x] Construct schema for storing data.
- [x] Construct protocol for preventing retrieved data from being revealed. Encryption? Or do we need to worry about this? Do not — under Creative Commons license and redistribution is permitted.
- [x] Choose data to query and retain: `temp.max`, `temp.min`, `rain`. (Few options available in forecast data.)
- [x] Construct query.
- [x] Construct saved-file name: `item` + `date_time` + suffix.

[end]