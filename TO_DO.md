## Weather Study To-Do List   
     
### Questions                 
     
- [x] How often are forecasts revised?
- [ ] What is meant by `mode=daily_compact` in a query? (It does seem to change the results slightly.)
- [x] What are the locations available? List located; code written to check for updates.
- [x] How many locations can be queried in a single query? Apparently only one for forecasts.

### To build                  

- [ ] Construct protocol for preventing retrieved data from being revealed. Encryption? Or do we need to worry about this?
- [ ] Choose data to query and retain. Where is the list of all fields available for querying?
- [ ] Save returned results to file in standard format.
- [ ] Construct schema for storing data.
- [x] Construct query.
- [x] Construct saved-file name: `item` + `date_time` + suffix.

[end]