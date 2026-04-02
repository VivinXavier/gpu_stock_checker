import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}

PRODUCTS = [
    {
        "name": "RTX 5090",
        "url": "https://nvidia.onlinestpl.co.in/product/nvidia-geforce-rtx-5090"
    },
    {
        "name": "RTX 5080",
        "url": "https://nvidia.onlinestpl.co.in/product/nvidia-geforce-rtx-5080"
    }
]


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def is_in_stock(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().lower()
    return "out of stock" not in text


def main():
    alerts = []

    for p in PRODUCTS:
        try:
            r = requests.get(p["url"], headers=HEADERS, timeout=10)

            if r.status_code != 200:
                print(f"{p['name']} error {r.status_code}")
                continue

            if is_in_stock(r.text):
                alerts.append(f"🚀 {p['name']} IN STOCK!\n{p['url']}")
            else:
                print(f"{p['name']} out of stock")

        except Exception as e:
            print(f"{p['name']} failed: {e}")

    if alerts:
        send_telegram("\n\n".join(alerts))


if __name__ == "__main__":
    main()