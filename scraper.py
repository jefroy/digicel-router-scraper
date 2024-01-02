import logging

from selenium import webdriver
from bs4 import BeautifulSoup

from utils import *

from dotenv import load_dotenv
import os
import json

username = "Digicel"
password = "Digicel"
url = "http://192.168.100.1/"
tableId = "PcpConfigList_tbl"
interval = 15 * 60  # run entire process every 15 mins :)
# interval = 10

# Load .env file
load_dotenv()

port_map_string = os.getenv('APPLICATION_PORT_MAP')
application_port_map = json.loads(port_map_string)
json_dump_file_path = os.getenv('JSON_DUMP_FILE_PATH')

pcpConfig = None
while True:
    driver = webdriver.Chrome("chromedriver")
    driver.get(url)

    # find username/email field and send the username itself to the input field
    driver.find_element("id", "txt_Username").send_keys(username)
    # find password input field and insert password as well
    driver.find_element("id", "txt_Password").send_keys(password)
    # click login button
    driver.find_element("name", "Submit").click()
    driver.find_element("name", "mainli_pcp").click()

    driver.implicitly_wait(10)

    iframe = driver.find_element("id", "frameContent")
    driver.switch_to.frame(iframe)

    try:
        # https://stackoverflow.com/questions/38363643/python-selenium-get-inside-a-document

        driver.find_element("id", "headPcpConfigList_0_0").click()  # anti-afk
        page_source = driver.page_source  # on the pcp forward rules page

        soup = BeautifulSoup(page_source, 'lxml')
        table = soup.find("table", {"id": "PcpConfigList_tbl"})

        for row in table.findAll("tr"):
            newPcpConfig = {}
            for app, port in application_port_map.items():
                newPcpConfig[app] = prune_row(row, port)
            if newPcpConfig != pcpConfig and newPcpConfig is not None:
                pcpConfig = newPcpConfig
                printToJsonFile(pcpConfig, json_dump_file_path)

    except Exception as e:
        print("error occurred trying to soup")
        logging.critical(e, exc_info=True)
        # driver.close()
        # quit(1)
    driver.close()
    countdown(interval)
