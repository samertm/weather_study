Directions on how to install netcdf4
======================================
Written by Gina Schmalzle 20140422

1. You will need xcode 5.0.2 or higher to install netcdf.
2. Once installed, make sure brew is up to date:

        brew doctor
        brew update

3. Install graphics programs:

        brew install geos graphviz hdf5 jasper netcdf pil proj udunits

  * pil did not come up for me in the pip database.  I installed pillow instead, another visualization library.

4. In your favorite virtual environment

        pip install netCDF4

  In addition to netCDF4 you will need numpy, scipy, matplotlib.

Detailed instructions on downloading peripherals for netCDF found at https://github.com/SciTools/installation-recipes/blob/master/osx10.8/install.txt
