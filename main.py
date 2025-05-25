import os
from telethon import TelegramClient, events
import re
import datetime
import asyncio

# === CONFIGURATION (HARDCODED) ===
api_id = 25440549  # <-- hardcoded API ID
api_hash = 'c13c2b66dccce92a8c95e4de3adbf533'  # <-- hardcoded API hash
session_name = 'link_forwarder'  # Will store .session file

# Source channels to monitor
source_channels = [
    '@telugutechtuts',
    '@TechFactsDeals'
]

# Link converter bot username
link_converter_bot = '@ExtraPeBot'

# === SETUP TELEGRAM CLIENT ===
client = TelegramClient(session_name, api_id, api_hash)
url_pattern = re.compile(r'https?://[^\s]+')


def is_within_run_window():
    # Always return True (no time window)
    return True


@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    if not is_within_run_window():
        print('[!] Outside allowed time window — skipping message.')
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
    print(f'[✓] Running 24/7 — no shutdown window.')

    while True:
        await asyncio.sleep(60)  # Keep running forever

    await client.disconnect()
    print('[✓] Script stopped.')


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
