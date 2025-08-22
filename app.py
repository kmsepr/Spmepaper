from flask import Flask, Response
import requests

app = Flask(__name__)

API_URL = "https://api2.suprabhaatham.com/api/ePaper"
EDITION = "Malappuram"
EDITORIAL_PAGE = 6   # Page 6 = Editorial

def get_editorial_url():
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        for item in data:
            if EDITION in item.get("imageUrl", ""):
                if f"page-{EDITORIAL_PAGE}-" in item.get("imageUrl", ""):
                    return item["imageUrl"]
    except Exception as e:
        print("Error fetching API:", e)
    return None


@app.route("/")
def home():
    img_url = get_editorial_url()
    if not img_url:
        return "<h2>Editorial page not available today!</h2>", 404

    html = f"""
    <html>
    <head><title>Suprabhaatham Editorial</title></head>
    <body style="margin:0;text-align:center;background:#f8f9fa;">
        <h2>Suprabhaatham - Page 6 (Editorial)</h2>
        <img src="{img_url}" style="width:100%;max-width:900px;border:1px solid #ccc;">
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")


@app.route("/editorial")
def editorial():
    return home()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)