from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
import time
import random

# Setup Selenium WebDriver options
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Setup database connection
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Select all rows from the products table that don't have a description
cursor.execute('SELECT id, link FROM products WHERE description IS NULL OR description = ""')
rows = cursor.fetchall()

# Loop through each URL and scrape the description
for row in rows:
    product_id, product_url = row
    
    try:
        # Navigate to the Craigslist product page
        driver.get(product_url)
        time.sleep(random.uniform(1, 3))  # Be polite, wait a bit to mimic human behavior
        
        # Get the page source and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the meta tag with the description
        meta_tag = soup.find('meta', {'name': 'description'})
        if meta_tag:
            description = meta_tag.get('content')
        else:
            description = "No description available"
        
        # If no description is available, delete the row from the database
        if description == "No description available":
            cursor.execute('''
                DELETE FROM products
                WHERE id = ?
            ''', (product_id,))
            print(f"Deleted product ID {product_id} because no description was found.")
        else:
            # Update the description in the database for the current product
            cursor.execute('''
                UPDATE products
                SET description = ?
                WHERE id = ?
            ''', (description, product_id))
            print(f"Updated product ID {product_id} with description.")
        
        # Commit the changes to the database after each update or delete
        connection.commit()

    except Exception as e:
        print(f"Error scraping {product_url}: {e}")


# Execute the SELECT query to retrieve all data from the 'products' table
cursor.execute('SELECT * FROM products')

# Fetch all rows of the result
products = cursor.fetchall()

# Optionally, print the results
for product in products:
    print(product)  # Each 'product' will be a tuple of values

# Close resources
cursor.close()
connection.close()

# Close the Selenium driver
driver.quit()