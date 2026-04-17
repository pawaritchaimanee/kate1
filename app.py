from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("cosmetic.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
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

init_db()

@app.route("/")
def index():
    conn = get_db()
    products = conn.execute("""
        SELECT products.*, categories.name as category_name 
        FROM products 
        LEFT JOIN categories ON products.category_id = categories.id
    """).fetchall()
    conn.close()
    return render_template("cakemenu.html", products=products)

@app.route("/append", methods=["GET", "POST"])
def append():
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        image_url = request.form["image_url"]
        stock = request.form.get("stock", "0")
        category_id = request.form.get("category_id")
        
        conn.execute("INSERT INTO products (name, price, image_url, stock, category_id) VALUES (?, ?, ?, ?, ?)",
                     (name, price, image_url, stock, category_id))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("append.html", categories=categories)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        image_url = request.form["image_url"]
        stock = request.form["stock"]
        category_id = request.form["category_id"]
        
        conn.execute("UPDATE products SET name=?, price=?, image_url=?, stock=?, category_id=? WHERE id=?",
                     (name, price, image_url, stock, category_id, id))
        conn.commit()
        conn.close()
        return redirect("/")
    
    product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", product=product, categories=categories)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)