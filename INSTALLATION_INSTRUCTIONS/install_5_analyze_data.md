## Weather Study Installation Instructions: Part 5. Analyze Data.

 1. This step assumes that forecast data has already been collected for a number of days. We are using `Numpy` to conduct statistical analysis, `MatPlotLib` to plot, and `netCDF4` to display in the browser.
 1. To retrieve data for the database there are presently two functions. For multiple dates, use:

        In [9]: retrieve.get_multidate_data_from_db()

   The data structure returned is a list of tuples. Each tuple contains three elements:

   - sub-tuple containing latitude and longitude (floats);
   - target_date (int);
   - list of 15 sub-sub-tuples, each containing
   - `maxt`, `mint`, `rain`, `snow` (floats).

   For dates where the database contains no data, the forecast tuple is: `(None, None, None, None)`.

   It is possible to narrow down the output of this function with the argument `exact_date`, specifying the date as integer:
   
       In [10]: retrieve.get_multidate_data_from_db(exact_date=20140424)

   It is also possible to narrow down the output of this function with two other default arguments, both also integers, which may be used together or singly:
   
       In [11]: retrieve.get_multidate_data_from_db(start_date=20140423, end_date=20140424)

 1. For a single date, use:

       In [12]: retrieve.get_single_date_data_from_db(exact_date)

   where `exact_date` is an integer. This function returns a dictionary, with latitude and longitude (as a tuple) as the key and a list of sub-tuples (as above) the key.

 1. (Further description of this part of the project is pending.)

---

### Further installation steps:

See these files in the `INSTALLATION_INSTRUCTIONS` directory:

 1. `install_1_dependencies.md`
 1. `install_2_database.md`
 1. `install_3_netCDF4.md`
 1. `install_4_ matplotlib_basemap.md`
 1. `install_5_analyze_data.md` (**this file**)

---

[end]
