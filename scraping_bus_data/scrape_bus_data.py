# scrape bus data - active cron job

from bs4 import BeautifulSoup
import urllib.request as urllib
import pandas as pd
import os
import datetime

now = datetime.datetime.now()
 
# web scraping
late_busses = 'https://www.seattleschools.org/departments/transportation/latebus'
page = urllib.urlopen(late_busses)
soup = BeautifulSoup(page, "html.parser")

# get bus list and date from html
t = soup.find_all('p')
print(t)
[a, bus_list, b] = soup.find_all('p')
[a,date] = soup.find_all('h3')

# parse date into month, day, year
date = str(date)

date = date.strip('</h3>')
date = date.strip(',')
date = date.split(" ")
months = ['January','February','March','April','May','June',
          'July','August','September','October','November','December']

i = 0
while date[i] not in months:
    i = i+1

the_month = date[i]
the_day = date[i+1]
the_year = date[i+2]

if the_day[0:2].isdigit() == True:
    the_day = the_day[0:2]
else:
    the_day = the_day[0]

# parse bus list
bus_list = str(bus_list)
bus_list = bus_list.strip('<p>')
bus_list = bus_list.strip('</p>')
bus_list = bus_list.strip('is running')
bus_list_array = bus_list.split("<br/>")

new_bus_array = []

for string in bus_list_array:
    string = string.split(' ')
    new_bus_array.append(string)

bus_number_list = []
school_list = []
to_from_list = []
time_list = []
unit_list = []
month_list = []
day_list = []
year_list = []
today_month = []
today_day = []
today_year = []
today_hour = []
today_minute = []

print(new_bus_array)


for list_item in new_bus_array:
    bus_number_list.append(int(list_item[1]))
    to_from_list.append(list_item[2])

    #schools
    if list_item[4] == "is":
        is_index = 4
        school_list.append(list_item[3])
    elif list_item[5] == "is":
        is_index = 5
        school_list.append(list_item[3]+" "+list_item[4])
    elif list_item[6] == "is":
        is_index = 6
        school_list.append(list_item[3]+" "+list_item[4]+" "+list_item[5])

    #time
    if list_item[is_index+3] == 'minutes':
        time_list.append(int(list_item[is_index+2]))
    elif list_item[is_index+3] == 'hours' or list_item[is_index+3] == 'hour' :
        time_list.append(60*int(list_item[is_index+2]))

    unit_list.append("minutes")
    month_list.append(the_month)
    day_list.append(the_day)
    year_list.append(the_year)
    today_month.append(now.month)
    today_day.append(now.day)
    today_year.append(now.year)
    today_hour.append(now.hour)
    today_minute.append(now.minute)


# write to data frame and save
BusDataSet = list(zip(month_list,day_list,year_list,bus_number_list,school_list,
                      to_from_list, time_list, unit_list,today_month,today_day, today_year, today_hour, today_minute))

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'bus_data.pk1')
filename_csv = os.path.join(dirname, 'bus_data.csv')

df = pd.read_pickle(filename)
num_rows = df['Month'].count()



df2 = pd.DataFrame(data = BusDataSet, columns=['Month', 'Day','Year',
                                              'Bus Number','School',
                                                'To/From','Time','Unit','Data Taken Month','Data Taken Day',
                                               'Data Taken Year','Data Taken Hour','Data Taken Minute'])
if df['Day'][num_rows-1] == df2['Day'][0] and df['Data Taken Hour'][num_rows-1] >= 15:
    print("old data")
else:
    df3 = df.append(df2,ignore_index=True)
    df3.to_pickle(filename)
    df3.to_csv(filename_csv)

print("day list:", day_list)

#/Users/becca.elenzil/Documents/personal_projects/scrape_bus_data.py
#/Users/becca.elenzil/GitHub/seattle-school-buses/scraping_bus_data/scrape_bus_data.py
