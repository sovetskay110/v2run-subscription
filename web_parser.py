def main():
    merged = []

    for channel in CHANNELS:
        try:
            html  = fetch_html(channel)
        except Exception as e:
            print(f'⚠️ Ошибка при запросе @{channel}: {e}')
            continue

        posts = extract_bottom_posts(html, FETCH_NUM)
        for post in posts:
            lines = post.splitlines()
            for i, line in enumerate(lines):
                text = line.strip()

                # 1) trojan-группа из 3 строк
                if 'trojan' in text.lower():
                    group = lines[i:i+3]
                    merged.append(' '.join(l.strip() for l in group))

                # 2) отдельные vless:// строки
                if 'vless://' in text.lower():
                    merged.append(text)

    # Добавление ключа из секретов Codespaces
    vless1 = os.getenv('VLESS1')
    if vless1:
        merged.append(vless1)

    if not merged:
        print(f'⚠️ Не найдено ни trojan, ни vless в последних {FETCH_NUM} постах каналов {CHANNELS}')
        return

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        for item in merged:
            f.write(item + '\n')

    print(f'✅ Записано {len(merged)} записей (trojan + vless + VLESS1) из каналов {CHANNELS} в {OUT_FILE}')


