import names 
import pandas as pd    
import numpy as np

names_dict = dict()
names_dict['gender'] = []
names_dict['first_name'] = []
names_dict['last_name'] = []

for i in range(100):
    if np.random.randint(0,100)%2==0:
        names_dict['gender'].append('female')
        fname,lname = names.get_first_name(gender='female'),names.get_last_name()
        # while fname not in names_dict['first_name'] and lname not in names_dict['last_name']:
        names_dict['first_name'].append(fname)
        names_dict['last_name'].append(lname)
    else:
        names_dict['gender'].append('male')
        fname,lname = names.get_first_name(gender='male'),names.get_last_name()
        # while fname not in names_dict['first_name'] and lname not in names_dict['last_name']:
        names_dict['first_name'].append(fname)
        names_dict['last_name'].append(lname)
names_df = pd.DataFrame(names_dict)
names_df.to_csv('names.csv')