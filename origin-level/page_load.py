import requests
response = requests.get('https://www.amazon.com')
print(len(response.content))
print(response.elapsed.total_seconds())
print(len(response.content)/response.elapsed.total_seconds())
#response = requests.get('https://images-na.ssl-images-amazon.com/images/G/01/img18/events/mothersday/gateway/md_gw_DesktopShoveler_under30_200x200._CB498563694_.jpg')
#print(len(response.content))
#print(response.elapsed.total_seconds())
#print(len(response.content)/response.elapsed.total_seconds())


