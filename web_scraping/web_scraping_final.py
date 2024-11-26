from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from bs4 import BeautifulSoup

import time
import random

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

url_categories = [
    "ata",
    "ppa",
    "ara",
    "sna",
    "pta",
    "ava",
    "baa",
    "bar",
    "haa",
    "bip",
    "bia",
    "bpa",
    "boo",
    "bka",
    "bfa",
    "cta",
    "ema",
    "moa",
    "cla",
    "cba",
    "syp",
    "sya",
    "ela",
    "gra",
    "zip",
    "fua",
    "gms",
    "foa",
    "hva",
    "hsa",
    "jwa",
    "maa",
    "mpa",
    "mca",
    "msa",
    "pha",
    "rva",
    "sga",
    "tia",
    "tla",
    "taa",
    "tra",
    "vga",
    "waa",
    "wta"
]

urls = []

for url_prefix in url_categories:
  urls.append("https://sfbay.craigslist.org/search/" + url_prefix + "#search=1~gallery~0~0")

def filter_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the <ol> tag, which contains the <div> elements
    ol_tag = soup.find('ol')

    first_level_divs = [div for div in ol_tag.find_all('div', recursive=False)]

    valid_divs = [div for div in first_level_divs if has_valid_image(div)]

    return valid_divs


def has_valid_image(div):
    # Find all <img> tags within this <div>
    img_tags = div.find_all('img')

    if (img_tags):
        for img in img_tags:
            # Check if the src attribute is a valid URL (some of these images will be lazy-loaded)
            src = img.get('src', '')
            if src and not src.startswith('data:image'):
                return True  # Return True if there's a valid external image
        
    return False  # Return False if no valid image is found

all_components = []

# should be doing this section here for all urls but not because craigslist will block requests
driver.get(urls[0]) 

time.sleep(1.5)

html = driver.page_source

all_components.extend(filter_html(html))

random_component = random.choice(all_components)

def remove_price_info(div):
    price_info = div.find('span', class_='priceinfo')
    if price_info:
        price = price_info.text.strip()
        price_info.decompose()
        return price
    return None

real_price = remove_price_info(random_component)

modified_html = str(random_component)

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[-1])

driver.execute_script(f"document.body.innerHTML = `{modified_html}`;")

guessed_price = int(input("Guess what the price is: "))

print("the real price is " + real_price)

# time.sleep(10)

driver.quit()