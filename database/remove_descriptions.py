import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute the DELETE query
cursor.execute("DELETE FROM products WHERE description LIKE 'south bay%'")

# Commit changes and close the connection
conn.commit()
conn.close()
