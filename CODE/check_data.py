#! /usr/bin/python
# check_data.py
# David Prager Branner and Gina Schmalzle
# 20140419, works

"""Programs to examine character of data in Weather Study project."""

import os
import ast
import pprint
import difflib
import glob
import utils as U

def check_dt_uniformity_01():
    """Report all initial dt values & # of forecasts in all files in one dir."""
    # Get names of directories in download folder
    directories = U.open_directory('../DATA/DOWNLOADS/downloads_OWM_US_')
    # For each directory, get all files
    for directory in directories:
        num_forecasts = set()
        dt_set = set()
        files = U.open_directory(directory+'/')
        # Process each file
        for file in files:
            #  print(file)  # debug
            with open(os.path.join(file), 'r') as f:
                contents = f.read()
            content_dict = ast.literal_eval(contents)
            forecast_list =(content_dict['list'])
            # How many forecasts in this file?
            num_forecasts.add(len(forecast_list))
            query_date = forecast_list[0]['dt']
            dt_set.add(U.convert_from_unixtime(query_date))
        print(directory)
        pprint.pprint(dt_set)
        print('\n')
        print('In dir. {}, there are the following numbers of forecasts: {}.'.
                format(directory, num_forecasts), end='\n\n')

def check_dt_uniformity_02():
    """Report the consistence of dt-time values in each file."""
    # Get names of directories in download folder
    directories = U.open_directory('../DATA/DOWNLOADS/downloads_OWM_US_')
    # For each directory, get all files
    for directory in directories:
        print(directory)
        files = U.open_directory(directory+'/')
        # Process each file
        below15 = False # boolean: < 15 forecasts in files in this dir?
        counter_same_time_each_day = 0
        for file in files:
            #  print(file)  # debug
            with open(os.path.join(file), 'r') as f:
                contents = f.read()
            content_dict = ast.literal_eval(contents)
            forecast_list =(content_dict['list'])
            length = len(forecast_list)
            if length < 15:
                below15 = True
            times = set()
            for j in range(length):
                date = forecast_list[j]['dt']
                the_time = U.convert_from_unixtime(date).split(' ')[-1]
                times.add(the_time)
            if len(times) == 1:
                # increment counter
                counter_same_time_each_day += 1
            else:
                # report id, times
                ID = file.split('/')[-1]
                print(ID, times, sep='\n', end='\n\n')
        if below15:
            print('In dir. {}, there are {} forecasts in forecast_list.'.
                    format(directory, length))
        print('''In this directory, {} out of {} files had only a single '''
                '''time in all the dt values (= {}%).'''.
                format(counter_same_time_each_day, len(files),
                    round(100*counter_same_time_each_day/len(files), 1)))

def find_lowest_value(to_find='rain'):
    """Report cases where rain (or other) are forecast explicitly to be 0."""
    # Get names of directories in download folder
    directories = U.open_directory('../DATA/DOWNLOADS/downloads_OWM_US_')
    lowest_value= None
    # For each directory, get all files
    for directory in directories:
        files = U.open_directory(directory+'/')
        for file in files:
            with open(os.path.join(file), 'r') as f:
                contents = f.read()
            content_dict = ast.literal_eval(contents)
            forecast_list_received =(content_dict['list'])
            for forecast in forecast_list_received:
                if to_find in forecast:
                    if not lowest_value or forecast[to_find] < lowest_value:
                        lowest_value = forecast[to_find]
        print('In directory {} the lowest value of {} is {}.'.
                format(directory, to_find, lowest_value))

def find_snow_or_rain_0(to_find='rain'):
    """Report cases where rain (or other) are forecast explicitly to be 0."""
    # Get names of directories in download folder
    directories = U.open_directory('../DATA/DOWNLOADS/downloads_OWM_US_')
    # For each directory, get all files
    for directory in directories:
        files = U.open_directory(directory+'/')
        for file in files:
            with open(os.path.join(file), 'r') as f:
                contents = f.read()
            content_dict = ast.literal_eval(contents)
            forecast_list_received =(content_dict['list'])
            for forecast in forecast_list_received:
                if to_find in forecast and forecast[to_find] == 0:
                    print('In file\n    {}\n    {} = 0.'.format(file, to_find))

def find_identical_forecasts():
    """Determine how much of two forecast-sets are identical."""
    # Get names of directories in download folder
    directories = U.open_directory('../DATA/DOWNLOADS/downloads_OWM_US_')
    # For each directory, get all files
    for dir1, dir2 in zip(directories, directories[1:]):
        print(dir1, dir2, sep='\n') # debug
        files1 = U.open_directory(dir1+'/')
        files2 = U.open_directory(dir2+'/')
        forecast_dict1 = U.retrieve_data_vals(files1)
        forecast_dict2 = U.retrieve_data_vals(files2)
        same_counter = [0] * 5
        same_counter_items = ['dt', 'maxt', 'mint', 'rain', 'snow']
        keys = forecast_dict1.keys()
        for key in keys:
            if not (key in forecast_dict1 and key in forecast_dict2):
                continue
            for i in range(5):
                if forecast_dict1[key][i] == forecast_dict2[key][i]:
                    same_counter[i] += 1
        pairs = ['{}: {}/{} = {}%'.
                format(i, j, len(keys), round(100*j/len(keys)))
                    for i, j in zip(same_counter_items, same_counter)]
        pprint.pprint(pairs)
        print('\n')

def check_dt_deltas_same():
    """Report if deltas vary between consecutive dts for single location."""
    set_of_set_contents = set()
    # Get all files in a directory
    sub_dirs = glob.glob('../DATA/DOWNLOADS/downloads_OWM_US_*')
    for directory in sub_dirs:
        files = glob.glob(directory+'/*')
        forecast_dict = U.retrieve_data_vals(files)
        for key in forecast_dict:
            if key == 'query_date':
                continue
            forecast_list = forecast_dict[key]
            set_dt_deltas = set()
            for tuple1, tuple2 in zip(forecast_list, forecast_list[1:]):
                set_dt_deltas.add(int(tuple2[0])-int(tuple1[0]))
            if len(set_dt_deltas) > 1:
                print("\nScream bloody murder", set_dt_deltas, key, sep='\n')
            set_of_set_contents.update(set_dt_deltas)
        if len(set_of_set_contents) > 1: 
            print("\nAgain, Really?", set_of_set_contents, directory, sep='\n')
        else:
            print(set_of_set_contents)
