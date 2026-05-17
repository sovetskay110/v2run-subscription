import requests
from bs4 import BeautifulSoup
import hashlib
import os

URL = "https://t.me/s/vpn_free_one_day"
OUT_FILE = "subscribes.txt"


def get_last_posts(url, count=2):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    posts = soup.find_all("div", class_="tgme_widget_message_text")
    texts = [p.get_text("\n", strip=True) for p in posts]

    return texts[-count:]  # последние N постов


def hash_text(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def save_posts_overwrite(posts, path):
    # Полная перезапись файла
    with open(path, "w", encoding="utf-8") as f:
        for post in posts:
            h = hash_text(post)
            f.write("#hash:" + h + "\n")
            f.write(post + "\n\n")


if __name__ == "__main__":
    last_posts = get_last_posts(URL, 2)
    save_posts_overwrite(last_posts, OUT_FILE)
    print("Готово — subscribes.txt полностью перезаписан последними двумя постами")
