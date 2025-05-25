import os
from telethon import TelegramClient, events
import re
import datetime
import asyncio

# === CONFIGURATION ===
api_id = 25440549  # <- your hardcoded API ID
api_hash = 'c13c2b66dccce92a8c95e4de3adbf533'  # <- your hardcoded API hash
session_name = 'link_forwarder'                 # Will store .session file

# Source channels to monitor
source_channels = [
    '@telugutechtuts',
    '@TechFactsDeals'
]

# Link converter bot username
link_converter_bot = '@ExtraPeBot'

# Daily run window (24-hour clock)
start_hour = 8    # 08:00
end_hour = 24     # Midnight

# === SETUP TELEGRAM CLIENT ===
client = TelegramClient(session_name, api_id, api_hash)
url_pattern = re.compile(r'https?://[^\s]+')


def is_within_run_window():
    now = datetime.datetime.now().time()
    start = datetime.time(hour=start_hour)
    end = datetime.time(hour=end_hour if end_hour != 24 else 0)
    if start < end:
        return start <= now < end
    else:
        return now >= start or now < end


@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    if not is_within_run_window():
        print('[!] Outside allowed time window — skipping.')
        return

    message_text = event.raw_text
    links = url_pattern.findall(message_text)
    if links:
        for link in links:
            try:
                await client.send_message(link_converter_bot, link)
                print(f'[✓] Forwarded: {link}')
            except Exception as e:
                print(f'[!] Failed to forward {link}: {e}')
    else:
        print('[!] No links found in this message.')


async def main():
    print('[✓] Starting Telegram client...')
    await client.start()
    print(f'[✓] Listening daily from {start_hour}:00 to {end_hour}:00.')

    while True:
        if not is_within_run_window():
            print('[!] Outside window — shutting down.')
            break
        await asyncio.sleep(60)

    await client.disconnect()
    print('[✓] Script stopped for the day.')


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
