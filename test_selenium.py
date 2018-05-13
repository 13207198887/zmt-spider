from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("https://www.baidu.com")
elem = driver.find_element_by_id("kw")
elem.send_keys("哈哈")
elem.send_keys(Keys.RETURN)
#driver.close()
