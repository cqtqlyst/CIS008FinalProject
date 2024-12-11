import sqlite3

# Define the mapping of shorthand category codes to full names
category_map = {
    "ata": "antiques", "ppa": "appliances", "ara": "arts+crafts", "sna": "atv/utv/sno", 
    "pta": "auto parts", "ava": "aviation", "baa": "baby+kid", "bar": "barter", 
    "haa": "beauty+hlth", "bip": "bike parts", "bia": "bikes", "bpa": "boat parts", 
    "boo": "boats", "bka": "books", "bfa": "business", "cta": "cars+trucks", 
    "ema": "cds/dvd/vhs", "moa": "cell phones", "cla": "clothes+acc", "cba": "collectibles", 
    "syp": "computer parts", "sya": "computers", "ela": "electronics", "gra": "farm+garden", 
    "zip": "free", "fua": "furniture", "gms": "garage sale", "foa": "general", 
    "hva": "heavy equip", "hsa": "household", "jwa": "jewelry", "maa": "materials", 
    "mpa": "motorcycle parts", "mca": "motorcycles", "msa": "music instr", "pha": "photo+video", 
    "rva": "rvs+camp", "sga": "sporting", "tia": "tickets", "tla": "tools", 
    "taa": "toys+games", "tra": "trailers", "vga": "video gaming", "waa": "wanted", 
    "wta": "wheels+tires"
}

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Update the category in the database using the mapping
for shorthand, full_name in category_map.items():
    query = """
    UPDATE products
    SET category = ?
    WHERE category = ?
    """
    cursor.execute(query, (full_name, shorthand))

# Commit the changes
conn.commit()

# Verify the update
cursor.execute("SELECT DISTINCT category FROM products")
updated_categories = cursor.fetchall()
for category in updated_categories:
    print(category)

# Close the connection
conn.close()
