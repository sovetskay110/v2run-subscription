import os
import requests
from bs4 import BeautifulSoup

CHANNEL = os.getenv("CHANNEL", "vpn_free_one_day").strip()
FETCH_LIMIT = int(os.getenv("FETCH_LIMIT", "2"))

URL = f"https://t.me/s/{CHANNEL}"
OUT_FILE = "subscribes.txt"


def fetch_posts():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", class_="tgme_widget_message_text")

    texts = [p.get_text("\n", strip=True) for p in posts]
    return texts[-FETCH_LIMIT:]  # последние N постов


def save_posts(posts):
    # Полное очищение файла (режим "w" перезаписывает файл)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for post in posts:
            f.write(post + "\n\n")


if __name__ == "__main__":
    posts = fetch_posts()
    save_posts(posts)
    print(f"Saved {len(posts)} posts from {CHANNEL} → {OUT_FILE}")

