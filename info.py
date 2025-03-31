import os
from os import environ
import re 

id_pattern = re.compile(r'^.\d+$')

#API ID and HASH
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")

#ADMINS
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
POSTERS = [int(poster) if id_pattern.search(poster) else poster for poster in os.environ.get('POSTERS', '1234567890').split()] + ADMINS

#Bot token and User String 
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

USER_SESSION = os.getenv("USER_SESSION", "")

DB_URI = os.getenv("DB_URI", "")

#LOG 
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "")
LOG_MESSAGE = os.getenv("LOG_MESSAGE", "")

#pm warn limit 
WARN_LIMIT = os.getenv("WARN_LIMIT", "5")
MAINBOT_UNAME = os.getenv("MAINBOT_UNAME", "EDITH")
#COMMAND SUFIX
CMD = ["*", ".", "!"]
