import socket
import time
import dns.resolver
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def get_cdn(query):
    print "Querying: " + query
    for rdata in resolver.query(query):
#        print rdata
        try:
            hostname = socket.gethostbyaddr(str(rdata))[0]
        except:
            print "NSLOOKUP Failed"
            return
        names = []
        with open("names", "r") as fp:
            names = fp.readlines()
	    names = [each.rstrip()[:-1].lstrip() for each in names]
        for each in names:
		    mapping = eval(each)
		    if mapping[0] in hostname:
			    print mapping[1]

def parse_cdn(query):
    idx = 0
    driver = webdriver.Chrome()
    try:
        for site in query:
            buff = site.rstrip() + " -> "
            url = 'https://www.cdnplanet.com/tools/cdnfinder/#site:https://' + site
            driver.get(url)
            domComplete = driver.execute_script("return window.performance.timing.domComplete")
            time.sleep(20)
            table = driver.find_element_by_xpath('//table[1]')
            resp = table.text
            for line in resp.split('\n'):
                if any(each == 'www.' + site for each in line.split(' ')):
                    buff += str(line.split('www.' + site)[1].encode('utf-8').lstrip())
            print buff
            idx += 1
        driver.quit()
    except Exception as e:
        print "Skipping " + query[idx]
        driver.quit()
        idx += 1
        parse_cdn(query[idx:])
    return ""

if __name__ == "__main__":
    # Set the DNS Server
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['130.245.255.4']
    with open("top200", "r") as fp:
        sites = fp.readlines()
    sites = [each.rstrip().lstrip().split(',')[1] for each in sites]
    parse_cdn(sites)
