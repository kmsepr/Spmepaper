import requests
import datetime
import os
from io import BytesIO
from PIL import Image

# Config
EDITION = "Malappuram"
SAVE_DIR = "suprabhaatham_epaper"
PRAYER_PAGE = 6  # page-6 usually has prayer times

def get_today_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def fetch_epaper_data():
    url = "https://api2.suprabhaatham.com/api/ePaper"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def download_image(url, filename):
    resp = requests.get(url)
    resp.raise_for_status()
    img = Image.open(BytesIO(resp.content))
    img.save(filename)
    print(f"Saved: {filename}")

def run_daily():
    today = get_today_date()
    data = fetch_epaper_data()

    os.makedirs(SAVE_DIR, exist_ok=True)

    prayer_link = None
    for item in data:
        if EDITION in item.get("imageUrl", "") and today in item.get("date", ""):
            if f"page-{PRAYER_PAGE}-" in item["imageUrl"]:
                prayer_link = item["imageUrl"]
                break

    if prayer_link:
        filename = os.path.join(SAVE_DIR, f"page-{PRAYER_PAGE}.jpeg")
        download_image(prayer_link, filename)
        print(f"Prayer page saved: {filename}")
    else:
        print("Prayer page not found for today!")

if __name__ == "__main__":
    run_daily()