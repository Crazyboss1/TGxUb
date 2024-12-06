from SafoneAPI import SafoneAPI
from pymongo import MongoClient
from pyrogram import Client, filters, enums
from pyrogram.types import Message
import logging
from info import *
import re 
import time
import os 
from os import environ, execle, system
import sys
import asyncio
import random
from typing import Union
from time import time 
from bot import save_message

database = MongoClient(DB_URI)
db = database.my_database
warnings_collection = db.warnings
authorized_collection = db.authorized_users
sudo_collection = db.sudo_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

id_pattern = re.compile(r'^.\d+$')

BOT_START_TIME = time.time()
start_time = BOT_START_TIME


def extract_user(message: Message) -> Union[int, str]:
    """extracts the user from a message"""
    # https://github.com/SpEcHiDe/PyroGramBot/blob/f30e2cca12002121bad1982f68cd0ff9814ce027/pyrobot/helper_functions/extract_user.py#L7
    user_id = None
    user_first_name = None
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        # Retrieve the user's ID
        user_id = message.chat.id
        user_first_name = message.chat.first_name
            
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name

    elif len(message.command) > 1:
        if (
            len(message.entities) > 1 and
            message.entities[1].type == enums.MessageEntityType.TEXT_MENTION
        ):
           
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id
        try:
            user_id = int(user_id)
        except ValueError:
            pass
    else:
        return (user_id, user_first_name)
    return (user_id, user_first_name)


async def get_bot_uptimetor():
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    ###############################
    uptime_string = f"(¬‿¬)\n \n{uptime_days % 7}ᴅ : {uptime_hours % 24}ʜ : {uptime_minutes % 60}ᴍ : {uptime_seconds % 60}s"
    return uptime_string

@User.on_message(filters.chat(CHATS))
async def delete(user, message):
    try:
       _time = int(time()) + TIME 
       save_message(message, _time)
    except Exception as e:
       print(str(e))
        
@Client.on_message(filters.command("alive", CMD))
async def check_alivetor(client, message):
    me = await client.get_me()
    if message.from_user.id == me.id:
        await message.edit("Alert!  Living bot detected!")        
        return
    await message.reply("Alert!  Living bot detected!")
    
@Client.on_message(filters.command("uptime", CMD)) 
async def pingtor(client, message):    
    me = await client.get_me()
    uptime = await get_bot_uptimetor()
    if message.from_user.id == me.id:
        await message.edit(f"{uptime}")
        return 
    await message.reply_text(f"{uptime}")
        
