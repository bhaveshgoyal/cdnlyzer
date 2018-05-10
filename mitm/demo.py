img_extensions = [".jpeg", ".jpg", ".gif", ".png"]

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

total_size = 0
img_size = 0
css_size = 0
js_size = 0

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

def get_base(url):
	print ("Checking " + url)
	with open("names", "r") as fp:
		names = fp.readlines()
	names = [each.rstrip()[:-1].lstrip() for each in names]
	for each in names:
		mapping = eval(each)
		if mapping[0] in url:
			return mapping[0]
	return ""

def check_dynamic(url, base):
	#RAHUL's API
	return True

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

	print ("Percentage images", (float(img_req)/total_req)*100)
	if img_req > 0:
		print ("Percentage static CDN images", (float(img_static_req)/img_req)*100)
		print ("Percentage dynamic CDN images", (float(img_dyn_req)/img_req)*100)
	print ("Percentage css", (float(css_req)/total_req)*100)
	if css_req > 0:
		print ("Percentage static CDN css", (float(css_static_req)/css_req)*100)
		print ("Percentage dynamic CDN css", (float(css_dyn_req)/css_req)*100)
	print ("Percentage js", (float(js_req)/total_req)*100)
	if js_req > 0:
		print ("Percentage static CDN js", (float(js_static_req)/js_req)*100)
		print ("Percentage dynamic CDN js", (float(js_dyn_req)/js_req)*100)
	print (base_req)

def print_res_analysis():
	global img_size
	global css_size
	global js_size
	global total_size
	
	print ("Total bytes", total_size)
	print ("Image bytes", img_size)
	print ("CSS bytes", css_size)
	print ("JS bytes", js_size)

def request(flow):
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

	
	total_req += 1

	if check_image(flow.request.path):
		img_req += 1
		if check_static(flow.request.pretty_host):
			img_static_req += 1
		elif check_dynamic(flow.request.pretty_host, base_req):
			img_dyn_req += 1

	if check_js(flow.request.path):
		js_req += 1
		if check_static(flow.request.pretty_host):
			js_static_req += 1
		elif check_dynamic(flow.request.pretty_host, base_req):
			js_dyn_req += 1

	if check_css(flow.request.path):
		css_req += 1
		if check_static(flow.request.pretty_host):
			css_static_req += 1
		elif check_dynamic(flow.request.pretty_host, base_req):
			css_dyn_req += 1
	
	print_req_analysis()

def response(flow):
	global img_size
	global css_size
	global js_size
	global total_size

	headers = dict(flow.response.headers)
	try:
		if 'image' in headers['content-type']:
			if 'content-length' in headers:
				img_size += int(headers['content-length'])
			else:
				img_size += len(flow.response.content)
		if 'css' in headers['content-type']:
			if 'content-length' in headers:
				css_size += int(headers['content-length'])
			else:
				css_size += len(flow.response.content)
		if 'javascript' in headers['content-type']:
			if 'content-length' in headers:
				js_size += int(headers['content-length'])
			else:
				js_size += len(flow.response.content)
		
		if 'content-length' in headers:
			total_size += int(headers['content-length'])
		else:
			total_size += len(flow.response.content)
	except:
		pass
	print_res_analysis()
