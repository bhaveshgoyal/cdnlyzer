import glob
path = 'out/'
w_fp = open("cdn_bytes.csv", "w")
tup2wr = ("Site Name", "Total Bytes", "Image Bytes", "Image Percentage", "CSS Bytes", "CSS Percentage", "JS Bytes", "JS Percentage", "Total Percentage")
tup2wrstr = ','.join(map(str, tup2wr))
w_fp.write(tup2wrstr)
w_fp.write("\n")

total_bytes = 0
total_img = 0
total_js = 0
total_css = 0
for filename in glob.glob('*_res'):
	print(str(filename))
        with open(filename, "r") as fp:
            sites = fp.readlines()
            sites = [each.rstrip().lstrip().split(':')[1] for each in sites]
	    tup2wr = (str(filename), str(sites[0]), str(sites[1]), float(sites[1])/float(sites[0]), str(sites[2]), float(sites[2])/float(sites[0]), str(sites[3]), float(sites[3])/float(sites[0]), (float(sites[1])+float(sites[3])+float(sites[2]))/float(sites[0]))
            total_bytes += float(sites[0])
            total_img += float(sites[1])
            total_css += float(sites[2])
            total_js += float(sites[3])
            tup2wrstr = ','.join(map(str, tup2wr))
            w_fp.write(tup2wrstr)
            w_fp.write("\n")
tup2wr = ("",total_bytes,total_img,total_img/total_bytes,total_css,total_css/total_bytes,total_js,total_js/total_bytes,(total_css+total_js+total_img)/total_bytes)
tup2wrstr = ','.join(map(str, tup2wr))
w_fp.write(tup2wrstr)
w_fp.write("\n")

