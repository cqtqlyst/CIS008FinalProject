import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()


# Execute the SELECT query to retrieve all data from the 'products' table
cursor.execute('SELECT * FROM products')

# Fetch all rows of the result
products = cursor.fetchall()

# Optionally, print the results
for product in products:
    print(product)  # Each 'product' will be a tuple of values

conn.commit()
conn.close()