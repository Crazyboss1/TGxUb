from pyrogram import Client, filters, enums
from pyrogram.types import Message
import logging
from info import *
import re 
import time
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BOT_START_TIME = time.time()
start_time = BOT_START_TIME


async def get_bot_uptimebot():
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    ###############################
    uptime_string = f"{uptime_days % 7}ᴅ : {uptime_hours % 24}ʜ : {uptime_minutes % 60}ᴍ : {uptime_seconds % 60}s"
    return uptime_string

@Client.on_message(filters.command('log') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command("start"))
async def check_alivebot(_, message):
    await message.reply("I am MATRIX ser's private Assistant")
    return
    
@Client.on_message(filters.command("uptime")) 
async def pingbot(_, message):    
    uptime = await get_bot_uptimebot()
    await message.reply_text(f"{uptime}")
