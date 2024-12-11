import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(products);")
columns = cursor.fetchall()
for column in columns:
    print(column)

# Add the 'description' column if it doesn't exist
cursor.execute('''ALTER TABLE products ADD COLUMN description TEXT''')
connection.commit()

cursor.execute("PRAGMA table_info(products);")
columns = cursor.fetchall()
for column in columns:
    print(column)

# Close the connection
cursor.close()
connection.close()