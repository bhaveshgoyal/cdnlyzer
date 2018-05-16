#!/usr/bin/env python
import sys
import urllib.request
import json
from geopy.distance import geodesic

# API to get distance in miles between two ip locations
# @location1, location2 - tupe containing latitude and longitude
# returns distance in miles
def distance_latitudes(location1, location2):
    return geodesic(location1, location2).miles

# API to get location information from ip address
# @address_ - ip address
# return tuples containing latitude and longitude
def get_info(address_):
    print("************************************************")

    api = "http://freegeoip.net/json/" + address_
    try:
        result = urllib.request.urlopen(api).read()
        result = str(result) 
        result = result[2:len(result)-3]
        result = json.loads(result)
    except:
        print("Could not find: ", address_)
        return None

    print(address_)
    print("IP: ", result["ip"])
    print("Country Name: ", result["country_name"])
    print("Country Code: ", result["country_code"])
    print("Region Name: ", result["region_name"])
    print("Region Code: ", result["region_code"])
    print("City: ", result["city"])
    print("Zip Code: ", result["zip_code"])
    print("Latitude: ", result["latitude"])
    print("Longitude: ", result["longitude"])
    print("Location link: " + "http://www.openstreetmap.org/#map=11/" + str(result["latitude"]) +"/" + str(result["longitude"]))
    return (result["latitude"], result["longitude"])

if __name__ == "__main__":
        address = "130.245.192.6" 
        lat1 = get_info(address)
        print("************************************************")
        address = "176.32.103.205"
	# 13.33.73.149" # "163.53.78.128" # "172.229.211.34" 
        lat2 = get_info(address)
        print("************************************************")
        print("Distance between them is: ",distance_latitudes(lat1, lat2))

