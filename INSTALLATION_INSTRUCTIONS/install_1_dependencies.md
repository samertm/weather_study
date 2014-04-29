## Weather Study Installation Instructions: Part 1. Download dependencies

 1. Install the current version of `matplotlib`. As of this writing (20140428), the current version is 1.4.x and it is not yet available through `pip`. So we do the following three steps:
 
   2. Set up a virtual environment (we are using Python 3.4 and have not tested this code with other versions):

        virtualenv --python=python3 v_env3
        source v_env3/bin/activate

     Note that this `source` line must be used to activate the local virtual environment every time you start working with the Weather Study tools.

   2. Install `numpy`, which is a dependency of `matplotlib`:

        pip install numpy

     This is a somewhat long install and may require versions of fortran, gcc, and other Unix tools. On Mac OS X 10.9 we have used `brew` to install these.

   2. Clone the current version of `matplotlib`:

        git clone https://github.com/matplotlib/matplotlib --depth=1

     We use `--depth=1` to ignore the full repository history, shortening the download process considerably.

 1. Once `matplotlib` is installed, install the other requirements:

        pip install -Ur requirements_python3.txt

---

### Further installation steps:

See these files in the `INSTALLATION_INSTRUCTIONS` directory:

 1. `install_1_dependencies.md` (**this file**)
 1. `install_2_database.md`
 1. `install_3_netCDF4.md`
 1. `install_4_ matplotlib_basemap.md`
 1. `install_5_analyze_data.md`

---

[end]