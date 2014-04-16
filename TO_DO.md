## Weather Study To-Do List

### Questions

- [ ] Decide how to manipulate data.
- [ ] Decide how to visualize data.
- [ ] How often are forecasts revised? We will test this by two full runs within a 24-hour (or shorter) period.
- [ ] What is meant by `mode=daily_compact` in a query? (It does seem to change the results slightly.)
- [ ] What is the unit of measurement for rain (in metric queries)?
- [x] What are the locations available? List located; code written to check for updates.
- [x] How many locations can be queried in a single query? Apparently only one for forecasts.

### To build                  

- [ ] Tool to evaluate extent of any differences in the 10 p.m. and 10 a.m. downloads for the same 24-hour period.
- [x] Tool to read data from saved `.txt` files. Use `ast.literal_eval()`.
- [x] Tool to archive data after storage. Use `tarfile` module.
- [ ] Select locations for study based on Country and Lat./Long.
- [ ] Place OWM's name and license information on site.
- [ ] Consider storing `lat` and `lon` each as a pair of integers rather than as a number or text. 
- [x] Revise `full_forecast_download()` and `make_urlrequest()` to show URL in case of error. (We had one `HTTP Error 504: Gateway Time-out` on 20140415 morning download run.)
- [x] Save returned results to file in standard format. 
- [x] Enter city list into database.
- [x] Construct schema for storing data.
- [x] Construct protocol for preventing retrieved data from being revealed. Encryption? Or do we need to worry about this? Do not — under Creative Commons license and redistribution is permitted.
- [x] Choose data to query and retain: `temp.max`, `temp.min`, `rain`. (Few options available in forecast data.)
- [x] Construct query.
- [x] Construct saved-file name: `item` + `date_time` + suffix.

[end]