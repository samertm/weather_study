## Weather Study Installation Instructions: Part 4. Install `basemap` for MatPlotLib

These directions assume you have `matplotlib` and `numpy` already installed and updated.

After `matplotlib` is installed follow these instructions:

 1. Download the latest version of `basemap` at http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/
The version GS downloaded for this project is `basemap-1.0.7`. Untar with `tar -xzf basemap-1.0.7.tar.gz` and cd into the resulting directory.

 1. Follow the installation directions at http://matplotlib.org/basemap/users/installing.html:

   2. Install the GEOS library. If you already have it on your system, just set the environment variable `GEOS_DIR` to point to the location of `libgeos_c` and `geos_c.h` (if `libgeos_c` is in `/usr/local/lib` and `geos_c.h` is in `/usr/local/include`, set `GEOS_DIR` to `/usr/local`). Then go to next step. If you don’t have it, you can build it from the source code included with basemap by following these steps:

        ~~~
cd geos-3.3.3
export GEOS_DIR=<where you want the libs and headers to go>
# A reasonable choice on a Unix-like system is /usr/local, or
# if you do not have permission to write there, your home directory.
./configure --prefix=$GEOS_DIR
make; make install
        ~~~

   2. cd back to the top level basemap directory (basemap-X.Y.Z) and run the usual `python setup.py install`. Check your installation by running `from mpl_toolkits.basemap import Basemap` at the python prompt.

   2. To test, cd to the examples directory and run `python simpletest.py`. To run all the examples (except those that have extra dependencies or require an internet connection), execute `python run_all.py`.

---

### Further installation steps:

See these files in the `INSTALLATION_INSTRUCTIONS` directory:

 1. `install_1_dependencies.md`
 1. `install_2_database.md`
 1. `install_3_netCDF4.md`
 1. `install_4_ matplotlib_basemap.md` (**this file**)
 1. `install_5_analyze_data.md`

---

[end]
