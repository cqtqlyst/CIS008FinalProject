from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import time
import random

import sqlite3

# setup selenium driver
options = Options()
# options.add_argument('--headless')
options.headless = True
driver = webdriver.Chrome(options=options)

# setup SQLite
connection = sqlite3.connect('../database.db')
cursor = connection.cursor()

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

    # find the <ol> tag, which contains the <div> elements
    ol_tag = soup.find('ol')

    first_level_divs = [div for div in ol_tag.find_all('div', recursive=False)]

    valid_divs = [div for div in first_level_divs if has_valid_image(div)]

    return valid_divs


def has_valid_image(div):
    # find all <img> tags within this <div>
    img_tags = div.find_all('img')

    if (img_tags):
        for img in img_tags:
            # check if the src attribute is a valid URL (some of these images will be lazy-loaded)
            src = img.get('src', '')
            if src and not src.startswith('data:image'):
                return True  # return True if there's a valid external image
        
    return False  # return False if no valid image is found

valid_divs = []

# functions for working through divs and finding the important 

def get_price(div):
    price_info = div.find('span', class_='priceinfo')
    if price_info:
        price = price_info.get_text(strip=True)
        price = price.replace("$", "")
        price = price.replace(",", "")
        price = int(price)
        return price
    return None

def get_product_link(div):
    link_info = div.find('a', class_="main")
    return link_info.get('href') if link_info else None

def get_img_link(div):
    img_info = div.find('img')
    if (img_info):
        src = img_info.get('src', '')
        if (src):
            return src
    return None

def get_name(div):
    name_info = div.find('span', class_="label")
    return name_info.get_text(strip=True) if name_info else None

def get_time(div):
    time_info = div.find('div', class_='meta')
    if time_info:
        # extract the time (text before the <span>)
        return time_info.contents[0].strip() if len(time_info.contents) > 0 else None
        

def get_location(div):
    location_info = div.find('div', class_='meta')
    if location_info:
        # extract the location (text after the <span>)
        return location_info.contents[2].strip() if len(location_info.contents) > 2 else None

for i in range(len(urls)):
    time.sleep(random.uniform(3, 10)) # wait so that we don't get flagged
    
    print(f"working on {urls[i]} now")

    driver.get(urls[i]) # grab the main code of this url
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * Math.random());") # scroll down to a random part of the page
    
    time.sleep(2) # let the page load

    html = driver.page_source

    valid_divs = filter_html(html) # get the valid_divs

    print(f"size of valid divs list for {urls[i]} is: {len(valid_divs)}")

    for div in valid_divs:

        # get all these important fields

        price = get_price(div)
        link = get_product_link(div)
        img = get_img_link(div)
        name = get_name(div)
        time_ago = get_time(div)
        location = get_location(div)
        category = url_categories[i]

        # print(price)
        # print(link)
        # print(img)
        # print(name)
        # print(time_ago)
        # print(location)

        # check that none of the fields are None
        try:
            if price is not None and link is not None and img is not None and name is not None and time_ago is not None and location is not None and category is not None:
                # prepare the insert query
                cursor.execute('''
                    INSERT INTO products (name, link, img, price, loc, time, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, link, img, price, location, time_ago, category))

                # commit the transaction to the database
                connection.commit()

                print(f"sucessfully commited to database from {urls[i]}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

driver.quit()

cursor.close()