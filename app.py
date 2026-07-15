from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = "inventory.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL,
                reorder_threshold INTEGER NOT NULL,
                last_updated TEXT
            )
        """)
        # Initial seed
        seed = [
            ("Bananas (case)", "Produce", 18, 10),
            ("Bottled Water 16oz (case)", "Beverages", 6, 12)
        ]
        for item in seed:
            conn.execute("INSERT INTO items (name, category, quantity, reorder_threshold, last_updated) VALUES (?, ?, ?, ?, ?)",
                         (*item, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()

@app.route("/")
def index():
    conn = get_db()
    items = conn.execute("SELECT * FROM items ORDER BY name").fetchall()
    conn.close()
    return render_template("index.html", items=items)

@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        conn = get_db()
        conn.execute("INSERT INTO items (name, category, quantity, reorder_threshold, last_updated) VALUES (?, ?, ?, ?, ?)",
                     (request.form["name"], request.form["category"], int(request.form["quantity"]), 
                      int(request.form["reorder_threshold"]), datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
