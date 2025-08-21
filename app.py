import os
import datetime
import requests
from flask import Flask, send_file

app = Flask(__name__)
IMG_PATH = "static/malappuram_page6.jpg"


def fetch_page6():
    """Fetch Malappuram edition page 6 from Suprabhaatham API."""
    url = "https://api2.suprabhaatham.com/api/ePaper"
    today = datetime.date.today().strftime("%Y-%m-%d")
    payload = {"edition": "Malappuram", "date": today}

    try:
        response = requests.post(url, json=payload, headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }, timeout=15)

        data = response.json()
        pages = data.get("pages", [])

        page6 = next((p for p in pages if p.get("pageNumber") == 6), None)
        if not page6:
            print("❌ Page 6 not found in API response")
            return False

        img_url = page6["imageUrl"]
        r = requests.get(img_url, timeout=15)
        if r.status_code == 200:
            os.makedirs("static", exist_ok=True)
            with open(IMG_PATH, "wb") as f:
                f.write(r.content)
            print("✅ Page 6 downloaded:", IMG_PATH)
            return True
        else:
            print("❌ Failed to download image:", r.status_code)
            return False

    except Exception as e:
        print("❌ Error fetching page 6:", str(e))
        return False


@app.route("/prayer")
def prayer():
    """Serve the latest Malappuram Page 6 image."""
    if not os.path.exists(IMG_PATH):
        fetch_page6()
    return send_file(IMG_PATH, mimetype="image/jpeg")


@app.route("/")
def home():
    return """
    <h2>Suprabhaatham - Malappuram Page 6</h2>
    <p><a href="/prayer">View Page 6</a></p>
    """


if __name__ == "__main__":
    # Fetch once on startup
    fetch_page6()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
