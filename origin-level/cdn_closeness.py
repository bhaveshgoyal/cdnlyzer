#!/usr/bin/env python
import sys
import urllib.request
from geopy.distance import geodesic
import re
import json
from urllib.request import urlopen
import dns.resolver
import trc2
import my

# API to lookup hostname to ip
# @ hostname - e.g. google.com
# returns ip of hostname 
def hostname_to_ip(hostname):
    # dns resolver
    resolver = dns.resolver.Resolver() 
    resolver.nameservers = ['130.245.255.4']
    answer = resolver.query(hostname)
    return (answer[0], answer.rrset.ttl)

# API to get distance in miles between two ip locations
# @location1, location2 - tupe containing latitude and longitude
# returns distance in miles
def distance_latitudes(location1, location2):
    return geodesic(location1, location2).miles

# API to get location information from ip address
# @address_ - ip address, @to_print - print flag
# return tuples containing latitude and longitude
def get_info(address_, to_print):

    api = "http://freegeoip.net/json/" + address_
    try:
        result = urllib.request.urlopen(api).read()
        result = str(result)
        result = result[2:len(result)-3]
        result = json.loads(result)
    except:
        print("Could not find: ", address_)
        return None
    if to_print:
        print("************************************************")
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

# API to get my current location details
# @to_print - print flag
# returns data
def my_curr_loc(to_print):
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    IP=data['ip']
    org=data['org']
    city = data['city']
    country=data['country']
    region=data['region']
    if to_print:
        print( 'Your IP detail\n ')
        print( 'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}'.format(org,region,country,city,IP))
    return data

# API to get traceroute details
# @address - host address
def ping_traceroute(address):
       print("IP:", address)
       res = trc2.traceroute_main(address) 
       return res

# API to get ping response time
# @address - host address
def ping_response(url):
       return my.myping(url)

if __name__ == "__main__":
        with open("top200", "r") as fp:
            sites = fp.readlines()
        w_fp = open("cdn_closeness.csv", "w")
        
        my_ip = my_curr_loc(False)['ip']
        my_latlong = get_info(my_ip, False)
        tup2wr = ("Curr IP", "Server IP", "CDN IP", "Trc Server", "Trc CDN", "Trc Diff.", "Ping Server", "Ping CDN", "Ping Diff", "CDN?", "Hops Server", "Hops CDN", "Distance Server", "Distance CDN", "Distance Diff.", "CDN TTL")
        tup2wrstr = ','.join(map(str, tup2wr))
        print("HERE:33", tup2wrstr)
        w_fp.write(tup2wrstr)
        w_fp.write("\n")
        sites = [each.rstrip().lstrip().split(',')[1] for each in sites]
        for site in sites:
            try:
                server_addr = str(hostname_to_ip(site)[0])
                cdn_addr_ttl = hostname_to_ip("www." + site)
                cdn_addr    = str(cdn_addr_ttl[0])
                cdn_ttl =  str(cdn_addr_ttl[1])
                print(server_addr)
                print(cdn_addr)
                ping_and_traceroute_server = ping_traceroute(server_addr)
                ping_and_traceroute_cdn = ping_traceroute(cdn_addr)
                ping_server_time = ping_and_traceroute_server[0]
                ping_cdn_time = ping_and_traceroute_cdn[0]
                server_hops = ping_and_traceroute_server[1] 
                cdn_hops =  ping_and_traceroute_cdn[1]
                server_latlon = get_info(server_addr, False)
                server_distance = distance_latitudes(my_latlong, server_latlon)
                cdn_latlon = get_info(cdn_addr, False)
                cdn_distance = distance_latitudes(my_latlong, cdn_latlon)
                ping_diff = ping_server_time - ping_cdn_time
                distance_diff = server_distance - cdn_distance
                p_ser = ping_response(site)
                p_cdn = ping_response("www." + site)
                p_diff = float(p_ser) - float(p_cdn)
                is_cdn = "No"
                if float(p_diff) > float(-1.0):
                    is_cdn = "Yes"
                    
                tup2wr = (my_ip, server_addr, cdn_addr, ping_server_time, ping_cdn_time, ping_diff, p_ser, p_cdn, p_diff, is_cdn, server_hops, cdn_hops, server_distance, cdn_distance, distance_diff, cdn_ttl)
                tup2wrstr = ','.join(map(str, tup2wr))
                w_fp.write(tup2wrstr)
                w_fp.write("\n")
            except:
                print("AN ERROR OCCURED")
                pass
        w_fp.close() 
        '''address = "104.254.66.16"
        lat1 = get_info(address)
        print("************************************************")
        address = "123.125.116.16"
        # 13.33.73.149" # "163.53.78.128" # "172.229.211.34" 
        lat2 = get_info(address)
        print("************************************************")
        print("Distance between them is: ",distance_latitudes(lat1, lat2))'''

