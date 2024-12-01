import os
from os import environ
import re 

id_pattern = re.compile(r'^.\d+$')

#API ID and HASH
API_ID = int(os.getenv("API_ID", "22849062"))
API_HASH = os.getenv("API_HASH", "e043bdee9d6f5a0061ea83d51655113f")

#ADMINS
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6245128154').split()]

#Bot token and User String 
BOT_TOKEN = os.getenv("BOT_TOKEN", "7047759925:AAFH14m-13bfEhPYamEF2MsZimzjwtfkvcc")
#appu
USER_SESSION = os.getenv("USER_SESSION", "BAFcpiYAfXnuYkwHxwVxhjqkgEwhGpFXaUiM73OMU6d7HmhTdyBcAGujzhkUI3T_nHAF3fvZx2pG-0c35jxYK_xuO9w4T7nQt2x8Z75YIzYNs80bgyXLz0LidS-jpiQ2PjJ-X2Pufa-uxNo5zhq2swp-VjwM4NYLS6fSiIwu9x8ac0PyMaT2uevwLPR8H78CVD_iyH8J_nDgKSG8qKIwBQZdfU89d5wxREkBnACM6iG1lcJ8kRy8Cc7tpbDePrxZ-vb8PIpdNwyrU5SjYOT3N0pb057OjYnVM5OELiK2FxAisbxbyhyw58jG4ZlUcT7ScIDN9UIMH_NLSwzwCGHHKrRD6eVmqAAAAAF0PRfaAA")

#DB
DB_URI = os.getenv("DB_URI", "mongodb+srv://mat:mat@cluster0.vtqpi4l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

#LOG 
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1001668201351")
LOG_MESSAGE = os.getenv("LOG_MESSAGE", "-1001946828338")

#pm warn limit 
WARN_LIMIT = os.getenv("WARN_LIMIT", "5")

#COMMAND SUFIX
CMD = ["*", ".", "!"]

#AUTOPICZ 
PICS_ID = os.getenv("PICS_ID", "-1001904493290")
PIC_TIME = os.getenv("PIC_TIME", "600")
