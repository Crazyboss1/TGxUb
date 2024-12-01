from plugins.matrix import db
from info import *
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiofiles
import requests
from aiohttp import web
from plugins import web_server
from pyrogram import idle, Client
from pyrogram.raw.types import InputFile
from pyrogram.errors import FloodWait
import os
import random
import re
import time
import logging.config
import traceback

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.error(traceback.format_exc())

name = "main"
PORT = "8080"

matrix = Client(
        "user_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=USER_SESSION,
        plugins={"root": "plugins"}
)

bot = Client(
        "bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins={"root": "botplugs"}
)

def send_restart_message(bots_restarted, bots_errors):
    message_text = "⌬ Restarted Successfully!\n"
    for bot_name in bots_restarted:
        message_text += f"{bot_name}    ✅\n"
    if bots_errors:
        message_text += "\nBots with errors:\n"
        for bot_name, error in bots_errors.items():
            message_text += f"{bot_name}    {error}\n"
    bot.send_message(chat_id=int(LOG_CHANNEL), text=message_text)


def start_bots():
    bots_restarted = []
    bots_errors = {}
    
    try:
        bot.start()
        bots_restarted.append("┠ BOT          ")    
    except Exception as e:
        bots_errors["┠ BOT"] = f"❌ {str(e)}"
        print(f"BOT ERROR - {e}\n{traceback.format_exc()}")
        pass
    try:        
        matrix.start()        
        bots_restarted.append("┖ UB")
    except Exception as e:
        bots_errors["┖ UB"] = f"❌ {str(e)}"
        print(f"UB ERROR \n {e}\n{traceback.format_exc()}")
        pass    
    send_restart_message(bots_restarted, bots_errors)
    
if __name__ == "__main__":
    try:        
        start_bots()    
        idle()                   
    except Exception as e:
        print(f"{e}")
    
