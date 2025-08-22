from flask import Flask, Response
import requests
from datetime import datetime

app = Flask(__name__)

def get_epaper_url():
    """Fetch today's Suprabhaatham ePaper Page 6 image"""
    today = datetime.now().strftime("%Y-%m-%d")
    # Replace this with the actual Suprabhaatham API/IP source you were using earlier
    base_url = "https://suprabhaathamepaper.com/uploads/epaper"
    # Example: /2025/08/22/suprabhaatham-6.jpg
    page6_url = f"{base_url}/{today}/suprabhaatham-6.jpg"
    return page6_url

@app.route("/")
def home():
    """Show Page 6 directly on root"""
    img_url = get_epaper_url()
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
    """Same page accessible via /editorial"""
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)