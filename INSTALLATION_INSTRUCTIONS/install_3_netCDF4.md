## Weather Study Installation Instructions: Part 3. Install `netcdf4`

 1. You will need xcode 5.0.2 or higher to install `netcdf`.
 1. Once installed, make sure `brew` is up to date:

        brew doctor
        brew update

 1. Install graphics programs:

        brew install geos graphviz hdf5 jasper netcdf proj udunits

   We would like to include the Python Imaging Library (PIL), but it does not yet support Python3 (http://www.pythonware.com/products/pil/, as of 20140424). I installed `pillow` instead, another visualization library:
  
        pip install pillow

 1. In your favorite virtual environment

        pip install netCDF4

   In addition to `netCDF4` you will need `numpy`, `scipy`, `matplotlib`.

Detailed instructions on downloading peripherals for `netCDF` are to be found at https://github.com/SciTools/installation-recipes/blob/master/osx10.8/install.txt.

---

### Further installation steps:

See these files in the `INSTALLATION_INSTRUCTIONS` directory:

 1. `install_1_dependencies.md`
 1. `install_2_database.md`
 1. `install_3_netCDF4.md` (**this file**)
 1. `install_4_ matplotlib_basemap.md`
 1. `install_5_analyze_data.md`

---

[end]
