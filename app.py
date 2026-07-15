"""
Inventory & Task Tracker
A small full-stack CRUD app modeled on real floor-inventory workflows
(replenishment tracking, low-stock flags) from a retail supervisor role.

Run:
    pip install flask
    python app.py
Then visit http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "inventory.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL,
            reorder_threshold INTEGER NOT NULL,
            last_updated TEXT
        )
        """
    )
    conn.commit()

    # seed a few starter rows if the table is empty
    count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if count == 0:
        seed = [
            ("Bananas (case)", "Produce", 18, 10),
            ("Bottled Water 16oz (case)", "Beverages", 6, 12),
            ("Paper Towels (case)", "Household", 4, 8),
            ("Canned Beans", "Pantry", 40, 15),
            ("Whole Milk (gal)", "Dairy", 9, 10),
        ]
        for name, category, qty, threshold in seed:
            conn.execute(
                "INSERT INTO items (name, category, quantity, reorder_threshold, last_updated) VALUES (?, ?, ?, ?, ?)",
                (name, category, qty, threshold, datetime.now().strftime("%Y-%m-%d %H:%M")),
            )
        conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    items = conn.execute("SELECT * FROM items ORDER BY name").fetchall()
    conn.close()
    low_stock = [i for i in items if i["quantity"] <= i["reorder_threshold"]]
    return render_template("index.html", items=items, low_stock_ids={i["id"] for i in low_stock})


@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO items (name, category, quantity, reorder_threshold, last_updated) VALUES (?, ?, ?, ?, ?)",
            (
                request.form["name"],
                request.form["category"],
                int(request.form["quantity"]),
                int(request.form["reorder_threshold"]),
                datetime.now().strftime("%Y-%m-%d %H:%M"),
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/update/<int:item_id>", methods=["POST"])
def update_item(item_id):
    quantity = int(request.form["quantity"])
    conn = get_db()
    conn.execute(
        "UPDATE items SET quantity = ?, last_updated = ? WHERE id = ?",
        (quantity, datetime.now().strftime("%Y-%m-%d %H:%M"), item_id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    conn = get_db()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
