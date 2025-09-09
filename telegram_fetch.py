import os
import asyncio
from telethon import TelegramClient

API_ID = int(os.environ['TELEGRAM_API_ID'])
API_HASH = os.environ['TELEGRAM_API_HASH']
SESSION = os.environ['TELEGRAM_SESSION']
CHANNEL = 'vless_vpns'  # без @

async def main():
    client = TelegramClient(
        session=SESSION,
        api_id=API_ID,
        api_hash=API_HASH,
    )
    await client.start()
    entity = await client.get_entity(CHANNEL)
    # получаем 2 последних сообщения
    messages = await client.get_messages(entity, limit=2)
    # перезаписываем файл
    with open('subscribes.txt', 'w', encoding='utf-8') as f:
        for msg in reversed(messages):
            # msg.message содержит текст; можно расширить для медиа
            f.write(msg.message.strip() + '\n')
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
