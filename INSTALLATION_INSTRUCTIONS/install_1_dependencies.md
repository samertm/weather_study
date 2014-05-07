## Weather Study Installation Instructions: Part 1. Download dependencies

 1. Install the current version of `matplotlib`. As of this writing (20140428), the current version is 1.4.x and it is not yet available through `pip`. So we do the following three steps:
 
   2. Set up a virtual environment (we are using Python 3.4 and have not tested this code with other versions):

        ~~~
virtualenv --python=python3 v_env3
source v_env3/bin/activate
        ~~~

     Note that this `source` line must be used to activate the local virtual environment every time you start working with the Weather Study tools.

   2. Install `numpy`, which is a dependency of `matplotlib`:

        ~~~
pip install numpy
        ~~~

     This is a somewhat long install and may require versions of fortran, gcc, and other Unix tools. On Mac OS X 10.9 we have used `brew` to install these. On Ubuntu 14.04 we have used `sudo apt-get install liblapack-dev libblas-dev libatlas-base-dev gfortran libpng-dev libjpeg8-dev libfreetype6-dev libqt4-core libqt4-gui libqt4-dev libzmq-dev`.

   2. Clone the current version of `matplotlib` (which is likely to be later than that available through `brew` or `apt-get`):

        ~~~
git clone https://github.com/matplotlib/matplotlib --depth=1
        ~~~

     We use `--depth=1` to ignore the full repository history, shortening the download process considerably.

 1. Once `matplotlib` is installed, install the other requirements. Below is the Ubuntu version:

        pip install -Ur requirements_python3_ubuntu1404.txt

   Note that references to `basemap`, `matplotlib`, `netCDF14` may need to be removed from the `requirements_python3.txt` file since some of these things are being installed through tools other than `pip`. In addition, on Ubuntu, we have encountered errors installing `gnureadline`; we removed it from `requirements_python3.txt` and continued with `pip` installation. 
   On Ubuntu v. 14.04, there were additional dependencies, found through `apt-get`:

   2. `cffi` required `libffi-dev`;
   2. `Pillow` required `libtiff4-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev`;.
   2. `gnureadline` requires `libreadline6-dev libtinfo-dev`, but apparently something else is needed, too.

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
