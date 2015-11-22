import requests
import time
import csv

bikeID = 1

with open('position.csv', 'rb') as poz:
    reader = csv.reader(poz)
    for row in reader:
        requests.post("http://52.32.72.73:8000/location/", json={"bike_id": bikeID, "latitude": row[0], "longitude": row[1]})
        time.sleep(30)
