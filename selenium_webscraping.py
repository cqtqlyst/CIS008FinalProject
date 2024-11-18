from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

url = 'https://sfbay.craigslist.org/search/apa#search=1~gallery~0~0'

driver.get(url)

time.sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(3)

html = driver.page_source

try:
    with open('webpage_with_imagesv2.html', 'w', encoding='utf-8') as file:
        file.write(html)

    print("Web page downloaded with images (JavaScript rendered).")
except:
    print("Failed to download the web page.")