@Client.on_message(filters.command(["restart", "rt"], CMD))
async def restart_bot(client, message):
    me = await client.get_me()
    user_id = message.from_user.id                        
    if (
        user_id not in ADMINS 
        and sudo_collection.find_one({"user_id": user_id}) is None
        and user_id != 6245128154
    ):
        return
    if message.from_user.id == me.id:
        msg = await message.edit("<b>Bot Restarting ...</b>")
    else:
        msg = await message.reply_text(text="<b>Bot Restarting ...</b>")        
    await msg.edit("<b>Restart Successfully Completed ✅</b>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "bot.py", environ)
        
@Client.on_message(filters.command(["addsudo", "asudo"], CMD)) 
async def add_sudo(client, message):
    me = await client.get_me()
    chat_type = message.chat.type
    if (
        len(message.command) == 1
        and not message.reply_to_message
        and chat_type != enums.ChatType.PRIVATE
    ):    
        if message.from_user.id == me.id:
            await message.edit("To proceed, Either reply with the specific user or provide the user's ID/username!")            
        else:
            await message.reply_text("To proceed, Either reply with the specific user or provide the user's ID/username!")
        return
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await message.reply(f"{error}")
    if from_user is None:
        if message.from_user.id == me.id:
            await message.edit("no valid user_id / message specified")
        else:
            await message.reply("no valid user_id / message specified")   
        return
    try:
        user_id = message.from_user.id                        
        if (
            user_id not in ADMINS 
            and sudo_collection.find_one({"user_id": user_id}) is None
            and user_id != 6105017520  # Add your user ID here
        ):
            if message.from_user.id == me.id:
                await message.edit("You don't have permission to use this command")
            else:
                await message.reply("You don't have permission to use this command")
            return
        try:
            if from_user_id:
                user_id = from_user.id
                is_sudo = sudo_collection.find_one({"user_id": user_id})
                if is_sudo:
                    if message.from_user.id == me.id:
                        await message.edit("Already sudo user!")
                    else:
                        await message.reply_text("Already sudo user!")        
                else:
                    sudo_collection.insert_one({"user_id": user_id})
                    warnings_collection.delete_many({"user_id": user_id})
                    if message.from_user.id == me.id:
                        await message.edit("Successfully added to sudo list.")
                    else:
                        await message.reply_text("Successfully added to sudo list.")
        except Exception as e:
            if message.from_user.id == me.id:
                await message.edit(f"{error}")
            else:
                await message.reply(f"{error}")    
    except Exception as e:
        if message.from_user.id == me.id:
            await message.edit(f"{e}")
        else:
            await message.reply(f"{e}")
                
@Client.on_message(filters.command(["remsudo", "rmsudo"], CMD)) 
async def rm_sudo(client, message):  
    me = await client.get_me()
    chat_type = message.chat.type
    if (
        len(message.command) == 1
        and not message.reply_to_message
        and chat_type != enums.ChatType.PRIVATE
    ):    
        if message.from_user.id == me.id:
            await message.edit("To proceed, Either reply with the specific user or provide the user's ID/username!")
        else:
            await message.reply_text("To proceed, Either reply with the specific user or provide the user's ID/username!")
        return 
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:        
        if message.from_user.id == me.id:
            await message.edit(f"{error}")
        else:
            await message.reply(f"{error}")
    if from_user is None:
        if message.from_user.id == me.id:
            await message.edit("no valid user_id / message specified")
        else:
            await message.reply("no valid user_id / message specified")
        return             
    try:                                
        user_id = message.from_user.id                        
        if (
            user_id not in ADMINS 
            and sudo_collection.find_one({"user_id": user_id}) is None
            and user_id != 6245128154
        ):
            if message.from_user.id == me.id:
                await message.edit("You don't have permission to use this command")
            else:
                await message.reply("You don't have permission to use this command")
            return 
        try:
            if from_user_id:
                user_id = from_user.id                
                is_sudo = sudo_collection.find_one({"user_id": user_id})
                if not is_sudo:
                    if message.from_user.id == me.id:
                        await message.edit("Already not in sudo list!")
                    else:
                        await message.reply_text("Already not in sudo list!")
                else:
                    sudo_collection.delete_one({"user_id": user_id})
                    if message.from_user.id == me.id:
                        await message.edit("Successfully removed from sudo list.")
                    else:
                        await message.reply_text("Successfully removed from sudo list.")
        except Exception as e:
            if message.from_user.id == me.id:
                await message.edit(f"{error}")
            else:
                await message.reply(f"{error}")    
    except Exception as e:
        if message.from_user.id == me.id:
            await message.edit(f"{e}")
        else:
            await message.reply(f"{e}")

@Client.on_message(filters.command(["approve", "a"], CMD)) 
async def add_approve(client, message):   
    me = await client.get_me()
    chat_type = message.chat.type
    if (
        len(message.command) == 1
        and not message.reply_to_message
        and chat_type != enums.ChatType.PRIVATE
    ):    
        if message.from_user.id == me.id:
            await message.edit("To proceed, Either reply with the specific user or provide the user's ID/username!")
        else:
            await message.reply_text("To proceed, Either reply with the specific user or provide the user's ID/username!")        
        return 
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        if message.from_user.id == me.id:
            await message.edit(f"{error}")
        else:
            await message.reply(f"{error}")
        return 
    if from_user is None:
        if message.from_user.id == me.id:
            await message.edit("no valid user_id / message specified")
        else:
            await message.reply("no valid user_id / message specified")    
        return 
    try:
        user_id = message.from_user.id                        
        if (
            user_id not in ADMINS 
            and sudo_collection.find_one({"user_id": user_id}) is None
            and user_id != 6245128154
        ):
            if message.from_user.id == me.id:
                await message.edit("You don't have permission to use this command")
            else:
                await message.reply("You don't have permission to use this command")
            return 
        try:
            if from_user_id:
                user_id = from_user.id
                is_auth = authorized_collection.find_one({"user_id": user_id})
                if is_auth:
                    if message.from_user.id == me.id:
                        await message.edit("Already authorised user!")
                    else:
                        await message.reply_text("Already authorised user!")
                else:
                    authorized_collection.insert_one({"user_id": user_id})
                    warnings_collection.delete_many({"user_id": user_id})
                    if message.from_user.id == me.id:
                        await message.edit("Successfully added to authorised users list.")
                    else:
                        await message.reply_text("Successfully added to authorised users list.")
        except Exception as e:
            if message.from_user.id == me.id:
                await message.edit(f"{error}")
            else:
                await message.reply(f"{error}")    
    except Exception as e:
        if message.from_user.id == me.id:
            await message.edit(f"{e}")
        else:
            await message.reply(f"{e}")
                
@Client.on_message(filters.command(["disapprove", "d"], CMD)) 
async def rm_disapprove(client, message):  
    me = await client.get_me()
    chat_type = message.chat.type
    if (
        len(message.command) == 1
        and not message.reply_to_message
        and chat_type != enums.ChatType.PRIVATE
    ):    
        if message.from_user.id == me.id:
            await message.edit("To proceed, Either reply with the specific user or provide the user's ID/username!")
        else:
            await message.reply_text("To proceed, Either reply with the specific user or provide the user's ID/username!")
        return 
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await message.reply(f"{error}")
    if from_user is None:
        if message.from_user.id == me.id:
            await message.edit("no valid user_id / message specified")       
        else:
            await message.reply("no valid user_id / message specified")
        return 
    try:                                
        user_id = message.from_user.id                        
        if (
            user_id not in ADMINS 
            and sudo_collection.find_one({"user_id": user_id}) is None
            and user_id != 6245128154
        ):
            if message.from_user.id == me.id:
                await message.edit("You don't have permission to use this command")
            else:
                await message.reply("You don't have permission to use this command")
            return 
        try:
            if from_user_id:
                user_id = from_user.id                
                is_auth = authorized_collection.find_one({"user_id": user_id})
                if not is_auth:
                    if message.from_user.id == me.id:
                        await message.edit("Already not in Authorized list!")
                    else:
                        await message.reply_text("Already not in Authorized list!")
                else:
                    authorized_collection.delete_one({"user_id": user_id})
                    if message.from_user.id == me.id:
                        await message.edit("Successfully removed from Authorized users list.") 
                    else:
                        await message.reply_text("Successfully removed from Authorized users list.") 
        except Exception as e:
            if message.from_user.id == me.id:
                await message.edit(f"{error}")
            else:
                await message.reply(f"{error}")    
    except Exception as e:
        if message.from_user.id == me.id:
            await message.edit(f"{e}")
        else:
            await message.reply(f"{e}")
                

@Client.on_message(filters.private)
async def handle_private_message(client, message):    
    me = await client.get_me()
    try:
        if message.from_user.is_bot:
            return
        user_id = message.from_user.id
        if (
            user_id not in ADMINS
            and sudo_collection.find_one({"user_id": user_id}) is None
            and authorized_collection.find_one({"user_id": user_id}) is None
            and user_id != 6245128154
        ):
            
            warning_count = warnings_collection.count_documents({"user_id": user_id})
            if int(warning_count) < int(WARN_LIMIT):
            # Issue a warning message
                user = await client.get_me()
                mention = user.mention                
                limit = int(WARN_LIMIT)
                warning_text = f"I am 🄷🄴🄻🄰 pmsecurity of {mention}, \n\nThis is your {warning_count + 1}/{limit} warning.\n\nIf you continue to send message, you will be banned and report as spam 🚫 \n\nYou can contact my admin through @mlz_botz_support"
                await message.reply_text(warning_text)
                warnings_collection.insert_one({"user_id": user_id})   
                
            else:
                # Block the user
                await message.reply_text("You have exceeded the warning limit. You are now blocked.")
                await client.block_user(user_id)
                warnings_collection.delete_many({"user_id": user_id})
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logger.exception(f"error in pm_security - {e}")
    if message.text:
        user_name = message.from_user.username or "<b>None</b>"
        user_id = message.from_user.id
        mension = message.from_user.mention
        await assistant.send_message(chat_id=LOG_MESSAGE, text=f"name: {mension} \nusername: {user_name}\nid: {user_id}\n\nmessage: {message.text}")
