import sqlite3

conn = sqlite3.connect('../database.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        link TEXT NOT NULL,
        img TEXT NOT NULL,
        price INTEGER NOT NULL,
        loc TEXT NOT NULL,
        time TEXT NOT NULL
    )
''')

conn.commit()
conn.close()