# scrape bus data - active cron job

import urllib.request as urllib
import pandas as pd
import os
import datetime

now = datetime.datetime.now()


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'time_data.pk1')


df = pd.read_pickle(filename)


df2 = pd.DataFrame([[now.month,now.day,now.hour,now.minute]], columns=['Month', 'Day','Hour','Minute'])

df3 = df.append(df2,ignore_index=True)
df3.to_pickle(filename)

#/Users/becca.elenzil/Documents/personal_projects/scrape_bus_data.py
#/Users/becca.elenzil/GitHub/seattle-school-buses/scraping_bus_data/scrape_bus_data.py
