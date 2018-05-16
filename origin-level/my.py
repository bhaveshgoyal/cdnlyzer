import pyping

def myping(url):
    print("MYPY:",url)
    r = pyping.ping(url)
    print(r.avg_rtt)
    return r.avg_rtt
