import sqlite3

def init_db():
    conn = sqlite3.connect("cosmetic.db")
    # ตารางหมวดหมู่สินค้า (เช่น Skin Care, Makeup, Perfume)
    conn.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)")
    
    # ตารางสินค้าเครื่องสำอาง
    conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        image_url TEXT,
        stock INTEGER DEFAULT 0,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    """)

    # เพิ่มหมวดหมู่เริ่มต้น
    default_cats = ["Skin Care", "Makeup", "Fragrance", "Hair Care", "Body Care"]
    for cat in default_cats:
        try:
            conn.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()
    print("cosmetic.db created successfully!")

if __name__ == "__main__":
    init_db()
