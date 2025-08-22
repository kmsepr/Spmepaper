# app.py
from flask import Flask, jsonify, render_template_string
import requests
import threading
import time

app = Flask(__name__)

EPAPER_URL = "https://suprabhaatham.com/uploads/epaper/json/suprabhaatham.json"
epaper_data = {"pages": []}


def fetch_epaper_data():
    """Fetch ePaper JSON every 1 hour (in background)."""
    global epaper_data
    while True:
        try:
            r = requests.get(EPAPER_URL, timeout=10)
            if r.status_code == 200:
                epaper_data = r.json()
                print("✅ ePaper data updated")
        except Exception as e:
            print("⚠️ Error fetching ePaper:", e)
        time.sleep(3600)  # refresh every 1 hr


@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <title>Suprabhaatham ePaper</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 30px; }
            a { display: block; margin: 10px; font-size: 18px; text-decoration: none; color: blue; }
        </style>
    </head>
    <body>
        <h1>Suprabhaatham ePaper</h1>
        <a href="/editorial">Editorial Page (Page 6)</a>
        <a href="/all">All Pages</a>
    </body>
    </html>
    """)


@app.route("/editorial")
def editorial():
    """Return only page 6 (editorial)."""
    pages = epaper_data.get("pages", [])
    if len(pages) >= 6:
        return jsonify({"page_6": pages[5]})  # index 5 = page 6
    return jsonify({"error": "Page 6 not available"}), 404


@app.route("/all")
def all_pages():
    """Return all pages."""
    return jsonify(epaper_data)


if __name__ == "__main__":
    # Start background updater
    threading.Thread(target=fetch_epaper_data, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)