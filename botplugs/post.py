import time
import re
import os
from os import environ
import asyncio
from info import ADMINS, MAINBOT_UNAME
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from utils import get_poster

POST_CHANNELS = list(map(int, (channel.strip() for channel in environ.get('POST_CHANNELS', '-1002377345015').split(','))))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/SpidySeries')

start_time = time.time()

@Client.on_message(filters.command('ipost'))
async def getfile(client, message):
    query = message.text.split(" ", 1)
    if len(query) < 2:
        return await message.reply_text("<b>Usage:</b> /ipost <movie_name>\n\nExample: /post Money Heist")
    
    k = await message.reply('𝖲𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀 𝖮𝗇 Imdb...')
    
    file_name = re.sub(r"[.,()[]](?!\d+\d+)", " ", query[1].strip())
    title = re.sub(r"#\w+|[\U0001F600-\U0001F64F"
                   r"\U0001F300-\U0001F5FF"
                   r"\U0001F680-\U0001F6FF"
                   r"\U0001F700-\U0001F77F"
                   r"\U0001F780-\U0001F7FF"
                   r"\U0001F800-\U0001F8FF"
                   r"\U0001F900-\U0001F9FF"
                   r"\U0001FA00-\U0001FAFF"
                   r"\U00002700-\U000027BF]", "", file_name).strip()

    search_results = await get_poster(title, bulk=True)
    if not search_results:
        await k.delete()
        return await message.reply_text("No results found on IMDb for the provided series name.")
    
    buttons = []
    for movie in search_results:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{movie['title']} - {movie['year']}",
                    callback_data=f"iimdb#{movie['imdb_id']}",
                )
            ]
        )
    reply_markup = InlineKeyboardMarkup(buttons)
    await k.delete()
    await message.reply_text(
        "Multiple results found. Please select the correct series or choose 'No Link':",
        reply_markup=reply_markup
    )

