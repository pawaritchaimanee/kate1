import sqlite3

conn = sqlite3.connect("cosmetic.db")
conn.execute("INSERT INTO products (name, price, image_url, stock, category_id) VALUES (?, ?, ?, ?, ?)",
             ("Lipstick", 250.0, "https://via.placeholder.com/300x300?text=Lipstick", 10, 2))
conn.execute("INSERT INTO products (name, price, image_url, stock, category_id) VALUES (?, ?, ?, ?, ?)",
             ("Moisturizer", 150.0, "https://via.placeholder.com/300x300?text=Moisturizer", 5, 1))
conn.commit()
conn.close()
print("Sample products added")