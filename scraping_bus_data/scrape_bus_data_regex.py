# import libraries
from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import os
#import numpy as np
import pandas as pd
from datascience import *
now = datetime.datetime.now()

# scrape from web
late_busses = 'https://www.seattleschools.org/departments/transportation/latebus'
page = urllib.urlopen(late_busses)
soup = BeautifulSoup(page, "html.parser")

# find the list of late buses using regex
running_late_bus_pattern = re.compile("Route (\d+) ([A-Za-z]+) ([A-Za-z]+) is running (\d+) ([A-Za-z]+) late")

paragraphs = []
for paragraph in soup.find_all('p'):
    paragraph = str(paragraph)
    if running_late_bus_pattern.search(paragraph):
        bus_list = paragraph

# find today's date using regex
date_text_pattern = re.compile("([A-Z][a-z]+) (\d+)[a-z]+, (\d\d\d\d)")

for header in soup.find_all('h3'):
    header = str(header)
    if date_text_pattern.search(header):
        date_text = header

# get today's date from match object
date_match = date_text_pattern.search(date_text)
the_month = date_match.group(1)
the_day = date_match.group(2)
the_year = date_match.group(3)

# make the bus list readable, so we can use regex
bus_list = str(bus_list)
bus_list = bus_list.strip('<p>')
bus_list = bus_list.strip('</p>')
bus_list = bus_list.strip('is running')
bus_list_array = bus_list.split("<br/>")
print(bus_list_array)

# create bus list arrays using regex
bus_number_list = [0]
school_list = [0]
to_from_list = [0]
time_list = [0]
unit_list = [0]
bus_date_list = [0]
data_collect_date_list = [0]
data_collect_time_list = [0]

for list_item in bus_list_array:
    # use regex to parse pattern
    match = running_late_bus_pattern.search(list_item)

    # put values in arrays
    bus_number_list.append(match.group(1))
    to_from_list.append(match.group(2))
    school_list.append(match.group(3))
    time_list.append(match.group(4))
    unit_list.append(match.group(5))

    # put date in arrays
    bus_date_list.append([the_month, the_day, the_year])

    # today's date as a string
    data_collect_date_list.append([now.month, now.day, now.year])
    data_collect_time_list.append([now.hour, now.minute, now.second])

# file organization

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'current_bus_data.pk1')
filename_csv = os.path.join(dirname, 'current_bus_data.csv')

df = pd.read_pickle(filename)

# put data in df
BusDataSet = list(zip(bus_date_list, bus_number_list,school_list, to_from_list, time_list, unit_list, data_collect_date_list, data_collect_time_list))

df = pd.read_pickle(filename)

df2 = pd.DataFrame(data = BusDataSet, columns=['Bus Date [M,D,Y]',
                                              'Bus Number','School',
                                              'To/From','Time','Unit','Collect Date', 'Collect Time'])
#update old df

df3 = df.append(df2,ignore_index=True)

# write new df to pickle
df3.to_pickle(filename)

# show the new data
print(df2)
