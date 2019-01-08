# scrape bus data - active cron job

import urllib.request as urllib
import pandas as pd
import os
import datetime

now = datetime.datetime.now()


# write to data frame and save
#DataSet = list(zip(now.month, now.day, now.hour, now.minute))

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'time_data.pk1')

try:
    df = pd.read_pickle(filename)
except:
    pass

df2 = pd.DataFrame([[now.month, now.day, now.hour, now.minute]], columns=['Month','Day', 'Hour', 'Minute'])

try:
    df3 = df.append(df2,ignore_index=True)
except:
    df3 = df2

df3.to_pickle(filename)

print(df3)

#print("day list:", day_list)

#/Users/becca.elenzil/Documents/personal_projects/scrape_bus_data.py
#/Users/becca.elenzil/GitHub/seattle-school-buses/scraping_bus_data/scrape_bus_data.py
