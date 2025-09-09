import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID   = int(os.environ['TELEGRAM_API_ID'])
API_HASH = os.environ['TELEGRAM_API_HASH']
SESSION  = os.environ['TELEGRAM_SESSION']
CHANNEL  = 'vless_vpns'  # без @

async def main():
    # ИСПРАВЛЕНИЕ: используем StringSession(SESSION)
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.start()
    
    # Получаем 2 последних сообщения
    messages = await client.get_messages(CHANNEL, limit=2)
    
    # Перезаписываем файл
    with open('subscribes.txt', 'w', encoding='utf-8') as f:
        for msg in reversed(messages):
            f.write(msg.message.strip() + '\n')
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

