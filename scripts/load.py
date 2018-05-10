from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

source = "https://amazon.com"

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
