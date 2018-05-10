import subprocess

def check_dynamic(url, base):
	op = subprocess.check_output(["ping",url,"-c","5"])
	time1 =  float(op.split('\n')[-2].split('=')[1].strip().split('/')[1])
	print time1
	op2 = subprocess.check_output(["ping",base,"-c","5"])
	time2 =  float(op2.split('\n')[-2].split('=')[1].strip().split('/')[1])
	print time2
	if time2 - time1 > time1/4:
		return True
	return False

if __name__ != "":
	print check_dynamic('www.amazon.com', 'amazon.com')
