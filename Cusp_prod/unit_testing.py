import csv
from main import leads_main

csv_filename = 'test.csv'

with open(csv_filename) as f:
    reader = csv.DictReader(f)
    case=1
    for row in reader:
        print("The case number is {0} \n".format(case))
        print("Input \n")
        print(row['start'],row['end'],row['tf'],row['cid'] ,"\n")
        print("Output \n")
        x=leads_main(row['start'],row['end'],row['tf'],row['cid'])
        print(x)
        print('\n')
        case=case+1