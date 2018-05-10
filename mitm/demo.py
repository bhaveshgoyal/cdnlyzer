import subprocess

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


def get_base(url):
	with open("top200", "r") as fp:
		names = fp.readlines()
	names = [each.strip().split(',')[1] for each in names]
	for each in names:
		if each in url:
			return each
	return ""

def print_res_analysis():
	global img_size
	global css_size
	global js_size
	global total_size
	global base_req

	print ("Total bytes", total_size)
	print ("Image bytes", img_size)
	print ("CSS bytes", css_size)
	print ("JS bytes", js_size)

	with open("out/" + base_req + "_res", "w+") as fp:
		fp.write("Total:" + str(total_size) + "\n")
		fp.write("Image:" + str(img_size) + "\n")
		fp.write("CSS:" + str(css_size) + "\n")
		fp.write("JS:" + str(js_size) + "\n")

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
	global base_req

	total_req += 1
	if base_req == "":
		base_req = get_base(flow.request.pretty_host)
	
	if base_req != "":
		with open("out/" + base_req + "_req", "a+") as fp:
			fp.write(flow.request.url + "," + base_req + "\n")
	

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
