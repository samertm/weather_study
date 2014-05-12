#!/Users/ginaschmalzle/v_env3/bin/python
import retrieve
import json

exact_date=20140422 
# Get Forecast data from retrieve.py
x = retrieve.get_single_date_data_from_db(exact_date)

#rec_x = {'type': 'Feature', 'properties': x[key] for key in x }
#print(rec_x)

#with open ('../OUTPUT/temp.json', 'w') as f:
        #f.write(json.dumps({str(key):x[key] for key in x}))
#       f.write(json.dumps({'type': 'Feature', 'properties': {x[key]}}) for key in x)

#, 'geometry':{'type':'Point', 'coordinates':list(key)}} for key in x}))
