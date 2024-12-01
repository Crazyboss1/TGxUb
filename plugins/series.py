import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

channel_username = "nocopypl"
bot_username = "Spidy_Series_bot"
DIGII = int(7448922857)

first_link = None
last_link = None
series_name = None
language = None
season = None
quality = None


def extract_series_details(text):
    pattern = r'^SADD\s+([^\s]+)\s+"([^"]+)"\s+"([^"]+)"\s+"([^"]+)"'
    match = re.match(pattern, text)
    if match:
        return match.groups()
    return None, None, None, None


async def send_to_bot_and_wait():
    global first_link, last_link, series_name, language, season, quality
    await Client.send_message(bot_username, text=f"/batch {first_link} {last_link}")

    # Wait for the bot to process and respond
    await asyncio.sleep(5)

    # Get the latest message from the bot
    async for message in matrix.get_chat_history(bot_username, limit=1):
        if message and message.text:
            edited_message_text = message.text

            # Now, send the quality command
            await matrix.send_message(
                bot_username,
                text=f"/quality {series_name} \"{language}\" \"{season}\" \"{quality}\" {edited_message_text}"
            )
            break

    # Reset global variables
    first_link = None
    last_link = None
    series_name = None
    language = None
    season = None
    quality = None


@Client.on_message(filters.channel & filters.chat(channel_username) & filters.text)
async def listen_channel(client: Client, message: Message):
    global first_link, last_link, series_name, language, season, quality
    text = message.text
    if text.startswith("SADD"):
        first_link = message.link
        series_name, language, season, quality = extract_series_details(text)
    elif text.startswith("SEND"):
        last_link = message.link
        # Send message to bot and wait for response
        await send_to_bot_and_wait()
