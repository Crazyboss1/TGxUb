import os
from os import environ
import re 

id_pattern = re.compile(r'^.\d+$')

#API ID and HASH
API_ID = int(os.getenv("API_ID", "27348356"))
API_HASH = os.getenv("API_HASH", "a6dc1dbe3feb1c263f749ad5f95ff445")

#ADMINS
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6544671421 6484052423 7188908429').split()]
POSTERS = [int(poster) if id_pattern.search(poster) else poster for poster in os.environ.get('POSTERS', '1234567890').split()] + ADMINS

#Bot token and User String 
BOT_TOKEN = os.getenv("BOT_TOKEN", "6515902214:AAF5DnMU3LcrJpglXzrbW70BrQmrRisU6D0")

USER_SESSION = os.getenv("USER_SESSION", "BQAf70YACd1OpLAfVtosIeoPCgpCPhW2ttPjOxytr1wGHilj7NV-mEWbArcjbE0XO6P2ofdBzP5KAL7jv_N6Td5dDr8GZtKGIFFZymo2G1FSWEdY4fA3s_Sbv616aJ6WfW7TepKK262AwPiipElm2Z5WFU33n-yCz4FnXNpLD-Q0vRefCp-KDe4oHrGydTid1Un1QwShDKN-tBouzz0cSv9XKmZqmthvzBKsbuvCe8FWa9KDqa-l2s38iNKGknBs4VpRw0WhP73nglvP4l89R1g3Ko7xcpHiycBuZgE5weErGIyAkTxz2p6wvCcyUY7-RnhvTFhl9sU5ehMZ57SP242NjkdG2AAAAAGGF8K9AA")

DB_URI = os.getenv("DB_URI", "mongodb+srv://spm5:spm5@spm5.twy1d.mongodb.net/?retryWrites=true&w=majority&appName=Spm5")

#LOG 
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1002018707320")
LOG_MESSAGE = os.getenv("LOG_MESSAGE", "-1002220423739")

#pm warn limit 
WARN_LIMIT = os.getenv("WARN_LIMIT", "5")

#COMMAND SUFIX
CMD = ["*", ".", "!"]
