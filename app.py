from flask import Flask, Response, render_template_string
import requests
import datetime

app = Flask(__name__)

EDITION = "Malappuram"
EDITORIAL_PAGE = 6

def get_today_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def fetch_epaper_data():
    url = "https://api2.suprabhaatham.com/api/ePaper"
    resp = requests.post(url, json={})  # The real site uses POST
    resp.raise_for_status()
    return resp.json()

def find_editorial_page():
    today = get_today_date()
    data = fetch_epaper_data()

    for item in data:
        if EDITION in item.get("imageUrl", "") and today in item.get("date", ""):
            if f"page-{EDITORIAL_PAGE}-" in item["imageUrl"]:
                return item["imageUrl"]
    return None

@app.route("/")
def home():
    return render_template_string("""
        <h2>Editorial Page</h2>
        <img src="/editorial_image" alt="Editorial Page" style="max-width:100%;"/>
    """)

@app.route("/editorial_image")
def editorial_image():
    url = find_editorial_page()
    if not url:
        return "Editorial page not found", 404

    resp = requests.get(url)
    return Response(resp.content, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)