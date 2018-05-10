from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import subprocess, signal
import os
import time
from urlparse import urlparse

img_extensions = [".jpeg", ".jpg", ".gif", ".png", ".svg"]

total_req = 0

img_req = 0
img_static_req = 0
img_dyn_req = 0

js_req = 0
js_static_req = 0
js_dyn_req = 0

css_req = 0
css_static_req = 0
css_dyn_req = 0

base_req = ""

def check_image(url):
	return any(ext in url for ext in img_extensions)

def check_js(url):
	return ".js" in url

def check_css(url):
	return ".css" in url

def check_static(url):
	with open("names", "r") as fp:
		names = fp.readlines()
	names = [each.rstrip()[:-1].lstrip() for each in names]
	for each in names:
		mapping = eval(each)
		if mapping[0] in url:
			return True
	return False

def check_dynamic(url):
	global base_req

	o = urlparse(url)
	host = o.hostname
	try:
		print "PING: " + host
		print "PING: " +  base_req
		op = subprocess.check_output(["ping", host, "-c", "2"])
		time1 =  float(op.split('\n')[-2].split('=')[1].strip().split('/')[1])
		op2 = subprocess.check_output(["ping",base_req,"-c","2"])
		time2 =  float(op.split('\n')[-2].split('=')[1].strip().split('/')[1])
		if time1 <= time2:
			return True
		return False
	except:
		pass
	return False

def print_req_analysis():
	global total_req
	
	global img_req
	global img_static_req
	global img_dyn_req

	global js_req
	global js_static_req
	global js_dyn_req

	global css_req
	global css_static_req
	global css_dyn_req

	global base_req
	final_buff = base_req

	final_buff += "," + str((float(img_req)/total_req)*100)
	if img_req > 0:
		final_buff += "," + str((float(img_static_req)/img_req)*100)
		final_buff += "," + str((float(img_dyn_req)/img_req)*100)
	else:
		final_buff += ',,'
	final_buff += "," + str((float(css_req)/total_req)*100)
	if css_req > 0:
		final_buff += "," + str((float(css_static_req)/css_req)*100)
		final_buff += "," + str((float(css_dyn_req)/css_req)*100)
	else:
		final_buff += ',,'
	final_buff += "," + str((float(js_req)/total_req)*100)
	if js_req > 0:
		final_buff += "," + str((float(js_static_req)/js_req)*100)
		final_buff += "," + str((float(js_dyn_req)/js_req)*100)
	else:
		final_buff += ',,'
	
	fp = open("out/final_res", "a+")
	fp.write(final_buff + "\n")
	fp.close()
	print (base_req)


def load_page(source):
	
	prox = Proxy()
	prox.proxy_type = ProxyType.MANUAL
	prox.http_proxy = "127.0.0.1:9090"
	prox.socks_proxy = "127.0.0.1:9090"
	prox.ssl_proxy = "127.0.0.1:9090"

	capabilities = webdriver.DesiredCapabilities.CHROME
	prox.add_to_capabilities(capabilities)

	driver = webdriver.Chrome(desired_capabilities=capabilities)
	driver.get(source)

	navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
	responseStart = driver.execute_script("return window.performance.timing.responseStart")
	domComplete = driver.execute_script("return window.performance.timing.domComplete")

	backendPerformance = responseStart - navigationStart
	frontendPerformance = domComplete - responseStart

	print "Back End: %s" % backendPerformance
	print "Front End: %s" % frontendPerformance

	driver.quit()

def parse_req(site):
	global total_req
	
	global img_req
	global img_static_req
	global img_dyn_req

	global js_req
	global js_static_req
	global js_dyn_req

	global css_req
	global css_static_req
	global css_dyn_req

	global base_req
	
	reqs = []
	with open("out/" + site + "_req", "r") as fp:
		reqs = fp.readlines()
	
	reqs = [req.strip() for req in reqs]
	
	total_req = 0
	img_req = 0
	img_static_req = 0
	img_dyn_req = 0
	js_req = 0
	js_static_req = 0
	js_dyn_req = 0
	css_req = 0
	css_static_req = 0
	css_dyn_req = 0
	base_req = ""

	base_req = reqs[0].split(',')[1]
	for each in reqs:
		path = each.split(',')[0]
		total_req += 1
		if check_image(path):
			img_req += 1
			if check_static(path):
				img_static_req += 1
			elif check_dynamic(path):
				img_dyn_req += 1

		if check_js(path):
			js_req += 1
			if check_static(path):
				js_static_req += 1
			elif check_dynamic(path):
				js_dyn_req += 1

		if check_css(path):
			css_req += 1
			if check_static(path):
				css_static_req += 1
			elif check_dynamic(path):
				css_dyn_req += 1
	
	print_req_analysis()

if __name__ == "__main__":
	
	headers = '"Site, Percentage images", "static imgs", "dynamic imgs", "Percentage css", "static css", "dynamic css", "Percentage js", "static js", "dynamic js"'

	final_out = open("out/final_res", "w+")
	final_out.write(headers + "\n")
	final_out.close()
	
	sites = ""
	with open('top200', 'r') as fp:
		sites = fp.readlines()
	sites = [each.strip().split(',')[1] for each in sites]
	for site in sites:
		mitm = subprocess.Popen(['mitmdump', '-p', '9090', '-s', 'demo.py'])
		time.sleep(3)
		load_page("http://" + site)
		p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)   
		out, err = p.communicate()
		for line in out.splitlines():
			if 'mitmdump' in line:
				pid = int(line.split(None, 1)[0])
				os.kill(pid, signal.SIGKILL)
		parse_req(site)
