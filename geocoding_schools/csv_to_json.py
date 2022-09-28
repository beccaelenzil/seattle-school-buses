import csv

with open('./cleaned_school_list.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

print(csv_reader)