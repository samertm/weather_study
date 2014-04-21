## NDFD Notes 20140421

[edited 20140421]

1. Timings:

  **Timing for each full download of 11K discrete points**:

        420 seconds
        367 seconds
        371 seconds
        482 seconds
        402 seconds
        366 seconds
        360 seconds
        357 seconds
        355 seconds
        351 seconds
        367 seconds

  **Timing for each full download of 200 cities**:

        8 seconds
        6 seconds
        5 seconds
        6 seconds
        7 seconds
        6 seconds
        6 seconds
        6 seconds
        6 seconds
        6 seconds
        6 seconds
        6 seconds

  Much better time than OWM! Each is plausibly a single data set.

1. Tasks I hope to get done today:

  2. Data insertion into db, from OWM (**DONE**). Needs some sort of verification, pending creation of a formal test suite.

  2. Function to store in (new) db table the name of each download set that is inserted. With this, we can keep track locally of what the local database contains. (**DONE**)

  2. Right now the download files are undergoing compression and deletion immediately at the end of the download process, so it will be necessary to do all data-related steps with a compressed file — opening it for the purpose of retrieving the data. That would happen locally, Ao that we don't have to upload the whole db.

  2. Function to retrieve data from db.

  2. And of course before we can start doing actual analysis of forecasts, we'll need observation data, too.

[end]
