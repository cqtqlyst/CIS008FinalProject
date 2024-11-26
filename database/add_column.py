import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('../database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Add a new column to an existing table
cursor.execute("ALTER TABLE products ADD COLUMN category TEXT NO NULL")

# Commit the transaction to save changes
conn.commit()
# Close the connection
conn.close()