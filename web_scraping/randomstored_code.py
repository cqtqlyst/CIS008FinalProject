!snap install chromium
!chromium-browser --version  # Check Chromium version
!chromedriver --version  

!apt-get update
!apt-get install -y chromium-chromedriver

!pip install selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import time
import random


# Set up Chrome options to run in headless mode
chrome_options = Options()

chrome_options.add_argument('--headless')  # Ensure GUI is not opened
chrome_options.add_argument('--no-sandbox')  # Bypass sandboxing
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome resource limits

# Specify the path to the chromedriver
webdriver_service = Service('/usr/lib/chromium-browser/chromedriver')

# Set up the WebDriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

driver.get('https://www.google.com')
print(driver.title)  # Print the page title

driver.quit()  # Close the browser session