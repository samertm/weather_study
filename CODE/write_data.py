#!/Users/ginaschmalzle/v_env3/bin/python

exact_date = 20140422

with open('x.py', "w") as out_file:

f = open('x.py', 'w')
print f.write(retrieve.get_single_date_data_from_db(exact_date))
