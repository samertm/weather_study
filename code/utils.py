#! /usr/bin/env python
# utils.py
# David Prager Branner and Gina Schmalzle
# 20140531, works

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
import sqlite3

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
        try:
            with open(os.path.join(file), 'r') as f:
                contents = f.read()
        except Exception as e:
            print('Error {}\n    in file {}'.format(e, file))
        if contents == '\n':
            print('File {} empty.'.format(file))
            continue
        content_dict = ast.literal_eval(contents)
        if content_dict in (None, '\n'):
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

def tar_directory(source_dir=None, target_dir='compressed'):
    """Compress all directories found in download/ and delete originals."""
    start_time = time.time()
    home_dir = os.getcwd()
    os.chdir('../data/downloads')
    # Do the whole procedure below for any existing directories in downloads.
    # First find the directories.
    if not source_dir:
        directories = open_directory('downloads_')
    else:
        directories = [source_dir]
    print('{} directories to be compressed.'.
            format(len(directories)), end='\n\n')
    # Make sure target_dir exists in .. or create it.
    if not os.path.exists('../' + target_dir):
        os.makedirs('../' + target_dir)
        print('Created directory {}'.format('target_dir'), end='\n\n')
    # Now compress each directory and finally delete it.
    for directory in directories:
        file_list = glob.glob(directory+'/*')
        print('{} files to compress in directory\n    "{}":'.
                format(len(file_list), directory))
        # Compress each contained file, using context manager.
        with tarfile.open(
                os.path.join('../' + target_dir, directory + '.tar.bz2'),
                        'w:bz2') as f:
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

def untar_directory(dir_name=None, check_db=True, db='weather_data_OWM.db'):
    """Extract all archives in compressed/ into temporary/."""
    start_time = time.time()
    connection = sqlite3.connect(os.path.join('../', db))
    home_dir = os.getcwd()
    # In order not to repeat decompressions unnecessarily, get list of all
    # archives already inserted into database.
    with connection:
        cursor = connection.cursor()
        cursor_output = cursor.execute(
                '''SELECT directory_name FROM downloads_inserted''')
        archives_done = [item[0].split('/')[-1]
                 for item in cursor_output.fetchall()]
    os.chdir('../data/compressed')
    # Do the whole procedure below for any existing directories in downloads.
    # First find the directories.
    if not dir_name:
        archives = open_directory('downloads_')
    else:
        archives = [dir_name]
    number_archives = len(archives)
    print('{} directories available to extract.'.
            format(number_archives), end='\n\n')
    # Make sure ../compressed exists or create it.
    if not os.path.exists('../temporary'):
        os.makedirs('../temporary')
        print('Created directory temporary', end='\n\n')
    # Now uncompress each directory.
    archives.sort()
    for archive in archives:
        archive_short = archive.split('.')[0]
    # If check_db, then first check whether this archive has already
    # been processed.
        if check_db and archive_short in archives_done:
            number_archives -= 1
            continue
        # Copy and then uncompress each file, using context manager.
        with tarfile.open('../compressed/' + archive , 'r:bz2') as f:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(f, "../temporary/")
        print('Decompressed directory\n    "{}".'.
            format(archive), end='\n\n')
    print('In total, {} archives extracted out of {}.'.
            format(number_archives, len(archives)))
    # When finished, return to directory where we started.
    os.chdir(home_dir)
    end_time = time.time()
    total_time = round(end_time - start_time)
    print('Total time elapsed in tarring: {} seconds; '
            '{} seconds per directory on avg.\n'.
            format(total_time, round(total_time/len(archives), 1)))
