import sqlite3

conn = sqlite3.connect('../database.db')

cursor = conn.cursor()

cursor.execute("DELETE FROM products")
print(f"Rows deleted: {cursor.rowcount}")


conn.commit()
conn.close()