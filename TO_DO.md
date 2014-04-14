## Weather Study To-Do List   
     
### Questions                 
     
- [ ] How often are forecasts revised?
- [ ] What is meant by `mode=daily_compact` in a query? (It does seem to change the results slightly.)
- [x] What are the locations available? List located; code written to check for updates.
- [x] How many locations can be queried in a single query? Apparently only one for forecasts.

### To build                  

- [ ] Save returned results to file in standard format. 
- [x] Construct schema for storing data.
- [ ] Enter city list into database and then select points for study based on Country and Lat./Long.
- [x] Construct protocol for preventing retrieved data from being revealed. Encryption? Or do we need to worry about this? Do not — under Creative Commons license and redistribution is permitted.
- [x] Choose data to query and retain: `temp.max`, `temp.min`, `rain`. (Few options available in forecast data.)
- [x] Construct query.
- [x] Construct saved-file name: `item` + `date_time` + suffix.

[end]