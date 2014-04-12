## NDFD Notes

[edited 20140412]

1. Installing `mpld3` under pip3 succeeds, but it cannot be imported without `matplotlib` installed.

1. Various `matplotlib` dependencies were installed under pip3, but `matplotlib` itself fails repeatedly to install. Finally cloned from repo:

    pip install pyzmq dateutils pyparsing tornado numpy scipy pygtk cairocffi[all]
    git clone https://github.com/matplotlib/matplotlib
    cd matplotlib
    python3 setup.py build

Now installing `matplotlib` from the clone succeeds:

    sudo python3 setup.py install
    ipython3
    In [1]: import mpld3
    In [2]: import matplotlib

No error messages now. Finally, remove installed `matplotlib` clone:

    cd ..
    sudo rm -R matplotlib

[end]
