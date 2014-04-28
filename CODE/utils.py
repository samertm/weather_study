#! /usr/bin/python
# utils.py
# David Prager Branner and Gina Schmalzle
# 20140424, works

"""Utilities for Weather Study project."""

import os
import sys
import datetime
import time
import glob
import ast
import shutil
import tarfile
import pprint

def construct_date(date_and_time=None):
    """Construct a time-and-date string for appending to a filename."""
    if not date_and_time:
        date_and_time = datetime.datetime.today()
    date_and_time = date_and_time.strftime('%Y%m%d-%H%M')
    return date_and_time

def convert_from_unixtime(unixtime, whole=True):
    """Convert Unix time to human-readable string."""
    if not whole:
        # Date only, no time.
        date = datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y%m%d')
    else:
        # Both date and time.
        date = datetime.datetime.fromtimestamp(
            unixtime).strftime('%Y%m%d-%H%M')
    return date

def open_directory(path):
    """Get list of files in a given directory."""
    file_list = glob.glob(path+'*')
    return file_list

def retrieve_data_vals(files, to_print=None):
    """From a list of files return a dictionary of forecasts.

    Dictionary contains:

      * query_date (from directory name in filenames) and
      * a series of "city_id:forecast_list_pruned" pairs.

    Each "forecast_list_pruned" list contains tuples, bearing:

      * target date/time,
      * max temp.,
      * min. temp., and
      * rain,
      * snow.
    """
    # Get the date of the query from the filename, as int. 
    #     `dt` values vary too much.
    filename = files[0]
    dir_name = filename.split('/')[-2] # e.g. downloads_OWM_US_20140414-2215
    query_date_and_time = dir_name.split('_')[-1] # e.g. 20140414-2215
    query_date = int(query_date_and_time.split('-')[0]) # e.g. 20140414
    # Process each file
    forecast_dict = {'query_date': query_date}
    for file in files:
        forecast_list_pruned = []
        with open(os.path.join(file), 'r') as f:
            contents = f.read()
        content_dict = ast.literal_eval(contents)
        if content_dict == None:
            # This happens occasionally. Ignore silently and continue.
            continue
        forecast_list_received =(content_dict['list'])
        city_id = (content_dict['city']['id'])
        for i, forecast in enumerate(forecast_list_received):
            if 'rain' in forecast:
               rain = forecast['rain']
            else:
               # We believe that when 'rain' is forecast to be zero, no 'rain'
               # key is placed in the forecast.
               rain = 0
            if 'snow' in forecast:
                # We have found explicit examples of snow = 0; not same
                # situation as rain.
                snow = forecast['snow']
            else:
                snow = 0
            forecast_tuple = (
                    forecast['dt'],
                    float(forecast['temp']['max']),
                    float(forecast['temp']['min']),
                    float(rain),
                    float(snow),
                    )
            forecast_list_pruned.append(forecast_tuple)
        forecast_dict[city_id] = forecast_list_pruned
    if to_print:
        pprint.pprint(forecast_dict) # debug
        print('\n') # debug
    return forecast_dict

def tar_directory(dir_name=None):
    """Compress all directories found in DOWNLOAD/ and delete originals."""
    start_time = time.time()
    home_dir = os.getcwd()
    os.chdir('../DATA/DOWNLOADS')
    # Do the whole procedure below for any existing directories in DOWNLOADS.
    # First find the directories.
    if not dir_name:
        directories = open_directory('downloads_')
    else:
        directories = [dir_name]
    print('{} directories to be compressed.'.
            format(len(directories)), end='\n\n')
    # Make sure ../COMPRESSED exists or create it.
    if not os.path.exists('../COMPRESSED'):
        os.makedirs('../COMPRESSED')
        print('Created directory COMPRESSED', end='\n\n')
    # Now compress each directory and finally delete it.
    for directory in directories:
        file_list = glob.glob(directory+'/*')
        print('{} files to compress in directory\n    "{}":'.
                format(len(file_list), directory))
        # Compress each contained file, using context manager.
        with tarfile.open(
                '../COMPRESSED/' + directory + '.tar.bz2', 'w:bz2') as f:
            for i, item in enumerate(file_list):
                f.add(item)
                if not i % 1000:
                    length = len(file_list)
                    print('{} files compressed out of {}: {}%.'.
                            format(i, length, round(i*100/length, 1)))
        print('\n{} files compressed in directory\n    "{}".'.
                format(len(file_list), directory), end='\n\n')
        # Once directory is compressed, we would like to delete uncompressed
        # version. `shutil` makes this easier than `os.rmdir` etc.
        shutil.rmtree(directory)
        print('Original directory "{}" deleted.'.format(directory), end='\n\n')
        print('—' * 40, end='\n\n')
    # When finished, return to directory where we started.
    os.chdir(home_dir)
    end_time = time.time()
    total_time = round(end_time - start_time)
    print('Total time elapsed in tarring: {} seconds; '
            '{} seconds per directory on avg.'.
            format(total_time, round(total_time/len(directories), 1)))

def untar_directory(dir_name=None):
    """Extract all archives in COMPRESSED/ into TEMPORARY/."""
    start_time = time.time()
    home_dir = os.getcwd()
    os.chdir('../DATA/COMPRESSED')
    # Do the whole procedure below for any existing directories in DOWNLOADS.
    # First find the directories.
    if not dir_name:
        archives = open_directory('downloads_')
    else:
        archives = [dir_name]
    print('{} directories to be extracted.'.format(len(archives)), end='\n\n')
    # Make sure ../COMPRESSED exists or create it.
    if not os.path.exists('../TEMPORARY'):
        os.makedirs('../TEMPORARY')
        print('Created directory TEMPORARY', end='\n\n')
    # Now uncompress each directory.
    for archive in archives:
        # Copy and then uncompress each file, using context manager.
        with tarfile.open('../COMPRESSED/' + archive , 'r:bz2') as f:
            f.extractall('../TEMPORARY/')
        print('Decompressed directory\n    "{}".'.
                format(archive), end='\n\n')
    # When finished, return to directory where we started.
    os.chdir(home_dir)
    end_time = time.time()
    total_time = round(end_time - start_time)
    print('Total time elapsed in tarring: {} seconds; '
            '{} seconds per directory on avg.\n'.
            format(total_time, round(total_time/len(archives), 1)))
