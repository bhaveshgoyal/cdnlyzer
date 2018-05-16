import glob
path = 'out/'
for filename in glob.glob('*_res'):
	print(str(filename))
        with open(filename, "r") as fp:
            sites = fp.readlines()
            sites = [each.rstrip().lstrip().split(':')[1] for each in sites]
            for site in sites:
            	print(site)

