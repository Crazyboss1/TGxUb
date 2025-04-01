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

USER_SESSION = os.getenv("USER_SESSION", "BQAf70YAO7vzER8D2xYxwa5ONmK7FVhjt5SChdfZER-DrvG4OvnrqssHG6JDT2fzxiiYYVdOBHoWu9u4A8NzGTwhC9WDu8In0W4UGXEwINVRH-2U1OcGlobD81WP3RaBoKVqrVuqsTKf820yMqShVKvQmShFRmN4nMKQIpRjn5FUBBB7q84wJbrQDZMPfZnxv7RNNwDEKW60noS-hkVqtkSzLtDfbI4-f10r_PL4EoNjU-IySIij8WFqVwPiE6K6uaE9e2wcjVq4fk0kOY4HrbVyVPtXhVI0tH4oGN2Tnzrk4bHzh5WpAMf5tIlu5hU6B1mtPPYQ5fn3zFrX0dgIj55LLmRzMQAAAAGsfgmNAA")

DB_URI = os.getenv("DB_URI", "")

#LOG 
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "")
LOG_MESSAGE = os.getenv("LOG_MESSAGE", "")

#pm warn limit 
WARN_LIMIT = os.getenv("WARN_LIMIT", "5")
MAINBOT_UNAME = os.getenv("MAINBOT_UNAME", "EDITH")
#COMMAND SUFIX
CMD = ["*", ".", "!"]
