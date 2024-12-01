from plugins.bot import bot
from plugins.matrix import matrix, db
from info import *
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiofiles
import requests
from aiohttp import web
from plugins import web_server
from pyrogram import idle
from pyrogram.raw.types import InputFile
from pyrogram.errors import FloodWait
import os
import random
import re
import time
import logging.config

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

BOT = bot
MATRIX = matrix

name = "main"
PORT = "8080"

def send_restart_message(bots_restarted, bots_errors):
    message_text = "⌬ Restarted Successfully!\n"
    for bot_name in bots_restarted:
        message_text += f"{bot_name}    ✅\n"
    if bots_errors:
        message_text += "\nBots with errors:\n"
        for bot_name, error in bots_errors.items():
            message_text += f"{bot_name}    {error}\n"
    BOT.send_message(chat_id=int(LOG_CHANNEL), text=message_text)

def autopics_task():
    try:
        while True:
            name = db.autopic.find_one({"name": "on"})
            if name:
                chat_history = MATRIX.get_chat_history(chat_id=int(PICS_ID), limit=300)
                all_processed = False  

                for message in chat_history:
                    if message.photo:                        
                        try:                      
                            photo=MATRIX.download_media(message=message.photo)
                            MATRIX.set_profile_photo(photo=photo)
                            os.remove(photo)
                        except Exception as e:
                            print(f"Error setting profile photo: {e}")
                            BOT.send_message(chat_id=int(LOG_CHANNEL), text=f"Error setting profile photo: {e}")
                        
                        photos = [p for p in MATRIX.get_chat_photos("me")]
                        MATRIX.delete_profile_photos(photos[1].file_id)
                        time.sleep(int(PIC_TIME))
                        
                all_processed = TRUE                    
                if all_processed:
                    print("All photos processed. Restarting loop...")
                    time.sleep(int(PIC_TIME))
                    continue
            else:
                break
        
    except Exception as e:
        BOT.send_message(chat_id=int(LOG_CHANNEL), text=f"Error processing photos: {e}")
    except FloodWait as e:
        BOT.send_message(chat_id=int(LOG_CHANNEL), text=f"flood = {e}")
    
def start_bots():
    bots_restarted = []
    bots_errors = {}
    
    try:
        BOT.start()
        bots_restarted.append("┠ BOT          ")    
    except Exception as e:
        bots_errors["┠ BOT"] = f"❌ {str(e)}"
        print(f"BOT ERROR - {e}")
        pass
    try:        
        MATRIX.start()        
        bots_restarted.append("┖ UB")
    except Exception as e:
        bots_errors["┖ UB"] = f"❌ {str(e)}"
        print(f"UB ERROR \n {e}")
        pass    
    send_restart_message(bots_restarted, bots_errors)
    
if __name__ == "__main__":
    try:        
        start_bots()    
        idle()           
        autopics_task()        
         # This will keep the bot running        
    except Exception as e:
        print(f"{e}")
    
