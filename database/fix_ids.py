import sqlite3

# Connect to the database
conn = sqlite3.connect('../database.db')
cursor = conn.cursor()

try:
    # Update the IDs to start from 0
    cursor.execute("""
    WITH RECURSIVE id_sequence AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY id) - 1 AS new_id
        FROM products
    )
    UPDATE products
    SET id = (SELECT new_id FROM id_sequence WHERE products.id = id_sequence.id);
    """)

    # Reset the AUTOINCREMENT value to 0
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'products';")

    # Commit the changes to the database
    # conn.commit()

    # Verify the changes
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    print("Updated rows:")
    for row in rows:
        print(row)

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
    conn.rollback()

conn.close()