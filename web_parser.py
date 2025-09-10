# web_parser.py

import os
import requests
from bs4 import BeautifulSoup

# Название канала (без @)
CHANNEL    = os.getenv('CHANNEL', 'vless_vpns')
URL        = f'https://t.me/s/{CHANNEL}'
FETCH_NUM  = 2
OUT_FILE   = 'subscribes.txt'

def fetch_html():
    resp = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    resp.raise_for_status()
    return resp.text

def extract_bottom_posts(html, n):
    soup   = BeautifulSoup(html, 'html.parser')
    blocks = soup.select('.tgme_widget_message_text')
    bottom = blocks[-n:] if len(blocks) >= n else blocks
    return [blk.get_text(separator='\n', strip=True) for blk in bottom]

def main():
    html  = fetch_html()
    posts = extract_bottom_posts(html, FETCH_NUM)

    merged = []
    for post in posts:
        lines = post.splitlines()
        for i, line in enumerate(lines):
            if 'trojan' in line.lower():
                group = lines[i:i+3]
                merged.append(' '.join(l.strip() for l in group))

    if not merged:
        print(f'⚠️ Не найдено строк с trojan в последних {FETCH_NUM} постах')
        return

    # Записываем склеенные группы строк без замены суффикса 'vpns'
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        for item in merged:
            f.write(item + '\n')

    print(f'✅ Записано {len(merged)} склеенных строк в {OUT_FILE}')

if __name__ == '__main__':
    main()