@Client.on_callback_query(filters.regex(r"^iimdb#"))
async def imdb_selection_callback(client: Client, callback_query):
    imdb_id = callback_query.data.split("#")[1]
    movie = await get_poster(imdb_id, id=True)
    if not movie:
        return await callback_query.message.reply_text("Failed to retrieve IMDb data.")

    title = movie['title']
    year = movie['year']
    url = movie['url']
    languages = movie['languages']
    genres = movie['genres']
    search_link = f"tg://resolve?domain={MAINBOT_UNAME}&start=search_{title.replace(' ', '_')}_{year}"
    response_text = (
        f"<b>✅ {title} ({year})</b>\n\n"
        f"🔊 {languages}\n"
        f"⭐ <a href='{url}'>IMDB info</a>\n"
        f"🎥 Genre: {genres}"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Click Here To Search", url=search_link)]
    ])
    
    for channel_id in POST_CHANNELS:
        try:
            await client.send_message(
                chat_id=channel_id,
                text=response_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
        except Exception as e:
            await callback_query.message.reply_text(f"Error posting to channel {channel_id}: {str(e)}")

    await callback_query.answer("Movie details successfully posted to channels.")
    await callback_query.message.edit_text("Movie details successfully posted to channel ✅")

@Client.on_message(filters.command('mpost'))
async def manual_post(client, message):
    try:
        if len(message.text.split()) < 2:
            return await message.reply_text("Please provide title.\nFormat:\n/mpost Movie.Name.Year #Language\nor\n/mpost Movie.Name.Year 🔊 Language1, Language2\nor\n/mpost Movie.Name.Year")
        
        command_text = message.text.split(None, 1)[1]
        search_title = None
        response_text = None
        
        # Case 1: Title with #language
        if '#' in command_text:
            parts = command_text.split('#')
            title = parts[0].strip()
            language = parts[1].strip()
            
            display_title = re.sub(r'[._]', ' ', title)
            search_title = title.replace(' ', '_').replace('.', '_')
            response_text = f"<b>✅ {display_title}</b> #{language}"
            
        # Case 2: Title with 🔊 and languages
        elif '🔊' in command_text:
            parts = command_text.split('🔊')
            title = parts[0].strip()
            languages = parts[1].strip()
            
            display_title = re.sub(r'[._]', ' ', title)
            search_title = title.replace(' ', '_').replace('.', '_')
            response_text = f"<b>✅ {display_title}</b>\n\n🔊 {languages}"
            
        # Case 3: Just title
        else:
            title = command_text.strip()
            display_title = re.sub(r'[._]', ' ', title)
            search_title = title.replace(' ', '_').replace('.', '_')
            response_text = f"<b>✅ {display_title}</b>"
        
        # Create search link and keyboard
        search_link = f"tg://resolve?domain={MAINBOT_UNAME}&start=search_{search_title}"
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Click Here To Search", url=search_link)]
        ])
        
        # Post to all channels
        for channel_id in POST_CHANNELS:
            try:
                await client.send_message(
                    chat_id=channel_id,
                    text=response_text,
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            except Exception as e:
                await message.reply_text(f"Error posting to channel {channel_id}: {str(e)}")
        
        await message.reply_text("Posted successfully ✅")
        
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
        
@Client.on_message(filters.command('spost'))
async def smart_post(client, message):
    try:
        if len(message.text.split()) < 2:
            return await message.reply_text("Please provide a title.\nFormat: /spost Movie.Name.2024")

        title = message.text.split(None, 1)[1]
        display_title = re.sub(r'[._]', ' ', title)
        k = await message.reply('🔍 Searching IMDb...')
        search_results = await get_poster(display_title, bulk=True)

        if not search_results:
            await k.delete()
            return await message.reply_text("No results found on IMDb.")

        buttons = [
            [InlineKeyboardButton(f"{movie['title']} ({movie['year']})", callback_data=f"simdb#{movie['imdb_id']}")]
            for movie in search_results[:5]
        ]
        buttons.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
        await k.delete()
        await message.reply_text(
            "Select the matching title from IMDb:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_callback_query(filters.regex(r"^simdb#"))
async def handle_simdb_selection(client, callback_query):
    try:
        imdb_id = callback_query.data.split('#')[1]
        movie = await get_poster(imdb_id, id=True)
        if not movie:
            return await callback_query.message.edit_text("Failed to fetch IMDb details.")

        await callback_query.message.edit_text(
            f"Selected:\n<b>{movie['title']} ({movie['year']})</b>\n\n"
            "Send the name and optional language:\n\n"
            "Example:\nMalik.2021 #English\nor\nMalik.2021 🔊 English, Malayalam",
            parse_mode=ParseMode.HTML
        )

        # Wait for user input
        try:
            promp = "Now Send like Malik.2021 #language or 🔊 languages, mal, blah"
            response = await client.ask(callback_query.message.chat.id, promp, filters=filters.text, timeout=30)
            text = response.text
            display_title, response_text = process_language_input(text)

            search_title = display_title.replace(' ', '_').replace('.', '_')
            search_link = f"tg://resolve?domain={MAINBOT_UNAME}&start=search_{search_title}"
            response_text += (
                f"\n\n⭐ <a href='{movie['url']}'>IMDb</a> {movie.get('rating', 'N/A')}/10\n"
                f"🎥 Genre:{movie.get('genres', 'N/A')}"
            )

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Click Here To Search", url=search_link)]
            ])
            for channel_id in POST_CHANNELS:
                await client.send_message(
                    chat_id=channel_id,
                    text=response_text,
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )

            await callback_query.message.edit_text("Details successfully posted to channels ✅")
        except asyncio.TimeoutError:
            await callback_query.message.edit_text("No response received. Operation cancelled.")
    except Exception as e:
        await callback_query.message.edit_text(f"An error occurred: {str(e)}")

@Client.on_callback_query(filters.regex(r"^cancel"))
async def handle_cancel(client, callback_query):
    await callback_query.message.edit_text("Operation cancelled.")

def process_language_input(text):
    """Processes user input to extract title and optional languages."""
    if '#' in text:
        title, language = text.split('#', 1)
        display_title = re.sub(r'[._]', ' ', title.strip())
        response_text = f"<b>✅ {display_title}</b> #{language.strip()}"
    elif '🔊' in text:
        title, languages = text.split('🔊', 1)
        display_title = re.sub(r'[._]', ' ', title.strip())
        response_text = (
            f"<b>✅ {display_title}</b>\n\n"
            f"🔊 {', '.join(lang.strip() for lang in languages.split(','))}"
        )
    else:
        display_title = re.sub(r'[._]', ' ', text.strip())
        response_text = f"<b>✅ {display_title}</b>"
    return display_title, response_text
