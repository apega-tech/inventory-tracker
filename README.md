# Inventory & Task Tracker

A full-stack CRUD app for tracking floor inventory and flagging items that
need replenishment — modeled on real inventory workflows from a retail
supervisor role (achieving zero stockouts during peak hours by monitoring
stock levels against reorder thresholds).

## Stack
- **Backend:** Python (Flask)
- **Database:** SQLite
- **Frontend:** HTML/CSS (server-rendered via Jinja2 templates)

## Features
- View all inventory items with current quantity vs. reorder threshold
- Automatic low-stock flagging when quantity ≤ reorder threshold
- Add new items
- Update quantity in place
- Delete items
- Seeded with sample data on first run

## Run it locally
```bash
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## Why this project
This mirrors the actual inventory and replenishment workflows I managed as
a Supervisor at Food Garden Market — modeling stock data, structuring
reorder logic, and flagging issues before they became stockouts. Rebuilding
it as software was a natural first full-stack project: real domain
knowledge, a clear CRUD scope, and a direct line to a resume bullet.

## Possible next steps
- Add user authentication for multi-employee use
- Add a "restock history" log per item
- Deploy to Render/Railway for a live demo link
