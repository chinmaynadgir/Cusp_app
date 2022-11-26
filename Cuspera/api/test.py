import requests
import csv
headers = {"Content-Type": "application/json; charset=utf-8"}

data = {"begin":"2022-06-21","end":"2022-06-23"}

re = requests.post("http://127.0.0.1:5000/getData",json=data)

with open("out.csv","w",newline="") as f:
    writer = csv.writer(f)
    for line in re.iter_lines():
        writer.writerow(line.decode('utf-8').split(','))