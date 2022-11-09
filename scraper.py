import requests
from selenium import webdriver

username = password = "Digicel"
url = "http://192.168.100.1/"
driver = webdriver.Chrome("chromedriver")
driver.get(url)

# find username/email field and send the username itself to the input field
driver.find_element_by_id("txt_Username").send_keys(username)
# find password input field and insert password as well
driver.find_element_by_id("txt_Password").send_keys(password)
# click login button
driver.find_element_by_name("Submit").click()
driver.find_element_by_name("mainli_pcp").click()

driver.close()

