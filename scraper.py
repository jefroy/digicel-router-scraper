import logging

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

username = password = "Digicel"
url = "http://192.168.100.1/"
tableId = "PcpConfigList_tbl"
timeout = 7
currSettings = nextSettings = None
internalPortToCheck = 25565

driver = webdriver.Chrome("chromedriver")
driver.get(url)

# find username/email field and send the username itself to the input field
driver.find_element_by_id("txt_Username").send_keys(username)
# find password input field and insert password as well
driver.find_element_by_id("txt_Password").send_keys(password)
# click login button
driver.find_element_by_name("Submit").click()
driver.find_element_by_name("mainli_pcp").click()

driver.implicitly_wait(10)
time.sleep(10)

try:
    # https://stackoverflow.com/questions/38363643/python-selenium-get-inside-a-document
    # element = WebDriverWait(driver, 6).until(
    #     EC.presence_of_element_located((By.ID, "PcpConfigList_tbl"))
    # )
    # element_present = EC.presence_of_element_located((By.ID, tableId))
    # WebDriverWait(driver, timeout).until(element_present)
    # the above wont work cus the page is already loaded, but the driver hasnt updated
    iframe = driver.find_element_by_id("frameContent")
    driver.switch_to.frame(iframe)
    page_source = driver.page_source  # on the pcp forward rules page

    soup = BeautifulSoup(page_source, 'lxml')
    table = soup.find("table", {"id": "PcpConfigList_tbl"})
    for row in table.findAll("tr"):
        if len(row.contents) > 7:
            externalIP = row.contents[2].text
            externalPort = row.contents[3].text
            internalPort = row.contents[4].text
            resultCode = row.contents[7].text
            if internalPort == internalPortToCheck:
                if currSettings is None:
                    currSettings = {
                        "externalIP": externalIP,
                        "externalPort": externalPort,
                        "resultCode": resultCode
                    }
                else:
                    nextSettings = {
                        "externalIP": externalIP,
                        "externalPort": externalPort,
                        "resultCode": resultCode
                    }
                if currSettings["externalIP"] != nextSettings["externalIP"] or currSettings["externalPort"] != \
                        nextSettings["externalPort"]:
                    currSettings = nextSettings
                    # send update to chate
    print(currSettings)
    print(nextSettings)
    driver.close()
    quit(0)
except Exception as e:
    print("error occurred trying to soup")
    logging.critical(e, exc_info=True)
    driver.close()
    quit(1)
