import csv
from main import leads_main

csv_filename = 'test.csv'

with open(csv_filename) as f:
    reader = csv.DictReader(f)

    for row in reader:
        print("input \n")
        print(row['start'],row['end'],row['tf'],row['cid'])
        print("Output \n")
        x=leads_main(row['start'],row['end'],row['tf'],row['cid'])
        print(x)
        print('\n')