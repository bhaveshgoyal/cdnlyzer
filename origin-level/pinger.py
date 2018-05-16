#!/usr/bin/env python

import logging, sys

FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

echo = logging.info

from pyping import ping, Ping
from time import sleep

host = sys.argv[1]

history = {60:[], 600:[], 3600:[]}
losts = {}
dns_errors = {}
timings = {}

losting = 0
dns_error = 0
c = 0

from prettytable import PrettyTable

for k, v  in history.items():
	timings[k] = {"tmin":0, "tmax":0, "avg":0}
	losts[k] = []
	dns_errors[k] = []
	
print_cnt = 60
j = 0
	
while True: 
	j += 1
	
	if j == 2:
#		try:
		x = PrettyTable(field_names = ["period", "avg", "min", "max", "d", "lost", "nodns"])
		for k, v  in timings.items():
			x.add_row([k, v["avg"], v["tmin"], v["tmax"], v["ch_v"], v["losts"], v["dns_errors"]])
		echo("\n" + str(x))
#		except:
#			echo(str(timings))

	if j == print_cnt:
		j = 0

	sleep(max(0.1, 0.5 - c/1000.0))
	for k, v  in history.items():
		if len(v) >= k: history[k] = v[1:]
	for k, v  in losts.items():
		if len(v) >= k: losts[k] = v[1:]
	for k, v  in dns_errors.items():
		if len(v) >= k: dns_errors[k] = v[1:]

	try:
		r = ping(host, count=1, timeout=3000, udp=False)
	except Exception, e:
		#print ">%s<" % e
		if str(e) == "unknown_host":
			if dns_error == 0:
				echo("dns_error")
				dns_error = 1
			for k  in history.keys():
				dns_errors[k].append(0)
			continue
	
	if r.packet_lost > 0:
		if losting == 0:
			echo("losting")
			losting = 1
		for k  in history.keys():
			losts[k].append(1)
		continue
	else:
		if losting == 1:
			echo("losting done")
		losting = 0
		
	for k  in history.keys():
		losts[k].append(0)
		dns_errors[k].append(0)

	if dns_error == 1:
		echo("dns_error done")
	dns_error = 0
	
	c = float(r.avg_rtt)

	
	
	for k, v  in history.items():
		v.append(c)
		t = timings[k]
		t["avg"] = 0
		t["tmax"] = c
		t["tmin"] = c
		t["ch_v"] = 0
		li = None
		for i in v:
			t["avg"]  += i
			t["tmax"] = max(t["tmax"], i)
			t["tmin"] = min(t["tmin"], i)
			if li != None:
				t["ch_v"] += abs(i - li)
			else:
				li = i
		t["losts"] = 0
		t["dns_errors"] = 0
		for i in losts[k]:
			t["losts"] += i
		for i in dns_errors[k]:
			t["dns_errors"] += i
		t["avg"] /= float(len(v))
		t["ch_v"] /= float(len(v))

		t["avg"] = round(t["avg"], 2)
		t["ch_v"] = round(t["ch_v"], 2)
		t["tmax"] = round(t["tmax"], 2)
		t["tmin"] = round(t["tmin"], 2)

		
		

"""
[date]: ping OK
[date]: ping Error
"""
