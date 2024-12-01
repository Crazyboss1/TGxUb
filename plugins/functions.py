import time
import re
import os
from os import environ
import asyncio
from plugins.matrix import matrix
from info import ADMINS
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from imdb import IMDb

POST_CHANNELS = list(map(int, (channel.strip() for channel in environ.get('POST_CHANNELS', '-1002377345015').split(','))))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/SpidySeries')

async def get_poster(query, bulk=False, id=False, file=None):
    if not id:
        # https://t.me/GetTGLink/4183
        query = (query.strip()).lower()
        title = query
        year = re.findall(r"[1-2]\d{3}$", query, re.IGNORECASE)
        if year:
            year = list_to_str(year[:1])
            title = (query.replace(year, "")).strip()
        elif file is not None:
            year = re.findall(r"[1-2]\d{3}", file, re.IGNORECASE)
            if year:
                year = list_to_str(year[:1])
        else:
            year = None
        movieid = imdb.search_movie(title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered = list(filter(lambda k: str(k.get("year")) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid = list(
            filter(lambda k: k.get("kind") in ["movie", "tv series"], filtered)
        )
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = query
    movie = imdb.get_movie(movieid)
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    plot = ""
    if not False:
        plot = movie.get("plot")
        if plot and len(plot) > 0:
            plot = plot[0]
    else:
        plot = movie.get("plot outline")
    if plot and len(plot) > 800:
        plot = plot[0:800] + "..."

    return {
        "title": movie.get("title"),
        "votes": movie.get("votes"),
        "aka": list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        "box_office": movie.get("box office"),
        "localized_title": movie.get("localized title"),
        "kind": movie.get("kind"),
        "imdb_id": f"tt{movie.get('imdbID')}",
        "cast": list_to_str(movie.get("cast")),
        "runtime": list_to_str(movie.get("runtimes")),
        "countries": list_to_str(movie.get("countries")),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_str(movie.get("languages")),
        "director": list_to_str(movie.get("director")),
        "writer": list_to_str(movie.get("writer")),
        "producer": list_to_str(movie.get("producer")),
        "composer": list_to_str(movie.get("composer")),
        "cinematographer": list_to_str(movie.get("cinematographer")),
        "music_team": list_to_str(movie.get("music department")),
        "distributors": list_to_str(movie.get("distributors")),
        "release_date": date,
        "year": movie.get("year"),
        "genres": list_to_str(movie.get("genres")),
        "poster": movie.get("full-size cover url"),
        "plot": plot,
        "rating": str(movie.get("rating")),
        "url": f"https://www.imdb.com/title/tt{movieid}",
    }


@matrix.on_message(filters.command("ipost", CMD))
async def ipost(client, message):
    query = message.text.split(" ", 1)
    
    if message.from_user.id not in ADMINS:
        return

    if len(query) < 2:
        return await message.edit("<b>Usage:</b> .ipost <movie_name>\n\nExample: .ipost Money Heist")
    
    await message.edit('𝖲𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀 𝖮𝗇 Imdb...')
    
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
        return await message.edit("No results found on IMDb for the provided series name.")
    
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
    await message.edit(
        "Multiple results found. Please select the correct series or choose 'No Link':",
        reply_markup=reply_markup
    )

@matrix.on_callback_query(filters.regex(r"^iimdb#"))
async def imdb_selection_callback(client, callback_query):
    imdb_id = callback_query.data.split("#")[1]
    if callback_query.from_user.id not in ADMINS:
        return

    movie = await get_poster(imdb_id, id=True)
    if not movie:
        return await callback_query.message.edit("Failed to retrieve IMDb data.")

    title = movie['title']
    year = movie['year']
    url = movie['url']
    languages = movie['languages']
    genres = movie['genres']
    search_link = f"tg://resolve?domain=SpidyMoviez_bot&start=search_{title.replace(' ', '_')}_{year}"
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
            await callback_query.message.edit(f"Error posting to channel {channel_id}: {str(e)}")

    await callback_query.answer("Movie details successfully posted to channels.")
    await callback_query.message.edit("Movie details successfully posted to channel ✅")

@matrix.on_message(filters.command('mpost', CMD))
async def manual_post(client, message):
    try:
        if message.from_user.id not in ADMINS:
            return

        if len(message.text.split()) < 2:
            return await message.edit("Please provide title.\nFormat:\n.mpost Movie.Name.Year #Language\nor\n.mpost Movie.Name.Year 🔊 Language1, Language2\nor\n.mpost Movie.Name.Year")
        
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
        search_link = f"tg://resolve?domain=SpidyMoviez_bot&start=search_{search_title}"
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
                await message.edit(f"Error posting to channel {channel_id}: {str(e)}")
        
        await message.edit("Posted successfully ✅")
        
    except Exception as e:
        await message.edit(f"An error occurred: {str(e)}")

@matrix.on_message(filters.command('spost', CMD))
async def smart_post(client, message):
    try:
        if message.from_user.id not in ADMINS:
            return

        if len(message.text.split()) < 2:
            return await message.edit("Please provide a title.\nFormat: .spost Movie.Name.2024")

        title = message.text.split(None, 1)[1]
        display_title = re.sub(r'[._]', ' ', title)
        await message.edit('🔍 Searching IMDb...')
        search_results = await get_poster(display_title, bulk=True)

        if not search_results:
            return await message.edit("No results found on IMDb.")

        buttons = [
            [InlineKeyboardButton(f"{movie['title']} ({movie['year']})", callback_data=f"simdb#{movie['imdb_id']}")]
            for movie in search_results[:5]
        ]
        buttons.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
        await message.edit(
            "Select the matching title from IMDb:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await message.edit(f"An error occurred: {str(e)}")

@matrix.on_callback_query(filters.regex(r"^simdb#"))
async def handle_simdb_selection(client, callback_query):
    try:
        if callback_query.from_user.id not in ADMINS:
            return

        imdb_id = callback_query.data.split('#')[1]
        movie = await get_poster(imdb_id, id=True)
        if not movie:
            return await callback_query.message.edit("Failed to fetch IMDb details.")

        await callback_query.message.edit(
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
            search_link = f"tg://resolve?domain=SpidyMoviez_bot&start=search_{search_title}"
            response_text += (
                f"\n\n⭐ <a href='{movie['url']}'>IMDb Info</a>\n"
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

            await callback_query.message.edit("Details successfully posted to channels ✅")
        except asyncio.TimeoutError:
            await callback_query.message.edit("No response received. Operation cancelled.")
    except Exception as e:
        await callback_query.message.edit(f"An error occurred: {str(e)}")

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
